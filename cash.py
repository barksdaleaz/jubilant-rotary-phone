from cs50 import get_float

originalamt = get_float("Change owed: ")

while originalamt < 0:
    originalamt = get_float("Change owed: ")

if not originalamt:
    originalamt = get_float("Change owed: ")

# while originalamt >= 'a' and originalamt <= 'z':
    #originalamt = get_float("Change owed: ")

cents = round(originalamt * 100)

coins = 0

while cents > 0:
    if cents >= 25:
        cents -= 25
        coins += 1
    elif cents >= 10:
        cents -= 10
        coins += 1
    elif cents >= 5:
        cents -= 5
        coins += 1
    elif cents >= 1:
        cents -= 1
        coins += 1

print(f"{coins}")
