from website import socketio, app, email_scheduler

if __name__ == "__main__":
    #app.run(host='0.0.0.0',port=5000,debug=True)
    email_scheduler.start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
