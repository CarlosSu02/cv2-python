
from threading import Lock
import cv2
from app.utils.hand_tracking import hand_tracking

class FrameManager:

    def __init__ (self):
        self.frame = None
        self.frame_lock = Lock() # Lock the frame to avoid, en español, esto es para evitar que se corrompa el frame

    def get_frame (self):
        return self.frame

    def update_frame (self, frame):
        with self.frame_lock:
            self.frame = frame
            return frame
    
    def display_frames (self):
        # print type current_frame
        while True:

            with self.frame_lock:
                current_frame = self.get_frame()
                
            if current_frame is not None:
                hand_tracking(current_frame)
            
            if cv2.waitKey(30) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
