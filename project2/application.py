import os
import requests

from collections import deque

from flask import Flask, jsonify, render_template, request, url_for, session, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit, send, join_room, leave_room
# from helpers import login_required -> deleted bc the login_required decorator
# cannot be used with SocketIO event handlers
# from: https://flask-socketio.readthedocs.io/en/latest/

# a list of channels that exist
existingchannels = {}

# a list of users that exist
existingusers = []

channelmessages = dict()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html", channels=existingchannels)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    # clear any previous users
    session.clear()

    # get the user's input
    username = request.form.get("username")

    if request.method == "POST":

        if not username:
            return render_template("error.html", message="Must input a username.")

        if username in existingusers:
            return render_template("error.html", message="That username already exists. Try another one.")

        # add the username to the existing list of usernames
        existingusers.append(username)

        # make this user the current user
        session['username'] = username

        # remember the user even if they close the browser
        session.permanent = True

        return redirect("/")
    else:
        return render_template("signin.html")

@app.route("/logout")
def logout():
    # remove them from the list of current users logged in
    try:
        existingusers.remove(session['username'])
    except ValueError:
        pass

    # remove the cookie from their browser
    session.clear()

    return redirect("/")

@app.route("/create", methods=["GET", "POST"])
def create():
    newchannelname = request.form.get("ch-name")
    if request.method == "POST":
        if newchannelname in existingchannels:
            return render_template("error.html", message="That channel already exists. Try another one.")
        else:
            existingchannels.append(newchannelname)
            existingchannels[newchannelname] = []
            # return jsonify({"success": True})
            # add channel to a gloabl dict of channels with messages
            # channelmessages[newchannelname] = deque()
        return render_template("index.html", channels=existingchannels)
    else:
        return render_template("index.html", channels=existingchannels)

@app.route("/channels/<channel>", methods=["GET", "POST"])
def channel(channel):
    session['current_channel'] = channel
    if request.method == "GET":
        return render_template("channel.html", channels=existingchannels)
    else:
        return redirect("/")

@socketio.on("joined")
def joined(data):
    room = session.get("current_channel")
    join_room(room)
    emit("status", {"userJoined": session.get("username"),
                    "channel": room,
                    "msg": session.get("username") + " has entered the chat"},
                    room=room)

@socketio.on("left")
def left(room_to_leave):
    #room = session.get("current_channel")
    leave_room(room_to_leave)
    emit("status",
        {"msg": session.get("username") + " has left the chat!! Tea~"},
        room=room_to_leave)
    return redirect("/")

@socketio.on("send message")
def sendmsg(message_data):
    channel = message_data["current_channel"]
    # count the number of messages
    channel_message_count = len(existingchannels[channel])
    # add the new message to the list
    existingchannels[channel].append(message_data)
    # if the messages exceed 100, delete the first one
    if (channel_message_count > 100):
        #channelmessages[channel].popleft()
        del existingchannels[channel][0]

    emit("announce message", message_data, broadcast=True, room=channel)
