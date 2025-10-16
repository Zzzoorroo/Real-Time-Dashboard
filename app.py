from flask import Flask , render_template
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #for cross origin resource sharing 

socketio = SocketIO(app, cors_allowed_origins="*")

#displaying the main page 
@app.route('/')
def index():
    return render_template('index.html')

#handling client connetion
@socketio.on('connect')
def connect():
    print(f'Client connected: {request.sid}')
    socketio.emit("Connected", {'message':'Welcome!'}, to=request.sid)

#handling clienst disconnection
@socketio.on('disconnect')
def disconect ():
    print(f'Client disconnected: {request.sid}')

if __name__ == '__main__':
    socketio.run(app, debug=True, host="127.0.0.1" , port=5000)