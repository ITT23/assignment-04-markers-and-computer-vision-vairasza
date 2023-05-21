import random

from pyglet.shapes import Circle, Batch

import Config as C

class Ball(Circle):

  def __init__(self, width: int, x:float, y: float, velocity: float, colour: tuple, batch: Batch) -> None:
    self.width = width
    self._radius = random.randint(C.Ball.RADIUS_MIN, C.Ball.RADIUS_MAX)
    super().__init__(x=x, y=y, radius=self._radius, color=colour, batch=batch)
    self.velocity = velocity

  def move(self) -> None:
    '''
      balls passing max width do not longer move because this would lead to an index out of range error in collision detection
    '''
    if self.x < self.width - self.velocity:
      self.x += self.velocity
    else:
      self.visible = False