import hashlib as hl
print("Welcome to EAS Simulator.")
print("What password would you like to set for the controller?")
password = input()
encodedpw = hl.sha3_256(password.encode('utf-8')).hexdigest()
with open("password.txt", "w") as file:
    file.write(f"{encodedpw}")