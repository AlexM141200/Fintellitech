from flask import Flask, jsonify, request, render_template
import re
import requests
import long_responses as long
import subprocess
import testperception as psp
import chat as chatbot

app = Flask(__name__)


@ app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    response = chatbot.check_all_messages(message.split())
    return jsonify({'response': response})


@ app.route("/home")
def homepage():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run()
