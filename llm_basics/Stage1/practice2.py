# FILE HANDLING IN PYTHON

# -------------------------------
# 1. OPEN A FILE
# -------------------------------

file = open("sample.txt", "r")
print(file.read())
file.close()


# -------------------------------
# 2. WRITE TO A FILE
# -------------------------------

file = open("sample.txt", "w")
file.write("Hello World")
file.close()


# -------------------------------
# 3. APPEND TO A FILE
# -------------------------------

file = open("sample.txt", "a")
file.write("\nNew Line Added")
file.close()


# -------------------------------
# 4. READ ENTIRE FILE
# -------------------------------

file = open("sample.txt", "r")
content = file.read()
print(content)
file.close()


# -------------------------------
# 5. READ ONE LINE
# -------------------------------

file = open("sample.txt", "r")
print(file.readline())
file.close()


# -------------------------------
# 6. READ ALL LINES
# -------------------------------

file = open("sample.txt", "r")

for line in file:
    print(line)

file.close()


# -------------------------------
# 7. BEST PRACTICE: WITH OPEN
# -------------------------------

with open("sample.txt", "r") as file:
    print(file.read())


# -------------------------------
# FILE MODES
# -------------------------------

# "r"  -> Read
# "w"  -> Write (overwrites file)
# "a"  -> Append
# "x"  -> Create file
# "rb" -> Read binary
# "wb" -> Write binary


# -------------------------------
# 8. CHECK IF FILE EXISTS
# -------------------------------

import os

if os.path.exists("sample.txt"):
    print("File exists")
else:
    print("File does not exist")


# -------------------------------
# 9. DELETE A FILE
# -------------------------------

import os

if os.path.exists("sample.txt"):
    os.remove("sample.txt")
    print("File deleted")
else:
    print("File not found")


# -------------------------------
# 10. WRITE MULTIPLE LINES
# -------------------------------

lines = [
    "Python\n",
    "Java\n",
    "C++\n"
]

with open("languages.txt", "w") as file:
    file.writelines(lines)


# -------------------------------
# 11. READ + WRITE
# -------------------------------

with open("data.txt", "w+") as file:
    file.write("Hello")
    file.seek(0)
    print(file.read())


# -------------------------------
# IMPORTANT METHODS
# -------------------------------

# file.read()
# file.readline()
# file.readlines()
# file.write()
# file.writelines()
# file.close()
# file.seek()


# -------------------------------
# MOST IMPORTANT REAL-WORLD USAGE
# -------------------------------

with open("users.txt", "a") as file:
    name = input("Enter name: ")
    file.write(name + "\n")


with open("users.txt", "r") as file:
    for user in file:
        print(user.strip())