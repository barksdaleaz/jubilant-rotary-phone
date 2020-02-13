import csv
from cs50 import SQL
from sys import argv

if len(argv) != 2:
    print("Please type CSV file in command line.")
    exit()

# create database
open("students.db", "w").close()
db = SQL("sqlite:///students.db")

# create table
db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

with open(argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:  # split the string into 3 or 2 names
        vals = []

        for part in row["name"].split(" "):
            vals.append(part)

        vals.append(row["house"])
        vals.append(row["birth"])

        if len(vals) == 5:

            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", vals[:5])

        if len(vals) == 4:

            db.execute("INSERT INTO students (first, last, house, birth) VALUES (?, ?, ?, ?)", vals[:4])

csvfile.close()
