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


  def _game(self):
    self.aiBoard.showGrid(self.aiBoard.topGrid)
    self.aiBoard.showGrid(self.aiBoard.dataGrid)
    print(self.aiBoard.dataGrid)
    run = True
    end = False
    # first move which is always random
    move, firstRow, firstColumn = self.ai.randomMove()
    if firstRow in range(0, self.height) and firstColumn in range(0, self.width):
      end, win = self.move(move, firstRow, firstColumn)
      if end == False:
        if win == True:
          self._win()
          run = False
      elif end == True:
        self._gameover()
        run = True
    print(move, firstRow, firstColumn)
    currentRow = firstRow
    currentColumn = firstColumn
    while run:
      self.aiBoard.showGrid(self.aiBoard.topGrid)
      #self.aiBoard.showGrid(self.aiBoard.dataGrid)
      while True:
        move, row, column = self.ai.getMove(currentRow, currentColumn)
        currentRow = row
        currentColumn = column
        if row in range(0, self.height) and column in range(0, self. width):
          break
        else:
          True
      print(move, row, column)
      end, win = self.move(move, row, column)
      if end == False:
        if win == True:
          self._win()
          run = False
      elif end == True:
        self._gameover()
        run = False

  def move(self, move, row, column):
    if move == "F":
      end, win = self.aiBoard.placeFlag(row, column)
    elif move == "U":
      end, win = self.aiBoard.uncover(row, column)
    return end, win

  
  def _win(self):
    print("AI WON")
    self.aiBoard.showGrid(self.aiBoard.dataGrid)

  def _gameover(self):
    print("AI LOST")
    self.aiBoard.showGrid(self.aiBoard.dataGrid)
 
    