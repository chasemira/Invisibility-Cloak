# Description: This script creates an "invisibility cloak" effect using OpenCV.
#              It captures the background and then replaces a specified color 
#              (in this case, blue) in the video feed with the captured background,
#              making it appear as if the object of that color is invisible.
# Author: Jasleen Kaur 
# Date: August 2024


import cv2 # openCV library for computer vision tasks 
import numpy as np # NumPy library for numerical operations 
import time # time library for sleep functionality


# function to capture the background by taking multiple frames and computing their median
def createBackground(cap, numFrames=30):
    print("Capturing background. Please move out of frame.")
    backgrounds = []
    for i in range(numFrames):
        # capture a frame from the camera 
        ret, frame = cap.read()
        if ret:
            # add the captured frame to the backgrouns list 
            backgrounds.append(frame)
        else:
            print(f"Warning: Could not read frame {i+1}/{numFrames}")
        # wait for a short period before capturing the next frame 
        time.sleep(0.1)
    if backgrounds:
        # compute the median of the captured frames to create the background 
        return np.median(backgrounds, axis=0).astype(np.uint8)
    else:
        raise ValueError("Could not capture any frames for background")

# function to create a mask for the specified colour range in the frame
def createMask(frame, lower_color, upper_color):
    # convert the frame from BGR to HSV colour spce 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # create a mask for the specified colour range 
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # perform morophological opening to remove noise 
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    # perform morophological dialtion to fill gaps 
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)
    return mask

# function to apply the cloak effect by combining the foreground and background based on the mask 
def applyCloakEffect(frame, mask, background):
    # invert the mask 
    mask_inv = cv2.bitwise_not(mask)
    # extract the foreground (non-cloak area) from the frame
    fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    # extract the background (cloak area) from the background image 
    bg = cv2.bitwise_and(background, background, mask=mask)
    # combine the foreground and background to create the final output 
    return cv2.add(fg, bg)

def main():
    print("OpenCV version:", cv2.__version__)

    # open the default camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    try:
        # capture the background 
        background = createBackground(cap)
    except ValueError as e:
        # print an error message if background capture failed 
        print(f"Error: {e}")
        # release the camera 
        cap.release()
        return

    # define the lower bound for the blue colour in HSV
    lowerBlue = np.array([90, 50, 50])
    # define the upper bound for the blue colour in HSV
    upperBlue = np.array([130, 255, 255])

    print("Starting main loop. Press 'q' to quit.")
    while True:
        # capture a frame from the camera 
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            # wait for a short period before trying again
            time.sleep(1)
            continue
        
        # Flip the frame horizontally, so it is not inverted 
        frame = cv2.flip(frame, 1)
        # create a mask for the blue colour 
        mask = createMask(frame, lowerBlue, upperBlue)
        # apply the cloak effect 
        result = applyCloakEffect(frame, mask, background)

        # desplay the result 
        cv2.imshow('Invisible Cloak', result)

        # exit the loop if 'q' is pressed 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
