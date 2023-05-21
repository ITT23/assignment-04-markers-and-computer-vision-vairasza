import numpy as np
import cv2
from cv2 import Mat

import Config as C

class Detection:

  #https://medium.com/analytics-vidhya/hand-detection-and-finger-counting-using-opencv-python-5b594704eb08
  def __init__(self) -> None:
    self.lower = np.array(C.Detection.LOWER, dtype=np.uint8)
    self.upper = np.array(C.Detection.UPPER, dtype=np.uint8)

  def get_finger(self, frame: Mat) -> tuple[Mat, Mat]:
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinRegion = cv2.inRange(hsv_image, self.lower, self.upper)
    blurred = cv2.blur(skinRegion, (C.Detection.KERNEL_SIZE, C.Detection.KERNEL_SIZE))
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image_contours = cv2.drawContours(frame, contours, -1, C.Color.BLUE, -1)#blue turns red in this case as cv2 uses BGR colour space
    
    return (thresh, image_contours) #we are interested in thresh for collision detection and image_contours to highlight the finger or similar