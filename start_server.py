import subprocess, os

from server import socketio, app

db_dir = 'MongoDB'

db_path = os.path.join(os.getcwd(),db_dir)

if not os.path.exists(db_path):
    os.makedirs(db_path)

db_settings = ["mongod", "--dbpath", db_path]

subprocess.Popen(db_settings)

if __name__ == '__main__':
    socketio.run(app,debug=True)
