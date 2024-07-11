
import base64
from threading import Thread
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import numpy as np
import uvicorn
import socketio
from fastapi.templating import Jinja2Templates
import cv2

app = FastAPI();

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
socket_app = socketio.ASGIApp(sio)

app.mount('/socket.io', socket_app)

templates = Jinja2Templates(directory='app/templates')

current_frame = None

@app.get('/', response_class=HTMLResponse)
async def root(req:Request):
    # return { 'message': 'Hello strange!!' }
    return templates.TemplateResponse('index.html', context={ 'request': req })

@sio.on('connect')
async def connect(sid, env):
    print(f'New client connected, id: {str(sid)}') 

@sio.on('disconnect')
async def disconnect(sid):
    print(f'Client disconnected, id: {str(sid)}') 

@sio.on('frame')
async def handle_frame(sid, data):
    global current_frame
    img_data = base64.b64decode(data.split(',')[1])
    array = np.frombuffer(img_data, np.uint8) # Convert the image data to a NumPy array
    frame = cv2.imdecode(array, cv2.IMREAD_COLOR) # Decode the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_frame = gray
    print(f"Received data: {data[:100]}...") 

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
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True, workers=2)
