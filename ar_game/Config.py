class Font:
  NAME = "Verdana"
  SMALL = 15
  LARGE = 24
  XLARGE = 56
  COLOUR = (0,0,0,255)

class Window:
  WIDTH = 640
  HEIGHT = 480

class GameOver:
  TEXT_SCORE = "You made a score of XXX!"
  TEXT_REPEAT = "Press SPACE to restart the game!"
  X = 730
  Y = 350
  REPEAT_OFFSET = 50

class Game:
  NAME = "AR Game"
  SCORE_TEXT = "SCORE: XXX"
  X_OFFSET = 200
  Y_OFFSET = 50
  CORNERS_NUM = 4
  GAME_OVER_TIME = 20 #seconds

class Color:
  GREEN = (0,168,107,255)
  YELLOW = (255,255,0,255)
  BLUE = (0,0,255,255)
  LILAC = (198,161,207,255)
  ORANGE = (250,70,22,255)
  GRAY = (140,146,172,255)
  LIST = [GREEN, YELLOW, BLUE, LILAC, ORANGE, GRAY]

class Ball:
  RADIUS_MIN = 10
  RADIUS_MAX = 50
  START_X = 10
  VELOCITY_MIN = 5
  VELOCITY_MAX = 25

class Detection:
  KERNEL_SIZE = 3
  LOWER = [0,48,80]
  UPPER = [20,255,255]