
import cv2
import mediapipe as mp
import cvzone.HandTrackingModule as htm

# from main import arduino
from app.config.config import arduino

# Load the mediapipe hands model
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

# Initialising detector from HandTrackingModule
detector = htm.HandDetector(detectionCon=0.6, maxHands=1)

# Fingers dictionary
fingers = {
    0: 'thumb',
    1: 'index',
    2: 'middle',
    3: 'ring',
    4: 'pinky',
}

# This function is used to track the hand
def hand_tracking(frame):
    # Encode the frame in JPEG format
    hands, _ = detector.findHands(frame)

    if not hands:
        return

    # if hands:
    # Hand Landmarks
    hand = hands[0]
    lm_list = hand['lmList']  # List of 21 Landmark points
    bbox = hand['bbox']  # Bounding box info x,y,w,h
    center = hand['center']  # Center of the hand cx,cy
    
    # Find how many fingers are up
    # fingers = detector.fingersUp(hands[0])
    # fingers_count = fingers.count(1)

    fingers_up = detector.fingersUp(hand)
    fingers_count = fingers_up.count(1)

    show_name_finger(fingers_up, frame)
    # cv2.rectangle(current_frame, (25, 150), (100, 400), (0, 255, 0) , cv2.FILLED)
    # cv2.putText(current_frame, f'{ fingers_count }', (10, 70), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 0), 2)

# This function is used to show the name of the finger
def show_name_finger(fingers_list, current_frame):

    try:

        count = fingers_list.count(1);

        arduino.write(f'{ count }')

        if (count == 0 or (count > 1 and count < 5)):
            # return print(count)
            # arduino.open()
            # arduino.write(f'hi from python { count }'.encode())
            # print(arduino.is_open)
            # arduino.write(f'{ count }'.encode())
            # arduino.close()
            return cv2.putText(current_frame, f'{ count }', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

        if (count == 5):
            return cv2.putText(current_frame, f'all', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        
        return cv2.putText(current_frame, f'{ fingers[fingers_list.index(1)] }', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
    
    except Exception as err:
        print(err)

# arduino.close()

# arduino.close()
