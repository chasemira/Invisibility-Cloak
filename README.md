# Invisible Cloak Using OpenCV
## Description
This project is inspired by the "Invisibility Cloak" from Harry Potter. It uses computer vision techniques to make a specific color in a video feed (in this case, blue) invisible by replacing it with a previously captured background.

## How It Works
- The program captures the background before you enter the frame.
- When you hold up a blue cloth (or any other object that matches the specified color range), the program replaces that color in the video feed with the captured background, making it appear as though the object is invisible.

## Features
- Captures and averages multiple frames to create a stable background.
- Uses color detection to identify the specified color in the video feed.
- Applies a mask to separate the foreground and background, then combines them to create the invisibility effect.

## Requirements
- Python 3.x
- OpenCV (cv2) library
- NumPy library

## Usage
- Ensure you have a webcam connected.
- Run the script, and the program will start capturing the background.
- After the background is captured, move into the frame with a blue object to see the invisibility effect in action.
- Press q to quit the program.
