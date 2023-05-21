from pyglet.text import Label

import Config as C

class Menu:
  def __init__(self, width: int, height: int) -> None:
    self.width = width
    self.height = height
    self._game_over_score = Label(text=C.GameOver.TEXT_SCORE, font_name=C.Font.NAME, font_size=C.Font.LARGE, bold=True, color=C.Font.COLOUR, x=C.GameOver.X, y=C.GameOver.Y)

    self._game_over_repeat = Label(text=C.GameOver.TEXT_REPEAT, font_name=C.Font.NAME, font_size=C.Font.LARGE, bold=True, color=C.Font.COLOUR, x=C.GameOver.X, y=C.GameOver.Y)

    self._score = Label(text=C.Game.SCORE_TEXT, font_name=C.Font.NAME, font_size=C.Font.LARGE, bold=True, color=C.Font.COLOUR, x=self.width - C.Game.X_OFFSET, y=self.height - C.Game.Y_OFFSET)

  def show_game_over(self) -> None:
    self._game_over_score.visible = True
    self._game_over_repeat.visible = True

  def hide_game_over(self) -> None:
    self._game_over_score.visible = False
    self._game_over_repeat.visible = False

  def update_game_over(self, score: int=0) -> None:
    self._game_over_score.text = C.GameOver.TEXT_SCORE.replace("XXX", str(score))

    self._game_over_score.x = self.width / 2 - (self._game_over_score.content_width / 2)
    self._game_over_score.y = self.height / 2 - (self._game_over_score.content_height / 2)

    self._game_over_repeat.x = self.width / 2 - (self._game_over_repeat.content_width / 2)
    self._game_over_repeat.y = self.height / 2 - (self._game_over_repeat.content_height / 2) - C.GameOver.REPEAT_OFFSET

    self._game_over_score.draw()
    self._game_over_repeat.draw()

  def show_score(self) -> None:
    self._score.visible = True

  def hide_score(self) -> None:
    self._score.visible = False

  def update_score(self, score: int=0) -> None:
    self._score.text = C.Game.SCORE_TEXT.replace("XXX", str(score))
    self._score.draw()