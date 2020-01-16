import requests
from telegram.ext import (Updater, CommandHandler)
from github import Github
import json 
import time
import keys
import datetime

#Coinmarketcap based Crypto price bot
#Written by Jad El-Khatib 

currentDT = datetime.datetime.now()
class tgBot(object):
    
    def __init__(self):
        super(tgBot, self).__init__()
        
        #initialize updaters
        self.updater = Updater(keys.botKey)     
        self.dp = self.updater.dispatcher
    
        #pull github related data
        self.auth = Github(keys.githubUsername, keys.githubPassword)
        self.repoList = keys.repoList
        
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
    
        for repo in self.auth.get_user().get_repos():
            bot.sendMessage(self.chat_id,repo.name)
    
        return 
    
        
    def help(self,bot,update): 
    
        #Pull chat ID
        chat_id = update.message.chat_id
            
        #Initialize message
        message = "This bot grabs repo commit updates and pushes them to Telegram"
        
        #Sends the help message to the user
        bot.sendMessage(chat_id, message)
        
        return
    
    
     
    #Initializes the telegram bot and listens for a command
    def main(self):
        #Creating Handler
        self.dp.add_handler(CommandHandler('help',self.help))
        self.dp.add_handler(CommandHandler('start',self.start))
        
        #Start polling
        self.updater.start_polling()
        self.updater.idle()
    
if __name__ == '__main__':
    bot = tgBot()
    bot.main()



