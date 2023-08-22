#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import time
import argparse

# Initialize face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_face_and_move_mouse(interval_ms, sleep_ms):
    last_mouse_position = pyautogui.position()
    while True:
        current_mouse_position = pyautogui.position()
        
        # Check if the mouse has moved since it was last set
        if current_mouse_position != last_mouse_position:
            print(f"Mouse moved [by user]. Waiting {sleep_ms/1000.0}s")
            time.sleep(sleep_ms / 1000.0)
            print(" Continuing...")
            last_mouse_position = pyautogui.position()
            continue  # Skip the face detection and re-check the mouse position

        # Capture screen
        print("Grabbing screen")
        screenshot = ImageGrab.grab()
        frame = np.array(screenshot)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            # Compute the coordinates for the nose
            nose_x = x + w // 2
            nose_y = y + h // 2
            
            # Move the mouse cursor to the nose position
            pyautogui.moveTo(nose_x, nose_y)
            last_mouse_position = (nose_x, nose_y)  # Update the last mouse position set by the script
            break  # Move to the first face detected
        
        # Wait for the next screen capture
        time.sleep(interval_ms / 1000.0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Move mouse cursor to the face detected on screen.')
    parser.add_argument('-m', '--interval_ms', type=int, default=500, help='Milliseconds between screen captures')
    parser.add_argument('-s', '--sleep_ms', type=int, default=5000, help='Milliseconds to sleep when mouse moved by user')
    args = parser.parse_args()
    
    detect_face_and_move_mouse(args.interval_ms, args.sleep_ms)
