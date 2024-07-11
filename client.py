from flask import Flask, render_template
from flask_socketio import SocketIO
import numpy as np
import cv2
import base64
from threading import Thread

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

current_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('frame') # This decorator is used to receive data from the client
def handle_frame(data):
    global current_frame
    img_data = base64.b64decode(data.split(',')[1])
    array = np.frombuffer(img_data, np.uint8) # Convert the image data to a NumPy array
    frame = cv2.imdecode(array, cv2.IMREAD_COLOR) # Decode the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_frame = gray

def display_frames():
    global current_frame
    while True:
        if current_frame is not None:
            cv2.imshow('Frame', current_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

if __name__ == '__main__':
    display_thread = Thread(target=display_frames) # Create a thread for displaying frames
    display_thread.start() # Start the thread
    socketio.run(app, host='0.0.0.0', port=80)
