from flask import Flask, jsonify, request, render_template
import long_responses as long
import chat as chatbot

# import facereco as face

app = Flask(__name__)


@ app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    response = chatbot.check_all_messages(message.split())
    return jsonify({'response': response})

# Initialize the face recognition class
# dfu = face.Dlib_Face_Unlock()

# Route for the face recognition functionality


# @app.route("/face_recognition", methods=['POST'])
# def face_recognition():
# data = request.get_json()
# response = {}
# Call the ID() method of the Dlib_Face_Unlock class to capture an image of the user
# and compare it with the images of known users in the system
# user = dfu.ID()
# if user:
#  response['message'] = 'Hello, ' + user[0] + '!'
# else:
#  response['message'] = 'Face not recognized'
# return jsonify(response)


@ app.route("/login")
def login():
    return render_template('login.html')


@ app.route("/")
def homepage():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run()
