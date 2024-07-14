
from flask import Blueprint, render_template, request

from app.utils.user_manager import UserManager
from app.config.config import current_user

main = Blueprint('public_blueprint', __name__)

@main.get('/')
def index():
    return {
        'message': 'May the force be with you!',
    }, 200

@main.get('/video')
def video():
    # return { 'message': 'Hello strange!!' }
    return render_template('index2.html'), 200
    # return redirect('https://google.com', code=302)

@main.get('/status')
def status():
    # print(current_user.res())
    return current_user.res(), 200
