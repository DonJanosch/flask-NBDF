from website import socketio, app

if __name__ == "__main__":
    #app.run(host='0.0.0.0',port=5000,debug=True)
    socketio.run(app, debug=True, host='0.0.0.0',port=5000)
