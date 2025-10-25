from hashlib import sha256
print("Welcome to EAS Simulator.")
print("What password would you like to set for the controller?")
password = input()
encodedpw = sha256(password.encode('utf-8')).hexdigest()
with open("password.txt", "w") as file:
    file.write(f"password={encodedpw}")