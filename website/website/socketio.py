from website import socketio
from flask_socketio import send, emit

#Broadcast everything on infochat
@socketio.on('message', namespace='/infochat')
def broadcast_infochat(message):
    print(f'Recieved message {message}')
    send(message, broadcast=True)
