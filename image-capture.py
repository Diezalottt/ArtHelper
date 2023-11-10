import cv2
import time

# Define the function to capture an image from the webcam
def capture_image():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        raise ValueError("Could not open webcam")

    # Capture a single frame
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        raise ValueError("Could not read frame")

    # Save the captured frame to disk
    cv2.imwrite("/mnt/data/captured_image.jpg", frame)
    
    # Release the webcam
    cap.release()

# Call the function to capture the image
capture_image()