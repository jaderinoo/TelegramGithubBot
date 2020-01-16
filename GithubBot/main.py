from telegram.ext import (Updater, CommandHandler)
from flask import request
from flask import Flask
from flask_ngrok import run_with_ngrok
from github_webhook import Webhook
import telegram
import json 
import keys
import datetime

#Coinmarketcap based Crypto price bot
#Written by Jad El-Khatib 

currentDT = datetime.datetime.now()

app = Flask(__name__)
webhook = Webhook(app)
run_with_ngrok(app)

@app.route("/", methods =['POST'])     
def hello_world():
    request_data = request.get_json()
    tgBot.messageSender(bot,request_data)
    return "Received and sent"

    
  
#Format the json for the users
def messageFormattar(request_data):
    
    origin = json.dumps(request_data)
    data = json.loads(origin)

    repoName = data['repository']['name']
    
    text = repoName
    return text
    
class tgBot(object):
    
    def messageSender(self,request_data):
        
        bot = telegram.Bot(keys.botKey)
        
        text = messageFormattar(request_data)
        
        bot.sendMessage(self.chat_id, text)
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

    



