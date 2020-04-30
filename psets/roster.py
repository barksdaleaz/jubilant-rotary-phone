import csv
from cs50 import SQL
from sys import argv


if len(argv) != 2:
    print("Please type Hogwarts House in command line.")
    exit()

# create database
open("students.db", "r").close()
db = SQL("sqlite:///students.db")

with open("students.db", "r") as students:

    for row in db.execute("SELECT first, middle, last, birth FROM students WHERE house = %s ORDER BY last, first", argv[1]):
        if row["middle"] == None:
            print(row["first"], row["last"], ", born", row["birth"])
        else:
            print(row["first"], row["middle"], row["last"], ", born", row["birth"])

students.close()
