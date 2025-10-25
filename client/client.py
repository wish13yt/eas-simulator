import requests
import time
print("Welcome to EAS Simulator Client!")
print("NOTICE: This is SIMULATED. No alerts are real. This is SIMULATED.")
print("Licensed under Unlicense.")
print("What URL would you like to use (ex: https://example.com)")
url = input("")
if not url.endswith("/"):
    url = url + "/"
while True:
    time.sleep(5)
    response = requests.get(url + "api/getwarning")
    if response.text == "No EAS warning is active.":
        None
    else:
        print(response.text)