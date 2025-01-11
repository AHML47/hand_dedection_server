import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hand
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_raised_fingers(hand_landmarks):
        """Detect raised fingers based on hand landmarks."""
        raised_fingers = []

        fingers_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Little finger tips
        fingers_joints = [6, 10, 14, 18]  # Corresponding joints
        thumb_tip = 4
        thumb_joint = 3

        for i, tip in enumerate(fingers_tips):
            joint = fingers_joints[i]
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[joint].y:
                raised_fingers.append(i + 1)


        if hand_landmarks.landmark[thumb_tip].x > hand_landmarks.landmark[thumb_joint].x:
            raised_fingers.append(0)


        return raised_fingers

    def process_image(self, frame):
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        raised_fingers=[]
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                raised_fingers = self.detect_raised_fingers(hand_landmarks)
        return raised_fingers,frame

