import os

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

chatrooms = {}

@app.route("/")
def index():
    return render_template("index.html", chatrooms=chatrooms)

@app.route("/chatroom_list")
def chatroom_list():
    return jsonify(chatrooms)

@socketio.on("create chatroom")
def create_chatroom(data):
    new_chatroom = data["chatroom"]
    chatrooms[new_chatroom] = []
    emit("new chatroom", {'chatrooms': chatrooms, 'newChatroom': new_chatroom}, broadcast=True)

@socketio.on("new message")
def new_message(data):
    name = data["chatroom"]
    message = {
        "user": data["user"],
        "chatroom": data["chatroom"],
        "text": data["text"],
        "datetime": data["datetime"]
    }
    chatrooms[name].append(message)
    emit("broadcast new message", {'chatrooms': chatrooms, 'new_message': message}, broadcast=True)
