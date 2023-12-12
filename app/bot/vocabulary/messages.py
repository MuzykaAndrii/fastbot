from app.bot.vocabulary.schemas import VocabularySetSchema


class VocabularyMessages:
    bulk_vocabulary_creation_rules = """
    <b>There are several rules to create bulk vocabulary:</b>

📝 <b>Format:</b> Enter word pairs with a hyphen "-" on each line.
🚫 <b>Minimum Pairs:</b> Include at least two pairs. Less won't cut it!
🔄 <b>Case Insensitive:</b> Cases don't matter; "Word - Translation" = "word - translation."
✨ <b>Special Characters:</b> Go ahead, use emojis, punctuation, or anything fancy!
➖ <b>Hyphen in Words:</b> Totally allowed, but only as a separator.
🌟 <b>Multiple Translations:</b> Use commas for multiple translations, like "Word - Translation, Another."
🎉 <b>Have Fun!</b> Enjoy expanding your vocabulary with the bot! 🚀
    """

    start_quiz_msg = """
🌟 <b>Welcome to Vocabulary Quiz!</b> 🌟

📚 <b>How to Play:</b>
1. 🤖 The bot will send you a word.
2. 📝 Respond with the translation of that word.
3. ✅ The bot will check if your answer is correct.

🔍 <b>Correctness Check:</b>
- 🧐 <b>Full translation:</b>
  - U can send all variants of translating separated y comma. (Then u should send all variants, in the correct order)

- 🕵️ <b>One variant translation:</b>
  - U also can send one variant of translation, if it will match with at least one correct variant, answer will be correct.

🤔 <b>Tips:</b>
- 🚫 Avoid using extra symbols or unnecessary details in your response.

🔇 <b>Alerts during the Quiz:</b>
- 🚨 All alerts will be disabled during the quiz.
- 🔚 They will be re-enabled when you press the "End Quiz" button or answer all the questions.

🚀 <b>Let's Start the Quiz!</b> 🚀
Simply respond to the bot's prompts with your translations, and let's see how well you know your vocabulary! 🌐💬
"""
    quiz_stats = """
🎉 <b>Quiz Results!</b> 🎉
🌟 You've completed the Vocabulary Quiz!

🏆 <b>Statistics:</b>

📈 <b>Total Words Attempted:</b> {total_words_attempted}
✅ <b>Correct Guesses:</b> {correct_guesses}
❌ <b>Wrong Guesses:</b> {wrong_guesses}
📊 <b>Success Rate:</b> {success_rate}%

👏 <b>Well Done!</b> Keep expanding your vocabulary and come back for more challenges! 🚀💬
"""
    leave_quiz = """
👋 <b>Leaving Quiz!</b> 👋

🚨 Oh no! It looks like you're leaving the Vocabulary Quiz.
Feel free to come back anytime! 👋✨
"""

    quiz_question = "[{answered}/{total}] Enter translation for: \"<b>{word}</b>\" 🤔"
    quiz_success_answer = "✅ {word} - <b>{translation}</b>"
    quiz_wrong_answer = "❌ {word} - <b>{translation}</b>. Your'e answer: <u>{suggestion}</u>"

    user_havent_any_vocabularies = "You're haven't any vocabularies yet("
    user_is_not_owner_of_vocabulary = "☢️ You're not owner of this vocabulary! ☢️"
    vocabulary_deleted_successfully = "🗑️ Vocabulary deleted successfully 🫡"
    vocabulary_dont_exists = "Vocabulary does not exist 🤷🏻‍♂️"

    vocabulary_already_active = "Notifications for this vocabulary already active 😉"
    notification_active = " "*20 + "alerts is on ✅"
    notification_unactive = " "*19 + "alerts is off 📴"
    vocabulary_entity_header = "📃 <i>{vocabulary_name}</i>{notification_status}\n"
    active_vocabulary = "✅ Alerts active for: <b>{vocabulary_name}</b>"
    no_active_vocabulary = "📵 Alerts is turned off"
    vocabulary_entity_item = "{number}. <b>{word}</b> - {translation}"
    language_pair_notification = "<b>{word}</b> - {translation}"
    
    @classmethod
    def get_full_vocabulary_entity_msg(cls, vocabulary_set: VocabularySetSchema) -> str:
        full_msg: list[str] = []
        if vocabulary_set.is_active:
            notification_status = cls.notification_active
        else:
            notification_status = cls.notification_unactive

        header = cls.vocabulary_entity_header.format(vocabulary_name=vocabulary_set.name, notification_status=notification_status)

        full_msg.append(header)

        for index, lang_pair in enumerate(vocabulary_set.language_pairs, start=1):
            full_msg.append(cls.vocabulary_entity_item.format(
                number=index,
                word=lang_pair.word,
                translation=lang_pair.translation,
            ))
        
        return "\n".join(full_msg)