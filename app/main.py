
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from jinja2 import Template
import uvicorn
import socketio
from fastapi.templating import Jinja2Templates

app = FastAPI();

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
socket_app = socketio.ASGIApp(sio)

app.mount('/socket.io', socket_app)

templates = Jinja2Templates(directory='app/templates')

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

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True, workers=2)
