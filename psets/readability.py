from cs50 import get_string
import re

text = get_string("Text: ")
text = text.casefold()

letters = 0
other = 0

for i in text:
    if i.isalpha():
        letters += 1
    else:
        other += 1

words = len(text.split())
regex = r"[.!?]"
sentences = len(re.findall(regex, text))

L = (letters * 100) / (words)
S = (sentences * 100) / (words)
CLI = (0.0588 * L) - (0.296 * S) - 15.8

grade = round(CLI)

print(f"sentences {sentences}, words: {words}, letters: {letters}, CLI: {CLI}")

if grade >= 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1")
else:
    print(f"Grade {grade}")
