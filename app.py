from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
import os

app = Flask(__name__)
MESSAGE_FILE = 'messages.json'
USERS = ['User1', 'User2']

# Ensure message file exists
if not os.path.exists(MESSAGE_FILE):
    with open(MESSAGE_FILE, 'w') as f:
        json.dump([], f)

def load_messages():
    with open(MESSAGE_FILE, 'r') as f:
        return json.load(f)

def save_message(sender, receiver, message):
    messages = load_messages()
    messages.append({
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(MESSAGE_FILE, 'w') as f:
        json.dump(messages, f, indent=4)

def clear_messages():
    with open(MESSAGE_FILE, 'w') as f:
        json.dump([], f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sender = request.form.get('sender')
        receiver = request.form.get('receiver')
        message = request.form.get('message', '').strip()
        if sender in USERS and receiver in USERS and sender != receiver and message:
            save_message(sender, receiver, message)
        return redirect(url_for('index'))

    messages = load_messages()
    return render_template('index.html', users=USERS, messages=messages)

@app.route('/clear', methods=['POST'])
def clear():
    clear_messages()
    return redirect(url_for('index'))

# Prevent favicon 404s in debug
@app.route('/favicon.ico')
def favicon():
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
