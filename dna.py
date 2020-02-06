from sys import argv
from csv import reader, DictReader

if len(argv) != 3:
    print("Please enter CSV file name followed by TEXT file name")
    exit()

with open(argv[1]) as csvfile:
    people = reader(csvfile)
    for row in people:
        dnaSeq = row
        dnaSeq.pop(0)
        break

with open(argv[2]) as textfile:
    dnareader = reader(textfile)
    for row in dnareader:
        dnalist = row

str_list = dnalist[0]
sequences = {}
for item in dnaSeq:
    sequences[item] = 1

for key in sequences:
    l = len(key)
    tempMax = 0
    temp = 0
    for i in range(len(str_list)):
        while temp > 0:
            temp -= 1
            continue
        if str_list[i: i + l] == key:
            while str_list[i - l: i] == str_list[i: i + l]:
                temp += 1
                i += l
            if temp > tempMax:
                tempMax = temp
    sequences[key] += tempMax

with open(argv[1], newline='') as csvfile:
    people = DictReader(csvfile)
    for person in people:
        match = 0
        for str_list in sequences:
            if sequences[str_list] == int(person[str_list]):
                match += 1
        if match == len(sequences):
            print(person['name'])
            exit()

    print("No match.")
