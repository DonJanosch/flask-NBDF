from website import socketio
from flask_socketio import send, emit
from flask_login import current_user

#Broadcast everything on infochat
@socketio.on('message', namespace='/infochat')
def broadcast_infochat(message):
    if len(message)>0:
        author = 'Gast'
        if current_user.is_authenticated:
            author = current_user.firstname
        message = f'{author}: {message}'
        send(message, broadcast=True)
