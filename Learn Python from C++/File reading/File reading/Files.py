# Parampreet Singh - 20/06/20
# Reading and writing to files

import csv


fw = open("file2.txt", "w")  # Open file and write to it
fw.write("I am writing to this\n")  # Write to it
fw.write("Python programming\n")
fw.close()  # Close file

fr = open("file2.txt", "r")  # Open file to read
text = fr.read()  # Place contents in variable
print(text)
fr.close()


# CSV files (comma separated [delimiter = ","])


with open("file1.txt", "r") as csv_file:
    read_text = csv.reader(csv_file)  # Place text in variable

    next(read_text)  # Skips first line

    with open("file3.txt", "w") as file:  # Create a new file
        # and write contents with a delimeter of "-"
        text = csv.writer(file, delimiter="\t")

        for line in read_text:
            print(line)
            print(line[2])  # only print emails
            text.writerow(line)  # Turns comma to tabs
    file.close()


with open("file3.txt", "r") as file:
    # Have to specify delimiter if not comma when reading
    text = csv.reader(file, delimiter="\t")
    for line in text:
        print(line)
file.close()

with open("file1.txt", "r") as file:
    # Reading in Dictionary format (Key : Value)
    text = csv.DictReader(file)
    for line in text:
        print(line)
        print(line[' email'])  # Print values of speccific keys
file.close()

"""
with open("file4.txt", "w") as file1: # Write to a new file
    headers = ['first_name', 'last_name', 'email'] # fieldnames

    # fieldnames built in
    w_text = csv.DictWriter(file1, fieldnames=headers, delimiter="\t") # set the fieldnames
    w_text.writeheader()  # will write headers/field names

    for line1 in information:
        print(line1)
        del line["email"] # Delete all values of this key
        w_text.writerow(line1)
        print("\n\nIm writing\n\n")
file1.close()
"""
