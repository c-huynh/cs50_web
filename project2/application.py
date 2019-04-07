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
