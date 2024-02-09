select_quiz_type_msg = """
Welcome to the Language Learning Quiz! 🌐📚
To get started, use the interactive keyboard below to choose your quiz type:

- Translate from Native to Foreign 🏠➡️🌍
- Translate from Foreign to Native 🌍➡️🏠
- Mixed Mode 🔄🔀

Select your preferred type and embark on a language-learning adventure! 🚀🗣️
"""

start_quiz_msg = """
🌟 <b>Welcome to Vocabulary Quiz!</b> 🌟

📚 <b>How to Play:</b>
1. 🤖 The bot will send you a word.
2. 📝 Respond with the translation of that word.
3. ✅ The bot will check if your answer is correct.

🔍 <b>Correctness Check:</b>
- 🧐 <b>Full translation:</b>
  - U can send several variants of translating separated y comma.

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

🏆 <b>Statistics:</b>

📈 <b>Total Words Attempted:</b> {total_words_attempted}
✅ <b>Correct Guesses:</b> {correct_guesses}
❌ <b>Wrong Guesses:</b> {wrong_guesses}
🔁 <b>Skipped:</b> {skipped_answers}
📊 <b>Success Rate:</b> {success_rate}%

👏 <b>Well Done!</b> Keep expanding your vocabulary and come back for more challenges! 🚀💬
"""
leave_quiz = """
👋 <b>Leaving Quiz!</b> 👋

🚨 Oh no! It looks like you're leaving the Vocabulary Quiz.
Feel free to come back anytime! 👋✨
"""

quiz_question = "[{current_question_num}/{total_question_count}] Enter translation for: \"<b>{question}</b>\" 🤔"
quiz_success_answer = "✅ {word} - <b>{translation}</b>"
quiz_wrong_answer = "❌ {word} - <b>{translation}</b>. Your'e answer: <u>{suggestion}</u>"
quiz_skipped_answer = "🔁 {word} - <b>{translation}</b>"