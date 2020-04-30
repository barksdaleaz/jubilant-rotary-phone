import os
import csv
import psycopg2
from flask import Flask

t_host = "ec2-34-233-186-251.compute-1.amazonaws.com"
t_port = "5432"
t_dbname = "d3vi1v335jnocc"
t_user = "uhkjlpkgptxkde"
t_pw = "2da84bb87b1b8fec0d49989c4bebdd984090bbe1fb93b548d8bb1d0999ceedc5"
print("Connecting to database...")

conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
db = conn.cursor()

db.execute("CREATE TABLE books3 (isbn VARCHAR(13) NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INTEGER NOT NULL)")
conn.commit()
# with open('books.csv', 'r') as file:
    # next(file) # skip header row
    # db.copy_expert("""COPY books [(isbn, title, author, year)] FROM {'C:\Amber backup 2014\Amber\POSTGRAD\project1\project1\books.csv' | STDIN }""")
    # db.commit()

sql = "COPY %s FROM STDIN DELIMITER ',' CSV HEADER"
file = open("books.csv", "r")
table = "books3"

# db.execute("truncate " + table + ";")
db.copy_expert(sql=sql % table, file=file)
conn.commit()
db.close()
conn.close()

print("Loaded CSV into database.")
