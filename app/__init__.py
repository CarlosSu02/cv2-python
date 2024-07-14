
from threading import Thread
from flask import Flask
from flask_cors import CORS
import numpy as np
import gunicorn

from app.routes import public_routes
from app.utils.frame_manager import FrameManager
from app.utils.socket_manager import socket_manager, socketio

# Initialize the Flask app
app = Flask(__name__)

# Initialize the CORS extension
CORS(app, resources={ r'/*': { 'origins': '*' } })

frame_manager = FrameManager()

def init_app ():
    display_thread = Thread(target=frame_manager.display_frames, daemon=True) # Create a thread for displaying frames
    display_thread.start() # Start the thre ad
    gunicorn.SERVER_NAME = 'gunicorn'

    socket_manager(app)

    app.register_blueprint(public_routes.main, url_prefix = '/')

    return  app, socketio
