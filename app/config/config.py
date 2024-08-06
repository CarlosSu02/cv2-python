
from app.utils.user_manager import UserManager
from  app.utils.arduino_manager import ArduinoManager

current_user = UserManager() # Not show error on init app
arduino = ArduinoManager() # Not show error on init app

config = {
    'host': '0.0.0.0',
    'port': 8080,
    'debug': True,
}
