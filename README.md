[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/I4_dFpC1)

## Setup

1. python -m venv .venv
2. source .venv/bin/activate
3. python -m pip install -r requirements.txt

## Task 1

- start with `python image_extractor.py [input_file] -o [output_folder] -wt [width_output] -ht [height_output]`
- clicking with mouse on the four edges of the part of the image you want to crop, wraps the image
- pressing `s` saves the image to the desired location
- pressing `ESC` resets the current selection and/or wrapping

## Task 2

- start with `python ar_game.py -d [webcam_device_id]`
- shows flipped image of your webcam so that playing the game feels more easy
- showing the board with aruco markers in the webcam wraps the image and runs the game
- if the board is not correctly into the webcam, the game pauses
- use your finger or objects (only works if the object has a colour within these boundaries `LOWER = [0,48,80]; UPPER = [20,255,255]`
- the obstacle is to hit the incoming balls with your finger
- the games ends after x seconds and displays the score with an option to restart
- press `ESC` to exit the game any time
- press `SPACE` to restart the game
- FPS display can be toggled by pressing `f`
