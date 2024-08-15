
from app.utils.user_manager import UserManager
from  app.utils.arduino_manager import ArduinoManager

current_user = UserManager() # Not show error on init app
# arduino = ArduinoManager() # Not show error on init app

arduino = None

try:
    arduino = ArduinoManager()  # Manejar errores al inicializar Arduino
except Exception as e:
    print(f"Error al inicializar Arduino: { e }")

config = {
    'host': '0.0.0.0',
    'port': 8080,
    'debug': True,
}
