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
        tgBot.messageSender(bot,request_data,"push")
        return "Received and sent"
    
    if event_type == "ping":
        print("ping")
        return "Ping"
    
    if event_type == "create":
        tgBot.messageSender(bot,request_data,"create")
        return "Create"
    
    if event_type == "issues":
        tgBot.messageSender(bot,request_data,"issues")
        return "Create"
    
    if event_type == "issue_comment":
        tgBot.messageSender(bot,request_data,"issue_comment")
        return "Create"
    
    return "event_type invalid"
  
#Format the json for the users
def messageFormattar(request_data,event_type):
    
    origin = json.dumps(request_data)
    data = json.loads(origin)

    if event_type == "push":
        repoName = data['repository']['name']
        repoUrl = data['repository']['html_url']
        branchName = data['ref']
        commitUrl = data['head_commit']['url']
        timeStamp = data['head_commit']['timestamp']
        committer = data['head_commit']['author']['username']
        commitMessage = data['head_commit']['message']
        
        text = "*Github activity alert!* \nType: Commit/Push\nRepository: [" + repoName + "](" + repoUrl + ") / Branch: " + branchName + "\nCommit by: " + committer + "\nCommit message: " + commitMessage + "\n\n[Commit info](" + commitUrl + ")\nTimestamp: " + timeStamp

    if event_type == "create":
        timeStamp = data['head_commit']['timestamp']
        repoName = data['repository']['name']
        repoUrl = data['repository']['html_url']
        branchName = data['ref']
        branchCreator = data['sender']['login']
        
        text = "*Github activity alert!* \nType: New Branch was Created\nRepository: [" + repoName + "](" + repoUrl + ")\nNew branch name: " + branchName + "\nBranch created by: " + branchCreator + "\n\nTimestamp: " + timeStamp
    
    if event_type == "issues":
        issueStatus = data['action']
        repoName = data['repository']['name']
        repoUrl = data['repository']['html_url']
        issuer = data['sender']['login']
        issueTitle = data['issue']['title']
        issueUrl = data['issue']['html_url']
        
        if issueStatus == "opened":
            timeStampOpened = data['issue']['created_at']
            text = "*Github activity alert!* \nType: New Issue was Created\nRepository: [" + repoName + "](" + repoUrl + ")\nIssue Title: " + issueTitle + "\nIssue created by: " + issuer + "\n\n[Issue info](" + issueUrl + ")\nTimestamp: " + timeStampOpened
        
        if issueStatus == "closed":
            timeStampClosed = data['issue']['closed_at']
            text = "*Github activity alert!* \nType: Old Issue was Closed\nRepository: [" + repoName + "](" + repoUrl + ")\nIssue Title: " + issueTitle + "\nIssue closed by: " + issuer + "\n\n[Issue info](" + issueUrl + ")\nTimestamp: " + timeStampClosed
        
        
    if event_type == "issue_comment":
        repoName = data['repository']['name']
        repoName = data['repository']['name']
        repoUrl = data['repository']['html_url']
        issuer = data['sender']['login']
        issueTitle = data['issue']['title']
        issueUrl = data['issue']['html_url']
        issueComment = data['issue']['body']
        timeStamp = data['issue']['updated_at']
        
        text = "*Github activity alert!* \nType: New Issue Comment\nRepository: [" + repoName + "](" + repoUrl + ")\nIssue Title: " + issueTitle + "\nIssue updated by: " + issuer + "\nIssue Comment: " + issueComment + "\n\n[Issue info](" + issueUrl + ")\nTimestamp: " + timeStamp
        
        
    return text
    
class tgBot(object):
    
    def messageSender(self,request_data,event_type):
        
        bot = telegram.Bot(keys.botKey)
        
        text = messageFormattar(request_data,event_type)
        
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

    



