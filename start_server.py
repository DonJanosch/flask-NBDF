import subprocess, os

# HTTP-Server handling
from server import socketio, app

# MongoDB handling
db_name = 'NBDF'
db_sub_dir = 'MongoDB'
mongoDB_dir = "C:\\Program Files\\MongoDB\\Server\\4.0\\bin"
db_deamon_path = os.path.join(os.getcwd(),db_sub_dir)
db_settings = [os.path.join(mongoDB_dir,'mongod'), "--dbpath", db_path,'--quiet']
os.environ['db_name'] = db_name
os.environ['db_deamon_path'] = db_deamon_path

# Helperfunctions
def gracefull_exit(mongod_process_handle):
    mongod_process_handle.kill()
    print('PYTHON: Gracefully turned off mongod.')

if __name__ == '__main__':
    try:
        #Create the MongoDB-Path if it does not exist
        if not os.path.exists(db_path):
            os.makedirs(db_path)

        # Fire up a supprocess to run the mongo-deamon
        mongod_process = subprocess.Popen(db_settings)

        # Start the http-server
        print('FLASK: Starting the Webserver')
        socketio.run(app)#,debug=True)
    except KeyboardInterrupt:
        # Stop the Websocket-connections
        # TODO: Emit shut-down event to notify the client
        socketio.stop()
        # Gracefully shut down the MongoDB-daemon
        gracefull_exit(mongod_process)
