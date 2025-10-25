import requests
import time
import os
print("Welcome to EAS Simulator Client!")
print("NOTICE: This is SIMULATED. No alerts are real. This is SIMULATED.")
print("Licensed under Unlicense.")
print("What URL would you like to use (ex: https://example.com)")
if os.path.exists("escurl.txt"):
    with open("escurl.txt", "r") as file:
        urlff = file.read()
        url = input(urlff) or urlff
else:
    url = input("")
    if not url.endswith("/"):
        url = url + "/"
    with open("escurl.txt", "w") as file:
        file.write(url)
print("Great! You are set for alerts from " + url + "!")
while True:
    time.sleep(5)
    response = requests.get(url + "api/getwarning")
    if response.text == "No EAS warning is active.":
        None
    else:
        print(response.text)