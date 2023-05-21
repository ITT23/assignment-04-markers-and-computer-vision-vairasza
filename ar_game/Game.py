import random

from pyglet.shapes import Batch
from cv2 import Mat
import pyglet

from Ball import Ball
from Detection import Detection
from AppState import AppState
import Config as C

class Game:
  def __init__(self, width: int, height: int) -> None:
    self.width = width
    self.height = height
    self.batch = Batch()
    self.detection = Detection()
    self.color_list = C.Color.LIST

  def _create_ball(self, *_) -> None:
    colour = random.choice(self.color_list)
    y = random.randint(C.Ball.RADIUS_MAX * 2, self.height - C.Ball.RADIUS_MAX * 2)
    velocity = random.randint(C.Ball.VELOCITY_MIN, C.Ball.VELOCITY_MAX)

    ball = Ball(width=self.width, x=C.Ball.START_X, y=y, velocity=velocity, colour=colour, batch=self.batch)

    self.balls.append(ball)

  def _end_game(self, *_) -> None:
    self.state = AppState.END
      
  def init(self) -> None:
    self.balls = []
    self.score = 0
    self.state = AppState.START

    pyglet.clock.unschedule(self._create_ball)
    pyglet.clock.schedule_interval(self._create_ball, 1) #create a randomly assigned ball every 1 second
    pyglet.clock.schedule_once(self._end_game, C.Game.GAME_OVER_TIME) #automatically end the game after x seconds

  def run(self, thresh: Mat) -> None:
    for ball in self.balls:
      #code reference: https://github.com/ITT23/assignment-04-markers-and-computer-vision-tina-e/blob/master/ar_game/Ball.py
      hit = thresh[int(self.height - ball.y)][int(ball.x)]
      
      if hit:
        self.score += 1
        ball.delete()
        self.balls.remove(ball)
      
      else:
        ball.move()

    self.batch.draw()
