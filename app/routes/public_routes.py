
import re
from flask import Blueprint, render_template, request

from app.utils.user_manager import UserManager
from app.config.config import current_user
from app.config.config import arduino

main = Blueprint('public_blueprint', __name__)

@main.get('/')
def index():
    # return {
    #     'message': 'May the force be with you!',
    # }, 200
    return render_template('index.html'), 200

@main.get('/video')
def video():
    return render_template('./video/index.html'), 200

@main.get('/led')
def led():
    state = request.args.get('state')
    print(state)

    # match state with on or off
    if state is not None and re.search(r'on|off', state, re.IGNORECASE):
        if arduino is None:
            return render_template('./led/index.html', message = 'Arduino no está conectado'), 200
            
        arduino.write(f'{state}\n')
        # return render_template('./led/index.html', message = ''), 200

    return render_template('./led/index.html', message = ''), 200

@main.get('/led?led=<led>') 
def led_managment(led):
    print(led)
    # return render_template('led.html', led = led), 200

@main.get('/status')
def status():
    return current_user.res(), 200
