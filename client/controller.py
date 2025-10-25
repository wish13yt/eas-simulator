from hashlib import sha256
import requests
import sys
import inquirer 

print("EAS Simulator Controller")
url = input("Please enter the EAS server URL: ")
password = input("Please input a password to access the server: ")
encodedpw = sha256(password.encode('utf-8')).hexdigest()
data = {'password': encodedpw}
response = requests.post(url + "/api/login", data=data)
if response.text == "Your password wasn't valid. Try again!":
    print("Login failed.")
    sys.exit()
else:
    key = response.text
questions = [
    inquirer.List('emergency',
                message="Quick Emergency Menu",
                choices=['Tornado', 'Volcano', 'Missile', "Biochemical", "Other", "Revoke Warning"]
            ),
]
answers = inquirer.prompt(questions)
if answers['emergency'] == "Other":
    customeas = input("What EAS message would you like to show:")
    data = {'key': key, 'message': customeas}
    response = requests.post(url + "/api/makewarning", data=data)
if answers['emergency'] == "Tornado":
    eas = "A Tornado Warning was issued by " + url + ". Take shelter, and wait for further instruction."
    makedata = {'key': key, 'message': eas}
    makeresponse = requests.post(url + "/api/makewarning", data=makedata)
    print(eas + " was sent to the server!")
    print(makeresponse.text)
if answers['emergency'] == "Revoke Warning":
    data = {'key': key}
    response = requests.post(url + "/api/revoke", data=data)
    if response.text == "EAS revoked!":
        print("EAS was revoked successfully.")
    else:
        print("EAS was not revoked successfully. Try again!")