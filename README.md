# TelegramGithubBot
A bot that pulls info from github and pushes them to Telegram using python3.

~ also includes docker compatability! ~

# Currently the bot sends:
- Push
- Pulls
- Issues
- Branch Creation
- Branch Deletion
- Comments

# Usage 
- Download and install the Telegram.ext from https://github.com/python-telegram-bot/python-telegram-bot
  - ```sudo pip3 install python-telegram-bot```

- Install Flask ```sudo pip3 install flask```

- Install Pyngrok ```sudo pip3 install pyngrok```
  - Enable / Disable Pyngrok, depending on your usage, in the keys.py file.
  
- Set the tunnel url on the Github webhooks page (Found in repo settings)

- Move to directory and use: ```sudo nano keys.py``` (Replace required keys and add aditional tunnel information if necessary).
  - This bot requires the use of Content type: appliation/json

- Run ```sudo python3 main.py```

- The bot will then wait for the command /add from the desired chat

- Once the bot recieves the command it will add the chat_Id to a list

# Commands
/add - Adds the chat to the bots message list

# Depiction
![alt text](Depiction.png)
