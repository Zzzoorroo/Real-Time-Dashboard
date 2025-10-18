from imports import *

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
    global thread
    print(f'Client connected: {request.sid}')
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

    socketio.emit("Connected", {'message':'Welcome!'}, to=request.sid)

#handling clienst disconnection
@socketio.on('disconnect')
def disconect ():
    print(f'Client disconnected: {request.sid}')

if __name__ == '__main__':
    socketio.run(app, debug=True, host="127.0.0.1" , port=5000)

#Global variable 
thread = None
thread_lock = Lock()
last_value = None 

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

def background_thread():
    print("Starting background thread for random value generation")
    #start with inital one
    current_value =  round(uniform(16.0, 26.0),2)
    while True:
        change = round(uniform(-1.0, 1.0), 2)
        current_value = max(16.0, min(26.0, current_value + change))
        current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f"Generated value: {current_value} at {current_value}")

        socketio.emit('updateValue', {'value': current_value, 'time': current_time})

        time.sleep(1)