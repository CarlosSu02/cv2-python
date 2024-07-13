
import base64
from datetime import datetime
from threading import Thread, Lock
import time
from flask import Flask, Response, redirect, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import numpy as np
import gunicorn
import cv2
import mediapipe as mp

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

def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 Fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[mp_hands.HandLandmark(id * 4)].y < hand_landmarks.landmark[mp_hands.HandLandmark(id * 4 - 2)].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return fingers

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

def display_frames():
    global current_frame
    global c_time
    global p_time

    # print type current_frame
    while True:
        # with frame_clock:
        if current_frame is not None:
            RGB_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
            result = hand.process(RGB_frame)
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    # for point in hand_landmarks.landmark:
                        # mp_drawing.draw_landmarks(current_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # for id, lm in enumerate(hand_landmarks.landmark):
                    #     #print(id, lm)
                    #     h, w, c = current_frame.shape
                    #     cx, cy = int(lm.x*w), int(lm.y*h)
                    #     # print(id, cx, cy)

                    #     cv2.circle(current_frame, (cx, cy), 15, (139, 0, 0), cv2.FILLED)

                    mp_drawing.draw_landmarks(current_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    fingers = count_fingers(hand_landmarks)
                    finger_count = fingers.count(1)

                    print(fingers)

                    cv2.putText(current_frame, str(finger_count), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 3, (139,0,0), 3)



            # Time and FPS Calculation
            c_time = time.time()
            fps = 1/(c_time-p_time)
            p_time = c_time
             
            # cv2.putText(current_frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 3, (139,0,0), 3)

            cv2.imshow('Frame', current_frame)
    
        if cv2.waitKey(30) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    display_thread = Thread(target=display_frames, daemon=True) # Create a thread for displaying frames
    display_thread.start() # Start the thread
    gunicorn.SERVER_NAME = 'gunicorn'
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
