from telegram.ext import (Updater, CommandHandler)
from flask import request
from flask import Flask
import telegram
import json 
import keys
import datetime

#Github webhook info grabber for Telegram
#Written by Jad El-Khatib 

currentDT = datetime.datetime.now()

app = Flask(__name__, instance_relative_config=True)

@app.route("/", methods =['POST'])     
def listener():
    request_data = request.get_json()
    event_type = request.headers["X-GitHub-Event"]
    
    if event_type == "push":
        tgBot.messageSender(bot,request_data,"push")
        return "Commit"
    
    if event_type == "commit_comment":
        tgBot.messageSender(bot,request_data,"commit_comment")
        return "Commit Comment"
    
    if event_type == "ping":
        print("ping")
        return "Ping"
    
    if event_type == "create":
        tgBot.messageSender(bot,request_data,"create")
        return "Create"
    
    if event_type == "issues":
        tgBot.messageSender(bot,request_data,"issues")
        return "Issue"
    
    if event_type == "issue_comment":
        tgBot.messageSender(bot,request_data,"issue_comment")
        return "Issue Comment"
    
    if event_type == "pull_request":
        tgBot.messageSender(bot,request_data,"pull_request")
        return "Pull Request"
    
    return "event_type invalid"
  
#Format the json for the users
def messageFormattar(request_data,event_type):
    
    origin = json.dumps(request_data)
    data = json.loads(origin)

    if event_type == "push":
        
        if data['after'] != "0000000000000000000000000000000000000000":
            repoName = data['repository']['name']
            repoUrl = data['repository']['html_url']
            branchName = data['ref']
            commitUrl = data['head_commit']['url']
            timeStamp = data['head_commit']['timestamp']
            committer = data['head_commit']['author']['username']
            commitMessage = data['head_commit']['message'].replace("_", " ")
            
            text = "*Github activity alert!* \nType: Commit/Push\nRepository: [" + repoName + "](" + repoUrl + ") / Branch: " + branchName[11:] + "\nCommit by: " + committer + "\nCommit message: " + commitMessage + "\n\n[Commit info](" + commitUrl + ")\nTimestamp: " + timeStamp
        else:
            repoName = data['repository']['name']
            repoUrl = data['repository']['html_url']
            branchName = data['ref']
            timeStamp = data['repository']['updated_at']
            branchCloser = data['sender']['login']
            
            text = "*Github activity alert!* \nType: Old Branch was Closed\nRepository: [" + repoName + "](" + repoUrl + ")\nBranch name: " + branchName[11:] + "\nBranch closed by: " + branchCloser + "\n\nTimestamp: " + timeStamp
    
    if event_type == "commit_comment":
        repoName = data['repository']['name']
        repoName = data['repository']['name']
        repoUrl = data['repository']['html_url']
        issuer = data['sender']['login']
        commentUrl = data['comment']['html_url']
        commentComment = data['comment']['body'].replace("_", " ")
        timeStamp = data['comment']['updated_at']
        
        text = "*Github activity alert!* \nType: New Commit Comment\nRepository: [" + repoName + "](" + repoUrl + ")\nCommit thread updated by: " + issuer + "\nThread Comment: " + commentComment + "\n\n[Thread info](" + commentUrl + ")\nTimestamp: " + timeStamp
     
    if event_type == "create":
        timeStamp = data['repository']['pushed_at']
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
        issueComment = data['issue']['body'].replace("_", " ")
        timeStamp = data['issue']['updated_at']
        
        text = "*Github activity alert!* \nType: New Comment\nRepository: [" + repoName + "](" + repoUrl + ")\nThread Title: " + issueTitle + "\nThread updated by: " + issuer + "\nThread Comment: " + issueComment + "\n\n[Thread info](" + issueUrl + ")\nTimestamp: " + timeStamp
     
    if event_type == "pull_request":
        pullStatus = data['action']
        repoName = data['repository']['name']
        repoUrl = data['repository']['html_url']
        requester = data['sender']['login']
        issueTitle = data['pull_request']['title']
        issueUrl = data['pull_request']['html_url']   
        
        if pullStatus == "opened":
            timeStampOpened = data['pull_request']['created_at']
            text = "*Github activity alert!* \nType: New Pull Request was Created\nRepository: [" + repoName + "](" + repoUrl + ")\nPull Title: " + issueTitle + "\nPull created by: " + requester + "\n\n[Pull info](" + issueUrl + ")\nTimestamp: " + timeStampOpened
        
        if pullStatus == "closed":
            timeStampClosed = data['pull_request']['closed_at']
            text = "*Github activity alert!* \nType: Old Pull Request was Closed\nRepository: [" + repoName + "](" + repoUrl + ")\nPull Title: " + issueTitle + "\nPull closed by: " + requester + "\n\n[Pull info](" + issueUrl + ")\nTimestamp: " + timeStampClosed
        
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

    



