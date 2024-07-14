
from app.utils.user_manager import UserManager

current_user = UserManager() # Not show error on init app

config = {
    'host': '0.0.0.0',
    'port': 8080,
    'debug': True,
}
