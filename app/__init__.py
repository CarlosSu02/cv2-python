


import base64
from datetime import datetime
from threading import Thread, Lock
from flask import Flask, Response, redirect, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import numpy as np
import gunicorn
import cv2

from app.routes import public_routes
from app.utils.hand_tracking import hand_tracking
from app.utils.frame_manager import FrameManager
from app.utils.user_manager import UserManager
from app.config.config import current_user

frame_manager = FrameManager()

app = Flask(__name__)
# app.config['SOCKET'] = ''
CORS(app, resources={ r'/*': { 'origins': '*' } })

socketio = SocketIO(app, cors_allowed_origins='*')

# current_frame = None
sid = None
# current_user = UserManager() # Not show error on init app

# '''
@socketio.on('connect')
def connect():
    global sid

    sid = request.sid
    current_user.update_data(request.sid)

    # emit('messages', { 'data': False })
    print(f'New client connected, id: { str(sid) }') 

@socketio.on('disconnect')
def disconnect():
    global sid
    global current_user
    
    print(f'Client disconnected, id: { str(sid) }')
    sid = None
    current_user.reset_data()
    # clean buffer cv2

    # cv2.destroyAllWindows()

@socketio.on('destroy')
def destroy():
    global sid
    global current_user

    print(f'Client disconnected, id: { str(sid) }')
    sid = None
    current_user.reset_data()
    # clean buffer cv2

    # cv2.destroyAllWindows()

@socketio.on('frame')
def handle_frame(data):
    # global current_frame
    img_data = base64.b64decode(data.split(',')[1])
    array = np.frombuffer(img_data, np.uint8) # Convert the image data to a NumPy array
    frame = cv2.imdecode(array, cv2.IMREAD_COLOR) # Decode the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # emit('messages', { 'data': 'hello!' })

    # Detect faces
    # faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # Draw rectangle around the faces
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)

    # Encode the frame in JPEG format
    hand_tracking(frame)
    _, buffer = cv2.imencode('.jpg', frame)

    # Emit the frame to the client
    emit('new-frame', { 'data': base64.b64encode(buffer).decode('utf-8') })

    # frame_manager.update_frame(frame) # Uncomment this line to display the frame

#'''

def init_app ():
    display_thread = Thread(target=frame_manager.display_frames, daemon=True) # Create a thread for displaying frames
    display_thread.start() # Start the thre ad
    gunicorn.SERVER_NAME = 'gunicorn'

    app.register_blueprint(public_routes.main, url_prefix = '/')

    # socketio.run(app, host='0.0.0.0', port=8080, debug=True)

    return  app, socketio

