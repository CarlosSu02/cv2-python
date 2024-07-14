
import base64
from flask import request
from flask_socketio import SocketIO, emit
import numpy as np
import cv2

from app.utils.hand_tracking import hand_tracking
from app.utils.frame_manager import FrameManager
from app.config.config import current_user

frame_manager = FrameManager()
sid = None

# Initialize the socketio instance
socketio = SocketIO(cors_allowed_origins="*")

def socket_manager (app):

    socketio.init_app(app) # https://flask-socketio.readthedocs.io/en/latest/api.html

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
        
        print(f'Client disconnected, id: { str(sid) }')
        sid = None
        current_user.reset_data()

    @socketio.on('destroy')
    def destroy():
        global sid

        print(f'Client disconnected, id: { str(sid) }')
        sid = None
        current_user.reset_data()

    @socketio.on('frame')
    def handle_frame(data):
        # global current_frame
        img_data = base64.b64decode(data.split(',')[1])
        array = np.frombuffer(img_data, np.uint8) # Convert the image data to a NumPy array
        frame = cv2.imdecode(array, cv2.IMREAD_COLOR) # Decode the image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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
