
import re
from flask import Blueprint, render_template, request

from app.utils.arduino_manager import ArduinoManager
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

@main.get('/admin')
def admin():
    return render_template('./admin/index.html'), 200

@main.get('/video')
def video():
    return render_template('./video/index.html'), 200

@main.get('/led')
def led():
    return render_template('./led/index.html', message = ''), 200

@main.post('/change-states')
def change_led_state():
    state = request.json.get('state')
    # print(state)

    # match state with on or off
    if state is not None and re.search(r'on|off|all|reset', state, re.IGNORECASE):
        # print(arduino)
        try:
            if arduino is None:
                return {
                    'status': 400,
                    'message': 'Arduino no está conectado. Considere desconectar y conectar el Arduino.',
                }, 400
            
            arduino.write(f'{state}\n')
            
            return {
                'status': 200,
                'message': 'Se envió el comando al Arduino correctamente.',
            }, 200
        
        except Exception as e:
            # print(e)
            return {
                'status': 400,
                'message': 'Error al enviar el comando al Arduino. Considere desconectar y conectar el Arduino.',
            }, 400

    return {
        'status': 400,
        'message': 'Estado no válido, debe ser "on" o "off".',
    }, 400

@main.post('/init-arduino')
def init_arduino():
    try:
        global arduino

        if arduino is not None:
            arduino.close()
            arduino = None

        arduino = ArduinoManager() # para inicializar el arduino
        
        return {
            'status': 200,
            'message': 'Arduino inicializado correctamente, si las leda no encienden, considere guardar algún código con extensión .py.',
        }, 200
    
    except Exception as e:
        # print(e)
        return {
            'status': 400,
            'message': 'Error al inicializar el Arduino. Considere desconectar y conectar el Arduino y guardar algun código con extensión .py.',
        }, 400

@main.get('/status')
def status():
    return current_user.res(), 200

@main.delete('/reset-status')
def reset_status():
    
    current_user.reset_data()

    return {
        'status': 200,
        'message': 'Datos de conexión reiniciados.',
    }, 200
