
from datetime import datetime

class UserManager:
    def __init__(self, sid = None, date = None):
        self.sid = sid
        self.date = date

    def data (self):
        return f'sid: { self.sid }, date: { self.date }'
    
    def update_data (self, sid, date = datetime.now()):
        self.sid = sid
        self.date = date
        return
    
    def reset_data (self):
        self.sid = None
        self.date = None
        return
    
    def res (self):
        return {
            'sid': self.sid,
            'date': self.date
        }
