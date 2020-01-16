from flask import Flask, request, render_template, redirect, url_for, jsonify
import hmac
import hashlib
import subprocess
from flask_ngrok import run_with_ngrok
import os
import json

app = Flask(__name__)
run_with_ngrok(app)
    
def verify_hmac_hash(data, signature):
    GitHub_secret = bytes('some secret', 'UTF-8')
    mac = hmac.new(GitHub_secret, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)   
    
@app.route("/payload", methods=['POST'])
def GitHub_payload():
    signature = request.headers.get('X-Hub-Signature')
    data = request.data
    if verify_hmac_hash(data, signature):
        if request.headers.get('X-GitHub-Event') == "ping":
            return jsonify({'msg': 'Ok'})
        if request.headers.get('X-GitHub-Event') == "push":
            payload = request.get_json()
        if payload['commits'][0]['distinct'] == True:
            try:
                cmd_output = subprocess.check_output(['git', 'pull', 'origin', 'master'],)
                return jsonify({'msg': str(cmd_output)})
            except subprocess.CalledProcessError as error:
                return jsonify({'msg': str(error.output)})
            else:
                return jsonify({'msg': 'invalid hash'})
if __name__ == "__main__":   
    context = ('ssl.cert', 'ssl.key') # certificate and key file. Cannot be self signed certs    
    app.run() # will listen on port 5000