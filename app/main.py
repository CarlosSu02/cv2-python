
import base64
from threading import Thread
from flask import Flask, render_template, request
import numpy as np
import gunicorn
from flask_socketio import SocketIO
import cv2

app = Flask(__name__);
socketio = SocketIO(app)

current_frame = None
sid = None

@app.get('/')
def index():
    # return { 'message': 'Hello strange!!' }
    return render_template('index.html')

@socketio.on('connect')
def connect():
    global sid
    sid = request.sid
    print(f'New client connected, id: {str(sid)}') 

@socketio.on('disconnect')
def disconnect():
    global sid
    print(f'Client disconnected, id: {str(sid)}') 

@socketio.on('frame')
def handle_frame(data):
    global current_frame
    img_data = base64.b64decode(data.split(',')[1])
    array = np.frombuffer(img_data, np.uint8) # Convert the image data to a NumPy array
    frame = cv2.imdecode(array, cv2.IMREAD_COLOR) # Decode the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_frame = gray
    # print(f"Received data: {data[:100]}...") 

def display_frames():
    global current_frame
    # print type current_frame
    while True:
        if current_frame is not None:
            cv2.imshow('Frame', current_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

if __name__ == '__main__':
    display_thread = Thread(target=display_frames, daemon=True) # Create a thread for displaying frames
    display_thread.start() # Start the thread
    gunicorn.SERVER_NAME = 'gunicorn'
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
