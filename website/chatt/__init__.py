from flask_socketio import SocketIO, send

from website import app

socketio = SocketIO(app)

@socketio.on('message')
def handleMessage(msg):
    print(f'Message recieved: {msg}')
