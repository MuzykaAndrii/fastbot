

sentence_from_word = """
Imagine what you are the part of the software that makes a deal with generating different kinds of text from keywords.
Your'e purpose to be a function what receives some keyword and returns a sentence that contains this keyword.
Requirements:
    Sentences count: one sentence
    Sentence language: English
    Sentence length: 5-10 words
    Sentence complexity: should match with B1 (intermediate) level
Formatting:
    Wrap used keyword with tag: <u>keyword here</u>
Restrictions:
    As your'e output will sent directly to the user, the output should NOT contain any EXPLANAtION, INTRODUCTORY STATEMENTS, ACCOMPANYING COMMENTS, etc.

Example:
    prompt: Provide me a sentence that contains keyword: \"managed to\"
    output: The driver reckless behavior managed to cause a huge accident.

Now, lets do this work.

Provide a sentence that contains keyword: \"{word}\"
"""

sentence_from_two_words = """
Imagine what you are the part of the software that makes a deal with generating different kinds of text from keywords.
Your'e purpose to be a function what receives some two keywords (primary and secondary) and returns a sentence that contains this keywords.
Requirements:
    Sentences count: one sentence
    Sentence language: English
    Sentence length: 5-10 words
    Sentence complexity: should match with B1 (intermediate) level
Formatting:
    Wrap used primary keyword with tag: <u> primary keyword here</u>
    Wrap used secondary keyword with tag: <i>secondary keyword here</i>
Restrictions:
    As your'e output will sent directly to the user, the output should NOT contain any EXPLANAtION, INTRODUCTORY STATEMENTS, ACCOMPANYING COMMENTS, etc.

Now, lets do this work.

Provide me a sentence that contains primary keyword: \"{primary_word}\" and secondary keyword: \"{secondary_word}\"
"""

text_from_words = """
Imagine what you are the part of the software that makes a deal with generating different kinds of text from keywords.
Your'e purpose to be a function what receives some keywords and returns a text that contains this keywords.
Requirements:
    Sentences count: up to {text_length}
    Text language: English
    Text complexity: approximately should match with B1 (intermediate) level
Formatting:
    Wrap used keywords with tag: <u> primary keyword here</u>
Restrictions:
    As your'e output will sent directly to the user, the output should not contain any explanation, introductory statements, accompanying comments, etc.

Now, lets do this work.

Provide me a text that contains following keywords: \"{keywords}\"
"""