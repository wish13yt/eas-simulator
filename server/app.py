from flask import Flask, render_template, request
from hashlib import sha256
import random, string
import os
import linecache

app = Flask(__name__)

@app.route("/")
def index():
    if os.path.exists("eas.txt"):
        with open("eas.txt", "r") as file:
            warning = linecache.getline('eas.txt', 1).rstrip('\n')
            type = linecache.getline('eas.txt', 2).rstrip('\n')
            messenger = linecache.getline('eas.txt', 3).rstrip('\n')
    else:
        warning = None
    return render_template('index.html', warning=warning, type=type, messenger=messenger)

@app.route("/api/makewarning", methods=['POST'])
def makewarning():
    warning = request.form['message']
    sentkey = request.form['key']
    type = request.form['type']
    service = request.form['service']
    with open("key.txt", "r") as file:
        key = file.read()
    if sentkey == key:
        with open("eas.txt", "w") as easfile:
            easfile.write(f"{warning}\n{type}\n{service}")
        if os.path.exists("key.txt"):
            os.remove("key.txt")
        return "EAS warning sent!"
    return "EAS warning was not sent."

@app.route("/api/getwarning", methods=["GET"])
def getwarning():
    if not os.path.exists("eas.txt"):
        warning = "No EAS warning is active."
    else:
        warning = linecache.getline('eas.txt', 1).rstrip('\n')
    return warning

@app.route("/api/gettype", methods=["GET"])
def gettype():
    if not os.path.exists("eas.txt"):
        type = "No EAS warning is active."
    else:
        type = linecache.getline('eas.txt', 2).rstrip('\n')
    return type

@app.route("/api/getmessenger", methods=["GET"])
def getmessenger():
    if not os.path.exists("eas.txt"):
        messenger = "No EAS warning is active."
    else:
        messenger = linecache.getline('eas.txt', 3).rstrip('\n')
    return messenger

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