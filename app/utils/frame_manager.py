
from threading import Lock
import cv2
from app.utils.hand_tracking import hand_tracking

class FrameManager:

    def __init__ (self):
        self.frame = None
        self.frame_lock = Lock()

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

                # Time and FPS Calculation
                # c_time = time.time()
                # fps = 1/(c_time-p_time)
                # p_time = c_time
                    
                # cv2.putText(current_frame, f'FPS: { str(int(fps)) }', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (139,0,0), 3)

                # cv2.imshow('Frame', current_frame) # Uncomment this line to show the frame

            if cv2.waitKey(30) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


