from flask import Flask, render_template, url_for, jsonify, request
import main


app = Flask(__name__)


@app.route("/")
def home():
    return "<p>Hello user!</p>"


@app.route("/home")
def homepage():
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']

    response = main.get_response(message)
    return jsonify({
        'response': response
    })


if __name__ == "__main__":
    app.run(debug=True)
