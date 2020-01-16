import requests
from telegram.ext import (Updater, CommandHandler)
from github import Github
from flask import request
from flask import Flask
from flask import jsonify
from flask_ngrok import run_with_ngrok
from github_webhook import Webhook
import json 
import time
import keys
import datetime

#Coinmarketcap based Crypto price bot
#Written by Jad El-Khatib 

currentDT = datetime.datetime.now()

app = Flask(__name__)
run_with_ngrok(app)

@app.route("/", methods =['POST'])        # Standard Flask endpoint
def hello_world():
    if request.method == 'POST':
        print("Hey this works now!")
    return "Hello, World!"
    
if __name__ == '__main__':
    app.run()

    



