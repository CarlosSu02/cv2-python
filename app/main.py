
from ast import Dict
import base64
from datetime import datetime
import re
from threading import Thread, Lock
from flask import Flask, Response, redirect, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import numpy as np
import gunicorn
import cv2

app = Flask(__name__)
# app.config['SOCKET'] = ''
CORS(app, resources={ r'/*': { 'origins': '*' } })

socketio = SocketIO(app, cors_allowed_origins='*')
# socketio = SocketIO(app)

current_frame = None
sid = None
# frame_clock = Lock()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class User:
    def __init__(self, sid = None, date = ''):
        self.sid = sid
        self.date = date

    def data(self):
        return f'sid: { self.sid }, date: { self.date }'
    
    def res(self):
        return {
            'sid': self.sid,
            'date': self.date
        }
        
# current_user = None
current_user = User() # Not show error on init app

@app.get('/')
def index():
    return {
        'message': 'May the force be with you!',
    }, 200

'''
'''
@app.get('/video')
def video():
    # return { 'message': 'Hello strange!!' }
    return render_template('index2.html'), 200
    # return redirect('https://google.com', code=302)

@app.get('/status')
def status():
    # print(current_user.data())
    # return {
    #     'sid': sid
    # }, 200;
    return current_user.res(), 200

@socketio.on('connect')
def connect():
    global sid
    global current_user

    # print(request.sid, current_user.sid)

    sid = request.sid

    # current_user.sid = request.sid, 
    # current_user.date = datetime.now()
    
    current_user = User(sid, datetime.now())

    # emit('messages', { 'data': False })
    print(f'New client connected, id: { str(sid) }') 

@socketio.on('disconnect')
def disconnect():
    global sid
    global current_user
    
    print(f'Client disconnected, id: { str(sid) }')
    sid = None
    current_user = User()

@socketio.on('frame')
def handle_frame(data):
    global current_frame
    img_data = base64.b64decode(data.split(',')[1])
    array = np.frombuffer(img_data, np.uint8) # Convert the image data to a NumPy array
    frame = cv2.imdecode(array, cv2.IMREAD_COLOR) # Decode the image
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # emit('messages', { 'data': 'hello!' })

    # Detect faces
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)

    current_frame = frame
    # print(f"Received data: {data[:100]}...") 

    # with frame_clock:
    #     current_frame = gray


def display_frames():
    global current_frame
    # print type current_frame
    while True:
        # with frame_clock:
        if current_frame is not None:
                cv2.imshow('Frame', current_frame)
    
        if cv2.waitKey(30) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    display_thread = Thread(target=display_frames, daemon=True) # Create a thread for displaying frames
    display_thread.start() # Start the thread
    gunicorn.SERVER_NAME = 'gunicorn'
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
