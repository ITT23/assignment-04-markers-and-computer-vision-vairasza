from argparse import ArgumentParser

import numpy as np
import pyglet
from pyglet.window import key, Window, FPSDisplay

from Display import Display, cv2glet
from Detection import Detection
from Game import Game
from Menu import Menu
import Config as C
from AppState import AppState

class Application:

  def __init__(self, device_id: int) -> None:
    self.device_id = device_id

    self.display = Display(self.device_id)
    self.window_width = self.display.capture_width
    self.window_height = self.display.capture_height

    self.window = Window(self.window_width, self.window_height, caption=C.Game.NAME)
    self.fps_display = FPSDisplay(window=self.window, color=C.Font.COLOUR)
    self.on_draw = self.window.event(self.on_draw)
    self.on_key_press = self.window.event(self.on_key_press)

    self.game = Game(width=self.window_width, height=self.window_height)
    self.game.init()
    self.app_state = AppState.START
    self.menu = Menu(width=self.window_width, height=self.window_height)
    self.detection = Detection()

  def run(self) -> None:
    pyglet.app.run()

  def on_draw(self) -> None:
    self.window.clear()

    is_warped, image = self.display.next_image()
    if is_warped and self.game.state == AppState.START: #finger detection, game rendering etc. only happens when all aruco markers were detected
      (thresh, image) = self.detection.get_finger(image)
      thresh = np.flip(thresh, axis=1)

    image = np.flip(image, axis=1) #flip image so it feels more natural
    img = cv2glet(image, 'BGR')
    img.blit(0,0,0)
    
    self.fps_display.draw()
    
    if self.game.state == AppState.START:
      if is_warped:
        self.game.run(thresh)
      self.menu.hide_game_over()
      self.menu.show_score()
      self.menu.update_score(self.game.score)

    elif self.game.state == AppState.END:
      self.menu.hide_score()
      self.menu.show_game_over()
      self.menu.update_game_over(self.game.score)
      

  def on_key_press(self, symbol, _) -> None:
    if symbol == key.SPACE:
      self.game.init() #restarts the game

    elif symbol == key.ESCAPE:
      pyglet.app.exit()

if __name__ == "__main__":
  parser = ArgumentParser(prog="AR Game", description="crazy ar game.")
  parser.add_argument("-d", default=0, type=int, help="id of webcam")

  args = parser.parse_args()

  application = Application(device_id=args.d)

  application.run()