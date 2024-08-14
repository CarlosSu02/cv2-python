
import re
from flask import Blueprint, render_template, request

from app.utils.user_manager import UserManager
from app.config.config import current_user
from app.config.config import arduino

main = Blueprint('public_blueprint', __name__)

@main.get('/')
def index():
    return {
        'message': 'May the force be with you!',
    }, 200

@main.get('/video')
def video():
    return render_template('index3.html'), 200

@main.get('/led')
def led():
    state = request.args.get('state')
    print(state)

    # match state with on or off
    if re.search(r'on|off', state, re.IGNORECASE):
        if arduino:
            arduino.write(f'{state}\n')
            print('match')

    return render_template('led.html', active = state), 200

@main.get('/led?led=<led>') 
def led_managment(led):
    print(led)
    # return render_template('led.html', led = led), 200

@main.get('/status')
def status():
    return current_user.res(), 200
