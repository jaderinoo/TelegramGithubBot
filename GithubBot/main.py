from requests import Session
from telegram.ext import (Updater, CommandHandler)
import json 
import time
import keys
import datetime

#Coinmarketcap based Crypto price bot
#Written by Jad El-Khatib 

currentDT = datetime.datetime.now()

def start(bot,update): 
    
    #chatID
    chat_id = update.message.chat_id
    
    #Pull chat ID
    chatID = str(chat_id)
    
    print("----------------------\nBot started at: ")
    print(datetime.datetime.now())
    print("----------------------")

    #Initialize message
    message = "Bot has been initialized"
    
    #Sends the help message to the user
    bot.sendMessage(chat_id, message)

    return 

def help(bot,update): 

    #Pull chat ID
    chat_id = update.message.chat_id
        
    #Initialize message
    message = "This bot grabs repo commit updates and pushes them to Telegram"
    
    #Sends the help message to the user
    bot.sendMessage(chat_id, message)
    
    return

#Initializes the telegram bot and listens for a command
def main():
    updater = Updater(keys.botKey)     
    dp = updater.dispatcher
    
    #Creating Handler
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CommandHandler('start',start))
    
    #Start polling
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()



