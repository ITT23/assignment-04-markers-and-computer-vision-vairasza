from typing import Union

import numpy as np
import cv2
from cv2 import Mat
import cv2.aruco as aruco
from pyglet.math import Vec2
import pyglet
from PIL import Image

import Config as C

# converts OpenCV image to PIL image and then to pyglet texture
# https://gist.github.com/nkymut/1cb40ea6ae4de0cf9ded7332f1ca0d55
def cv2glet(img,fmt):
    '''Assumes image is in BGR color space. Returns a pyimg o1bject'''
    if fmt == 'GRAY':
      rows, cols = img.shape
      channels = 1
    else:
      rows, cols, channels = img.shape

    raw_img = Image.fromarray(img).tobytes()

    top_to_bottom_flag = -1
    bytes_per_row = channels*cols
    pyimg = pyglet.image.ImageData(width=cols, 
                                   height=rows, 
                                   fmt=fmt, 
                                   data=raw_img, 
                                   pitch=top_to_bottom_flag*bytes_per_row)
    return pyimg

#code reference: https://pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
def order_points(pts: np.ndarray) -> np.ndarray:
  rect = np.zeros((4, 2), dtype = "float32")

  s = pts.sum(axis = 1)
  rect[0] = pts[np.argmin(s)]
  rect[2] = pts[np.argmax(s)]

  diff = np.diff(pts, axis = 1)
  rect[1] = pts[np.argmin(diff)]
  rect[3] = pts[np.argmax(diff)]

  return rect

def get_vec_closest_mid(corners: Mat, mid: Vec2) -> Vec2:
  closest_point = Vec2(corners[0][0], corners[0][1])

  for corner in corners:
    vec_corner = Vec2(corner[0], corner[1])
    if mid.distance(vec_corner) <= mid.distance(closest_point):
      closest_point = vec_corner
  
  return closest_point

def get_corners(corners) -> None:
  #1 get midpoint by calculating the mid of a rectangle which is just 3 random points
  mid_point_x = (corners[0][0][0][0] + corners[1][0][0][0] + corners[2][0][0][0]) / 3
  mid_point_y = (corners[0][0][0][1] + corners[1][0][0][1] + corners[2][0][0][1]) / 3
  mid = Vec2(mid_point_x, mid_point_y)

  #2 get the closest point of each aruco mark in distance to mid
  point_one = get_vec_closest_mid(corners[0][0], mid)
  point_two = get_vec_closest_mid(corners[1][0], mid)
  point_three = get_vec_closest_mid(corners[2][0], mid)
  point_four = get_vec_closest_mid(corners[3][0], mid)

  #3 return points ordered
  return order_points(np.array([(point_one.x, point_one.y), (point_two.x, point_two.y), (point_three.x, point_three.y), (point_four.x, point_four.y)]))


class Display:
  def __init__(self, device_id: int) -> None:  
    self._video_capture = cv2.VideoCapture(device_id)
    #force the webcam image to a smaller size to improve FPS
    self._video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, C.Window.WIDTH)
    self._video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, C.Window.HEIGHT)
    self.capture_width = int(self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    self.capture_height = int(self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    self._aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    self._aruco_params = aruco.DetectorParameters()

  def next_image(self) -> tuple[bool, Union[Mat, None]]:
    '''
      returns true if four arcuo marker have been detected, and also returns a transformed image.
      returns false if not four aruco markers have been detected, and also returns the raw webcam image.
    '''
    _, work_image = self._video_capture.read()

    gray = cv2.cvtColor(work_image, cv2.COLOR_BGR2GRAY)
    corners, *_ = aruco.detectMarkers(gray, self._aruco_dict, parameters=self._aruco_params)

    if len(corners) == C.Game.CORNERS_NUM:
      #calculate the point of the marker which is closest to mid so the marker is not part of the game board.
      (left_bot, right_bot, right_top, left_top) = get_corners(corners)

      #make perspective transformation so that the playground is scaled to window width and height
      points = np.float32(np.array([left_bot, right_bot, right_top, left_top]))

      destination = np.float32(np.array([[0, 0], [self.capture_width, 0], [self.capture_width, self.capture_height], [0, self.capture_height]]))

      matrix = cv2.getPerspectiveTransform(points, destination)

      warp_image = cv2.warpPerspective(work_image, matrix, (self.capture_width, self.capture_height), flags=cv2.INTER_LINEAR)

      return (True, warp_image)

    else:
      return (False, work_image)
