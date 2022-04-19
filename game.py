import random
import time

from ai import Ai
from board import Board



class PlayGame:
  def __init__(self):
    self.height = 8 
    self.width = 10
    self.mines = 13
    self.aiBoard = Board(self.mines, self.height, self.width, [])
    self.ai = Ai(self.aiBoard.topGrid, self.height, self.width, self.mines)
    self._game()

  def _game(self):
    self.aiBoard.showGrid(self.aiBoard.topGrid)
    self.aiBoard.showGrid(self.aiBoard.dataGrid)
    run = True
    end = False
    move, row, column = self.ai.getMove()
    if row in range(0, self.height) and column in range(0, self.width):
      end, win = self.move(move, row, column)
      if end == False:
        if win == True:
          self._win()
          run = False
      elif end == True:
        self._gameover()
        run = False
    while run:
      self.aiBoard.showGrid(self.aiBoard.topGrid)
      self.aiBoard.showGrid(self.aiBoard.dataGrid)

      while True:
        move, row, column = self.ai.getMove()
        if row in range(0, self.height) and column in range(0, self. width):
          break
        else:
          True
      end, win = self.move(move, row, column)
      if end == False:
        if win == True:
          self._win()
          run = False
      elif end == True:
        self._gameover()
        run = False

  def _win(self):
    print("AI WON")


  def _gameover(self):
    print("AI LOST")