from flask import Flask, render_template, request
from hashlib import sha256
import random, string
import os

app = Flask(__name__)

@app.route("/")
def index():
    if os.path.exists("eas.txt"):
        with open("eas.txt", "r") as file:
            warning = file.read()
    else:
        warning = None
    return render_template('index.html', warning=warning)

@app.route("/api/makewarning", methods=['POST'])
def makewarning():
    warning = request.form['message']
    sentkey = request.form['key']
    with open("key.txt", "r") as file:
        key = file.read()
    if sentkey == key:
        with open("eas.txt", "w") as easfile:
            easfile.write(warning)
        if os.path.exists("key.txt"):
            os.remove("key.txt")
        return "EAS warning sent!"
    return "EAS warning was not sent."

@app.route("/api/getwarning", methods=["GET"])
def getwarning():
    if not os.path.exists("eas.txt"):
        warning = "No EAS warning is active."
    else:
        with open("eas.txt", "r") as file:
            warning = file.read()
    return warning

@app.route("/api/login", methods=["POST"])
def login():
    password = request.form['password']
    with open("password.txt", "r") as file:
        realpass = file.read()
    if password == realpass:
        def random_char(y):
            return ''.join(random.choice(string.ascii_letters) for x in range(y))
        key = random_char(50)
        with open("key.txt", "w") as file:
            file.write(key)
        return key
    else:
        return "Your password wasn't valid. Try again!"
    
@app.route("/api/revoke", methods=["POST"])
def revoke():
    sentkey = request.form['key']
    key = open("key.txt", "r").read()
    if sentkey == key:
        if os.path.exists("eas.txt"):
            os.remove("eas.txt")
        if os.path.exists("key.txt"):
            os.remove("key.txt")
        return "EAS revoked!"
    else:
        return "Key invalid!"