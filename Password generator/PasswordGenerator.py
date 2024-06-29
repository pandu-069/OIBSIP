import random

UpperCase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercase_letters = UpperCase_letters.lower()
digits = "0123456789"
sym = "(){}//!@#$%^&*<>:;|"

full = ""

UpperCase, lowercase, nums, symbols = False, False, False, False


print()
des1 = input("If you want uppercase letters to be present in the password then type 'yes' : ")
if des1 == "yes":
    UpperCase = True

des2 = input("If you want Lowercase letters to be present in the password then type 'yes' : ")
if des2 == "yes":
    lowercase = True

des3 = input("If you want numbers  to be present in the password then type 'yes' : ")
if des3 == "yes":
    nums = True

des4 = input("If you want Symbols  to be present in the password then type 'yes' : ")
if des4 == "yes":
    symbols = True



if UpperCase:
    full = full + UpperCase_letters
if lowercase:
    full = full + lowercase_letters
if nums:
    full = full + digits
if symbols:
    full = full + sym

length = 16
amount = 1

for i in range(amount):
    pas = "".join(random.sample(full, length))
    print(pas)
