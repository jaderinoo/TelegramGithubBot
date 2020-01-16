from telegram.ext import (Updater, CommandHandler)
from flask import request
from flask import Flask
from flask_ngrok import run_with_ngrok
import telegram
import json 
import keys
import datetime

#Coinmarketcap based Crypto price bot
#Written by Jad El-Khatib 

currentDT = datetime.datetime.now()

app = Flask(__name__)
run_with_ngrok(app)

@app.route("/", methods =['POST'])     
def hello_world():
    request_data = request.get_json()
    event_type = request.headers["X-GitHub-Event"]
    
    if event_type == "push":
        tgBot.messageSender(bot,request_data)
        return "Received and sent"
    
    if event_type == "ping":
        print("ping")
        return "Ping"
    
    return "event_type invalid"
  
#Format the json for the users
def messageFormattar(request_data):
    
    origin = json.dumps(request_data)
    data = json.loads(origin)

    repoName = data['repository']['name']
    repoUrl = data['repository']['html_url']
    commitUrl = data['head_commit']['url']
    timeStamp = data['head_commit']['timestamp']
    committer = data['head_commit']['author']['username']
    commitMessage = data['head_commit']['message']
    
    text = "*Github activity alert!* \nRepository: [" + repoName + "](" + repoUrl + ")\nCommit By: " + committer + "\nCommit message: " + commitMessage + "\n[Commit info](" + commitUrl + ")\n\nTimestamp: " + timeStamp

    
    return text
    
class tgBot(object):
    
    def messageSender(self,request_data):
        
        bot = telegram.Bot(keys.botKey)
        
        text = messageFormattar(request_data)
        
        bot.sendMessage(self.chat_id, text, 'Markdown')
        return

    

    def __init__(self):
        super(tgBot, self).__init__()
        
        #initialize updaters
        self.updater = Updater(keys.botKey)     
        self.dp = self.updater.dispatcher
        
    def start(self,bot,update):     
        
        #save the chatID
        self.chat_id = update.message.chat_id
        
        print("----------------------\nBot started at: ")
        print(datetime.datetime.now())
        print("----------------------")
    
        #Initialize message
        message = "Bot has been initialized"
        
        #Sends the help message to the user
        bot.sendMessage(self.chat_id, message)

        #Run the flask instance
        app.run()
        
        return 
 
    #Initializes the telegram bot and listens for a command
    def main(self):
        #Creating Handler
        self.dp.add_handler(CommandHandler('start',self.start))
        
        #Start polling
        self.updater.start_polling()
        self.updater.idle()
    
if __name__ == '__main__':
    bot = tgBot()
    bot.main()

    



