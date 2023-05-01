from flask import Flask, jsonify, request, render_template
import long_responses as long
import chat as chatbot

import face_recognition
import cv2
import pickle
import os
import numpy as np

import tkinter as tk
from tkinter import messagebox
import dlib

from pathlib import Path
import glob
from facereco import Dlib_Face_Unlock


# import facereco as face
dfu = Dlib_Face_Unlock()


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
@app.route('/authenticate', methods=['POST'])
def authenticate():
    user = dfu.ID()
    if user == []:
        return jsonify(success=False, message="Face Not Recognised")
    else:
        return jsonify(success=True, user=user[0])


@ app.route("/login")
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        #Create images folder
        if not os.path.exists("images"):
            os.makedirs("images")
        #Create folder of person (IF NOT EXISTS) in the images folder
        Path("images/"+name).mkdir(parents=True, exist_ok=True)
        #Obtain the number of photos already in the folder
        numberOfFile = len([filename for filename in os.listdir('images/' + name)
                            if os.path.isfile(os.path.join('images/' + name, filename))])
        #Add 1 because we start at 1
        numberOfFile+=1
        #Take a photo code
        cam = cv2.VideoCapture(0)

        cv2.namedWindow("test")


        while True:
            ret, frame = cam.read()
            cv2.imshow("test", frame)
            if not ret:
                break
            k = cv2.waitKey(1)

            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                cam.release()
                cv2.destroyAllWindows()
                break
            elif k % 256 == 32:
                # SPACE pressed
                img_name = str(numberOfFile)+".png"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                os.replace(str(numberOfFile)+".png", "images/"+name.lower()+"/"+str(numberOfFile)+".png")
                cam.release()
                cv2.destroyAllWindows()
                break

        return render_template('login.html')
    else:
        return render_template('register.html')



@ app.route("/")
def homepage():
    user = request.args.get('user', '')
    return render_template('chat.html', user=user)


if __name__ == '__main__':
    app.run()
