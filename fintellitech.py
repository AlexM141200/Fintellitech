from flask import Flask, jsonify, request, render_template
import long_responses as long
import chat as chatbot

app = Flask(__name__)


@ app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    response = chatbot.check_all_messages(message.split())
    return jsonify({'response': response})


@ app.route("/")
def homepage():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run()
