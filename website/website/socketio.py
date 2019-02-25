from website import socketio
from flask_socketio import send, emit

#Broadcast everything on infochat
@socketio.on('msg', namespace='/infochat')
def broadcast_infochat(msg):
    print(f'Recieved message {msg}')
    send(msg, broadcast=True)
