print('Loading camera input')
import cv2
print('Loaded camera input')
print('Loading ai hand detection')
import mediapipe as mp
print('loaded ai hand detection')
import math
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(int(config['Camera']['device_number']))

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
cap.set(cv2.CAP_PROP_FPS, int(config['Camera']['fps_cap']))

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

def calculate_distance_3d(point1, point2):
    try:
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)
    except:
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def get_and_parse_frame():
    begin = time.time()
    ret, frame = cap.read()
    if not ret:
        return "Error: Could not read frame."

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    return results

def get_hand_position(hand_data):
    landmarks_x = [lmk.x for lmk in hand_data.landmark]
    landmarks_y = [lmk.y for lmk in hand_data.landmark]
    landmarks_z = [lmk.z for lmk in hand_data.landmark]

    centroid_x = sum(landmarks_x) / len(landmarks_x)
    centroid_y = sum(landmarks_y) / len(landmarks_y)
    centroid_z = sum(landmarks_z) / len(landmarks_z)

    return centroid_x, centroid_y, centroid_z

def check_for_right_click(hand_data):
    for hand_landmarks in hand_data.multi_hand_landmarks:
        finger0nail = (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
                       hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y,
                       hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].z)
        finger1nail = (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x,
                       hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y,
                       hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].z)

        wrist_position = (hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
                          hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,
                          hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].z)
        bottom_middle = (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x,
                         hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y,
                         hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].z)

        distance_wrist_middle = calculate_distance_3d(wrist_position, bottom_middle)
        distance_thumb_index = calculate_distance_3d(finger0nail, finger1nail)
        distance = round(distance_thumb_index / distance_wrist_middle * 10)
            
        if distance < 3:
            return True
    return False

def check_for_grab(hand_data):
    for hand_landmarks in hand_data.multi_hand_landmarks:
        finger0nail = (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
                       hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y)
        finger1nail = (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x,
                       hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)

        wrist_position = (hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
                          hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)
        bottom_middle = (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x,
                         hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y)

        distance_wrist_middle = calculate_distance_3d(wrist_position, bottom_middle)
        distance_thumb_index = calculate_distance_3d(finger0nail, finger1nail)
        distance = round(distance_thumb_index / distance_wrist_middle * 10)
            
        if distance < 3:
            return hand_landmarks
        
    return False

def check_for_click(hand_data):
    for hand_landmarks in hand_data.multi_hand_landmarks:
        finger0nail = (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
                       hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y)
        finger1nail = (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,
                       hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)

        wrist_position = (hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
                          hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)
        bottom_middle = (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x,
                         hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y)

        distance_wrist_middle = calculate_distance_3d(wrist_position, bottom_middle)
        distance_thumb_index = calculate_distance_3d(finger0nail, finger1nail)
        distance = round(distance_thumb_index / distance_wrist_middle * 10)
            
        if distance < 3:
            return True
        
    return False

def check_for_scroll_click(hand_data):
    for hand_landmarks in hand_data.multi_hand_landmarks:
        finger0nail = (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
                       hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y)
        finger1nail = (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x,
                       hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y)

        wrist_position = (hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
                          hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)
        bottom_middle = (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x,
                         hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y)

        distance_wrist_middle = calculate_distance_3d(wrist_position, bottom_middle)
        distance_thumb_index = calculate_distance_3d(finger0nail, finger1nail)
        distance = round(distance_thumb_index / distance_wrist_middle * 10)
            
        if distance < 3:
            return True
        
    return False