import csv

with open("ref/1.csv") as f:
    d = csv.reader(f, delimiter=";")
    for a in d:
        print(a)
