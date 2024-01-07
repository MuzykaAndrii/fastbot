

class BaseMessages:
    about = """
<strong>🌐 The philosophy of this service is soft learning of foreign words by continuously seeing them (also known as Anki-method). 📚</strong>

<strong>Key Features: 💡</strong>
🗂️ Store multiple vocabularies with words to memorize. 
📆 The learning process occurs when the bot sends words from a specific vocabulary throughout the day (from 10 am to 11 pm) every 20 minutes.
📝 Test your skills by passing a quiz to ensure that you've already learned the vocabulary.

<strong>Commands: 🤖</strong>
✨ /create - Create a new vocabulary.
📋 /my - List your vocabularies and a menu to manage them.
🧠 /quiz - Take a quiz to test your knowledge (consisting of words from all your vocabularies). 
🚫 /disable - Disable notifications. 
🗑️ /cancel - Cancel the current command. 

<strong>Restrictions: 🚧</strong>
- Only one vocabulary can be active for notifications. Enabling one will turn off any other enabled vocabularies.
- Each vocabulary must have at least two word pairs (word pair - the word you're learning and its translation).
- The quiz button from the menu (/my command) will involve words from one vocabulary.
"""