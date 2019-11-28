import os
import requests

from flask import Flask, request, render_template, session, url_for, request, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room, Namespace
from flask_login import login_manager

# Confirguring App
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users = {"moderater"}
channels = {}
channels = set(channels)
messages = {}

# Main route
@app.route("/")
def login():
    if (session):
        return redirect('/chat')
    else:
        return render_template("login.html")

# User route, adding users to list 
@app.route("/user", methods=["POST", "GET"])
def user():
    if (session):
        return redirect('/chat')
    else:
        name = request.form.get('name')
        if not (name in users):   
            session['name'] = name
            users.add(name)
            return redirect('/chat')
        else:
            return "name already present"        


@app.route("/chat", methods=["POST", "GET"])
def chat():
    if not (session):
        return "Error please log in"
    else:
        return render_template("chat.html")

@app.route("/logout")
def logout():
    if (session):
        name = session['name']
        session.pop('name', None)
        session['Log'] = False
        session.clear()
        users.remove(name)
        return redirect("/")
    else:
        return redirect("/")

@socketio.on('join')
def join(data):
    user = session['name']
    room = data['room'] 
    join_room(room)
    emit('joined', {'room': room, 'username': user }, room= room)

# Sends message 
@socketio.on('send message')
def msg(data):
    currentChannel = data['channel']
    time = data['time']
    name = session['name']
    if not currentChannel in messages:
        msgslist = []
        msgslist.append(data['message'])
        msgslist.append(data['time'])
        msgslist.append(session['name'])
        messages[currentChannel] = msgslist
    else:
        messages[currentChannel].append(data['message']) 
        messages[currentChannel].append(time)
        messages[currentChannel].append(name)   
    if len(messages[currentChannel]) == 101: 
        messages[currentChannel].pop(0)
    addmsg = messages[currentChannel]
    emit('addmsg', addmsg, room = currentChannel)

# Adds the channel
@socketio.on('add_channel')
def addchannel(data):
    list = data['channel']
    if not (list in channels):
        channels.add(list)
        emit('add', list, broadcast = True)
    else:
        emit('error', 'Channel already present')    

if __name__ == '__main__':
    socketio.run(app, debug = 1)