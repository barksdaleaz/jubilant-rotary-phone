from cs50 import get_string

height = get_string("Height: ")

while (height >= 'a' and height <= 'z'):
    height = get_string("Height: ")

if not height:
    height = get_string("Height: ")

while (int(height) < 1 or int(height) > 8):
    height = get_string("Height: ")

for i in range (1, int(height) + 1):
    print(" "* (int(height) - i), end="")
    print("#"*i, end="")

    print("  ", end="")
    print("#"*i)

