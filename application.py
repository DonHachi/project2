import os

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app)

channels = []
users = []

msg={}

@app.route("/", methods = ["POST", "GET"])
def index():  
    code = 1
    if request.method == "POST":
        channel = request.form.get("channel_name")
        if (channel not in channels):
            channels.append(channel)
            msg[channel] = []
        else:
            code = 100 
        return render_template("index.html", channels=channels, code=code)
    else:
        return render_template("index.html", channels=channels, code=code)   

@app.route("/register", methods = ["POST", "GET"])
def register():
    code = 1
    if request.method == "POST":
        user = request.form.get("nickname")
        if (user not in users):
            users.append(user)
            return render_template("redirect.html", user = user)
        else:
            code = 101
        return render_template("register.html", users= users, code = code)
    else:
        return render_template("register.html")


@app.route("/channel/<string:channel>", methods = ["GET"])
def channel_creation(channel):
    print(msg[channel])
    return render_template("channels.html", channel = channel, msg = msg[channel])

@socketio.on('send message')
def newMessage(msg2):
    if (len(msg[msg2['channel']]) == 100):
        msg[msg2['channel']].pop(0)    
    msg[msg2['channel']].append(msg2)
    emit("new message", {"mensaje": msg2['mensaje'], "username": msg2['username'], "date": msg2['date'],"channel" : msg2['channel']}, broadcast= True)

if __name__ == '__main__':
    socketio.run(app)