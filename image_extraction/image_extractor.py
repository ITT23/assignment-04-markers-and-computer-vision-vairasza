import os,time
from argparse import ArgumentParser, ArgumentTypeError

import cv2
from cv2 import Mat
import numpy as np


class ImageExtractor:

  NAME = "Image Extractor"
  CURR_DIR = os.path.dirname(__file__)
  NUM_MAX_CORNERS = 4
  WAIT_TIME = 1
  CIRCLE_RADIUS = 5
  CIRCLE_COLOUR = (255,0,0)
  CIRCLE_THICKNESS = -1

  def __init__(self, input_file: str, output_path: str, width: int, height: int) -> None:
    self.input_file = input_file
    self.output_path = output_path.removeprefix("./") #removing ./ to avoid misshaped paths due to os.path.join

    self.width = width
    self.height = height

    self._check_paths()
    self.file_name = os.path.basename(self.input_file)

    self._original_image = self._load_image()
    self._work_image = self._original_image.copy()
    self._corners = []

  def _check_paths(self) -> None:
    if not os.path.isfile(self.input_file) and not os.path.isfile(os.path.join(self.CURR_DIR, self.input_file)):
      raise FileNotFoundError(f"No such file: {self.input_file}")

    elif not os.path.isdir(self.output_path) and not os.path.isdir(os.path.join(self.CURR_DIR, self.output_path)):
      raise FileNotFoundError(f"No such directory: {self.output_path}")

  def _load_image(self) -> Mat:
    image = cv2.imread(self.input_file)

    if not self.width:
      self.width = image.shape[1]
    if not self.height:
      self.height = image.shape[0]

    return image

  #code reference: https://pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
  #according to this paper: https://www.researchgate.net/publication/282446068_Automatic_chessboard_corner_detection_method
  def _order_points(self, pts: np.ndarray) -> np.ndarray:
    rect = np.zeros((4, 2), dtype = "float32")

    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

  def _change_perspective(self) -> None:
    (left_bot, right_bot, right_top, left_top) = self._order_points(np.array(self._corners))

    points = np.float32(np.array([left_bot, right_bot, right_top, left_top]))

    destination = np.float32(np.array([[0, 0], [self.width, 0], [self.width, self.height], [0, self.height]]))

    matrix = cv2.getPerspectiveTransform(points, destination)
    self._work_image = cv2.warpPerspective(self._original_image, matrix, (self.width, self.height), flags=cv2.INTER_LINEAR)

    self._corners.clear()

  def _mouse_callback(self, event: any, x: int, y: int, *_) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
      point = (x,y)
      self._corners.append(point)   
      self._work_image = cv2.circle(self._work_image, point, self.CIRCLE_RADIUS, self.CIRCLE_COLOUR, self.CIRCLE_THICKNESS)
      
      if len(self._corners) == self.NUM_MAX_CORNERS:
        self._change_perspective()

      cv2.imshow(self.NAME, self._work_image)

  def _reset(self) -> None:
    self._work_image = self._original_image.copy()
    cv2.imshow(self.NAME, self._work_image)
    self._corners.clear()

  def run(self) -> None:
    cv2.namedWindow(self.NAME)
    cv2.setMouseCallback(self.NAME, self._mouse_callback) #imshow must be called before setting mouse callback else there are no events

    while True:    
      cv2.imshow(self.NAME, self._work_image)  
      key = cv2.waitKey(self.WAIT_TIME)

      #reset state
      if key == 27: #27 is ESC key
        self._reset()

      #save image to dest location
      elif key == ord("s"):
        if cv2.imwrite(os.path.join(self.output_path, self.file_name), self._work_image):
          print("image successfully saved")
        else:
          print("there was an error writing the image.")

        break

      #exit application
      elif key == ord("0"):
        break
    
    cv2.destroyAllWindows()

def check_positive_int(value) -> bool:
  try:
    int_val = int(value)
    if int_val < 0:
      raise ArgumentTypeError(f"{value} is not a positive integer.")
    return int_val
  except Exception:
    raise ArgumentTypeError(f"{value} is not a positive integer.")

if __name__ == "__main__":
  parser = ArgumentParser(prog=f"{ImageExtractor.NAME}", description="Perform perspective transformation with open cv.")
  parser.add_argument("input_file", type=str, help="absolute or relative path to an input file of type image.")
  parser.add_argument("-o", default="output", type=str, help="absolute or relative path to an output folder. default to current folder. relative without trailing ./")
  parser.add_argument("-wt", type=check_positive_int, help="width of output image. default to source width.")
  parser.add_argument("-ht", type=check_positive_int, help="height of output image. default to source height.")

  args = parser.parse_args()

  image_extractor = ImageExtractor(args.input_file, args.o, args.wt, args.ht)
  image_extractor.run()
