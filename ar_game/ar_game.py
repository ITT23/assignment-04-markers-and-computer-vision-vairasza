import sys

import cv2
import numpy as np
import pyglet
from PIL import Image
import cv2.aruco as aruco
from pyglet.math import Vec2
from pyglet.window import Window, FPSDisplay
from argparse import ArgumentParser

'''
TODO:
1 split into game and ar detection
2 make board detection more beautiful
'''

# Define the ArUco dictionary and parameters
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
aruco_params = aruco.DetectorParameters()

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


class Application:

  W_WIDTH = 640
  W_HEIGHT = 480
  NAME = "AR Game"
  COLOR_FPS = (0,0,0,255)

  def __init__(self, device_id: int) -> None:
    self.device_id = device_id
    
    self.video_capture = cv2.VideoCapture(self.device_id)
    #reducing the input video stream greatly increases fps
    #https://stackoverflow.com/a/45605531/13620136
    self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.W_WIDTH)
    self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.W_HEIGHT)
    ##event frame_w = self.video_catpure.get(cv2.CAP_PROP_FRAME_WIDTH) etc. depending on frame rate

    self.window = Window(self.W_WIDTH, self.W_HEIGHT, caption=self.NAME)
    self.fps_display = FPSDisplay(window=self.window, color=self.COLOR_FPS)
    self.on_draw = self.window.event(self.on_draw)

    self._load_aruco_settings()

  def _load_aruco_settings(self) -> None:
    self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    self.aruco_params = aruco.DetectorParameters()

  def run(self) -> None:
    pyglet.app.run()

  #code reference: https://pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
  def _order_points(self, pts: np.ndarray) -> np.ndarray:
    rect = np.zeros((4, 2), dtype = "float32")

    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

  def _get_corners(self, corners) -> None:
    #1 get midpoint by calculating the mid of a rectangle which is just 3 random points
    mid_point_x = (corners[0][0][0][0] + corners[1][0][0][0] + corners[2][0][0][0]) / 3
    mid_point_y = (corners[0][0][0][1] + corners[1][0][0][1] + corners[2][0][0][1]) / 3
    mid = Vec2(mid_point_x, mid_point_y)

    #2 get the closest point of each aruco mark in distance to mid
    point_one = Vec2(corners[0][0][0][0], corners[0][0][0][1])

    for corner in corners[0][0]:
      vec_corner = Vec2(corner[0], corner[1])
      if mid.distance(vec_corner) <= mid.distance(point_one):
        point_one = vec_corner
    
    point_two = Vec2(corners[1][0][0][0], corners[1][0][0][1])

    for corner in corners[1][0]:
      vec_corner = Vec2(corner[0], corner[1])
      if mid.distance(vec_corner) <= mid.distance(point_two):
        point_two = vec_corner

    point_three = Vec2(corners[2][0][0][0], corners[2][0][0][1])

    for corner in corners[2][0]:
      vec_corner = Vec2(corner[0], corner[1])
      if mid.distance(vec_corner) <= mid.distance(point_three):
        point_three = vec_corner
    
    point_four = Vec2(corners[3][0][0][0], corners[3][0][0][1])

    for corner in corners[3][0]:
      vec_corner = Vec2(corner[0], corner[1])
      if mid.distance(vec_corner) <= mid.distance(point_four):
        point_four = vec_corner
    
    #3 return points ordered
    return self._order_points(np.array([(point_one.x, point_one.y), (point_two.x, point_two.y), (point_three.x, point_three.y), (point_four.x, point_four.y)]))

  def on_draw(self) -> None:
    self.window.clear()

    _, frame = self.video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, *_ = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)

    if len(corners) == 4:
      (left_bot, right_bot, right_top, left_top) = self._get_corners(corners)

      #make perspective transformation so that the playground is scaled to window width and height
      points = np.float32(np.array([left_bot, right_bot, right_top, left_top]))

      destination = np.float32(np.array([[0, 0], [self.W_WIDTH, 0], [self.W_WIDTH, self.W_HEIGHT], [0, self.W_HEIGHT]]))

      matrix = cv2.getPerspectiveTransform(points, destination)

      _work_image = cv2.warpPerspective(frame, matrix, (self.W_WIDTH, self.W_HEIGHT), flags=cv2.INTER_LINEAR)
      ##warp until here
      gray_two = cv2.cvtColor(_work_image, cv2.COLOR_BGR2GRAY)

      ### get finger
      _, thresh = cv2.threshold(gray_two, 125, 255, cv2.THRESH_BINARY)
      contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      #extract largest area here and use it as input for game

      rgb_image = cv2.cvtColor(_work_image, cv2.COLOR_BGR2RGB)
      img_contours = cv2.drawContours(rgb_image, contours, -1, (255, 0, 0), 3)


      #flip image so it is easier to play
      _work_image = np.flip(img_contours, axis=1)

      img = cv2glet(_work_image, 'BGR')
      img.blit(0,0,0)

    else:
      #also flip image here so that it is not irritating
      _work_image = np.flip(frame, axis=1)
      img = cv2glet(_work_image, 'BGR')
      img.blit(0,0,0)

    self.fps_display.draw()


if __name__ == "__main__":
  parser = ArgumentParser(prog="AR Game", description="crazy ar game.")
  parser.add_argument("-d", default=0, type=int, help="id of webcam")

  args = parser.parse_args()

  application = Application(device_id=args.d)
  application.run()