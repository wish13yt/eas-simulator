from hashlib import sha256
import requests
import sys
import inquirer 
import os

print("EAS Simulator Controller")
if os.path.exists("server.txt"):
    with open("server.txt", "r") as file:
        urlserver = file.read()
        if not urlserver.endswith("/"):
            urlserver = urlserver + "/"
    url = input(f"Please enter the EAS server URL: {urlserver}") or urlserver
else:
    url = input("Please enter the EAS server URL: ")
    if not url.endswith("/"):
        url = url + "/"
password = input("Please input a password to access the server: ")
encodedpw = sha256(password.encode('utf-8')).hexdigest()
data = {'password': encodedpw}
response = requests.post(url + "/api/login", data=data)
if response.text == "Your password wasn't valid. Try again!":
    print("Login failed.")
    sys.exit()
else:
    key = response.text
    with open("server.txt", "w") as file:
        file.write(url)
        print("The server URL has been saved as your default server. To clear, delete 'server.txt'")
questions = [
    inquirer.List('emergency',
                message="Quick Emergency Menu",
                choices=['Tornado', 'Volcano', 'Missile', "Biochemical", "Other", "Revoke Warning"]
            ),
]
answers = inquirer.prompt(questions)
warnings = {"Tornado": f"A Tornado Warning was issued by {url}. Take shelter, and wait for further instruction.", "Volcano": f"A Volcano Alert was issued by {url}. Evacuate as quick as you can. Avoid lava. If outside, run. Do not stay inside."}
if answers['emergency'] == "Other":
    customeas = input("What EAS message would you like to show:")
    data = {'key': key, 'message': customeas}
    response = requests.post(url + "/api/makewarning", data=data)
if answers['emergency'] in warnings:
    eas = warnings[answers['emergency']]
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