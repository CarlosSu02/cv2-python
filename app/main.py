
import base64
from datetime import datetime
from threading import Thread, Lock
import time
from chardet import detect
from flask import Flask, Response, redirect, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from matplotlib.pylab import det
import numpy as np
import gunicorn
import cv2
import mediapipe as mp
import cvzone.HandTrackingModule as htm

app = Flask(__name__)
# app.config['SOCKET'] = ''
CORS(app, resources={ r'/*': { 'origins': '*' } })

socketio = SocketIO(app, cors_allowed_origins='*')
# socketio = SocketIO(app)

current_frame = None
sid = None
# frame_clock = Lock()

# Load the cascade for face detection
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the mediapipe hands model
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

# Initialising detector from HandTrackingModule
detector = htm.HandDetector(detectionCon=0.6, maxHands=1)
# fingers_count = 0
fingers = {
    0: 'thumb',
    1: 'index',
    2: 'middle',
    3: 'ring',
    4: 'pinky',
}

# Time and FPS Calculation
c_time = 0
p_time = 0

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
    # faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # Draw rectangle around the faces
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)

    current_frame = frame

    # print(f"Received data: {data[:100]}...") 

    # with frame_clock:
    #     current_frame = gray

def show_name_finger(fingers_list):
    # print(fingers_list)
    # print(fingers_list.count(1))
    try:

        count = fingers_list.count(1);

        # if (count == 0):
        #     # return print('none')
        #     return cv2.putText(current_frame, f'{count}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

        if (count == 0 or (count > 1 and count < 5)):
            # return print(count)
            return cv2.putText(current_frame, f'{ count }', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

        if (count == 5):
            return cv2.putText(current_frame, f'all', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        
        # print(fingers[fingers_list.index(1)])

        return cv2.putText(current_frame, f'{ fingers[fingers_list.index(1)] }', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
    
    except Exception as err:
        print(err)

def display_frames():
    global current_frame
    global c_time
    global p_time
    # global fingers_count

    # print type current_frame
    while True:
        # with frame_clock:
        if current_frame is not None:

            hands, _ = detector.findHands(current_frame)

            if hands:
                # Hand Landmarks
                hand = hands[0]
                lm_list = hand['lmList']  # List of 21 Landmark points
                bbox = hand['bbox']  # Bounding box info x,y,w,h
                center = hand['center']  # Center of the hand cx,cy
                
                # Find how many fingers are up
                # fingers = detector.fingersUp(hands[0])
                # fingers_count = fingers.count(1)

                fingers_up = detector.fingersUp(hand)
                fingers_count = fingers_up.count(1)

                # print(fingers_up[0]) # Thumb finger

                show_name_finger(fingers_up)

                # cv2.rectangle(current_frame, (25, 150), (100, 400), (0, 255, 0) , cv2.FILLED)
                # cv2.putText(current_frame, f'{ fingers_count }', (10, 70), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 0), 2)

            # Time and FPS Calculation
            # c_time = time.time()
            # fps = 1/(c_time-p_time)
            # p_time = c_time
             
            # cv2.putText(current_frame, f'FPS: { str(int(fps)) }', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (139,0,0), 3)

            cv2.imshow('Frame', current_frame)
    
        if cv2.waitKey(30) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    display_thread = Thread(target=display_frames, daemon=True) # Create a thread for displaying frames
    display_thread.start() # Start the thread
    gunicorn.SERVER_NAME = 'gunicorn'
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
