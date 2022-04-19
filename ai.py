import random

from stack import Stack

class Ai():
  def __init__(self, topGrid, height, width, mines):
    self.stackFlag = Stack(1100)
    self.stackUncover = Stack(1100)
    self.topGrid = topGrid
    self.height = height
    self.width = width
    self.mines = mines
    self.offsets = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    self.boundaries = []
    self.corners = [(1,-1,1,0,0,-1),
           (1,1,1,0,0,1),
           (-1,-1,0,-1,-1,0),
           (-1,1,-1,0,0,1)]

  def getMove(self):
    move,row,column = self._chooseMove()
    return move,row,column

  def randomMove(self):
    row = random.randint(0, self.height)
    column = random.randint(0, self.width)
    move = "U"
    return move, row, column

  def addFlag(self, row, column):
    coord = (row,column)
    self.stackFlag.push(coord)

  def addUncover(self, row, column):
    coord = (row,column)
    self.stackUncover.push(coord)

  def getFlagCoord(self):
    coord = self.stackFlag.pop()
    row = coord[0]
    column = coord[1]
    move = "F"
    return row, column, move

  def getUncoverCoord(self):
    coord = self.uncoverStack.pop()
    row = coord[0]
    column = coord[1]
    move = "U"
    return row, column, move

  def offsetCoord(self, row, column):
    for i in range(len(self.offsets)):
      offset = self.offsets[i]
      offsetRow = offset[0] + row
      offsetColumn = offset[1] + column
      if offsetRow in range(0, self.height) and offsetColumn in range(0, self.width):
        return offsetRow, offsetColumn

  def boundaries(self):
    boundaries = []
    for y in range(self.height):
      for x in range(self.width):
        if self.topGrid[y][x] != " ":
          offsetRow, offsetColumn = self.offsetCoord(y,x)
          if self.topGrid[offsetRow][offsetColumn] in [1,2,3,4,5,6,7,8]:
            boundaries.append((y,x))
            break
    self.boundaries = boundaries

  def countFlags(self,row,column):
    countF = 0
    spacesF = []
    offsetRow, offsetColumn = self.offsetCoord(row,column)
    if self.topGrid[offsetRow][offsetColumn] == "F":
      countF += 1
      spacesF.append((offsetRow,offsetColumn))
    return countF, spacesF

  def countSpaces(self,row, column):
    countS = 0
    spacesS = []
    offsetRow, offsetColumn = self.offsetCoord(row,column)
    if self.topGrid[offsetRow][offsetColumn] == " ":
      countS += 1
      spacesS.append((offsetRow,offsetColumn))
    return countS, spacesS

  def _chooseMove(self):
    if self.stackFlag._isEmpty == False:
      row, column, move = self.getFlagCoord()
    else:
      if self.uncoverStack._isEmpty == False:
        row, column, move = self.getUncoverCoord()
      else:
        self.stuff()

  def stuff(self):
    pass

  def lol(self,row, column):
    number = self.topGrid[row][column]
    countF, spacesF = self.countFlags(row, column)
    countS, spacesS = self.countSpaces(row,column)
    if countS == number:
      if countF == 0:
        for i in range(len(spacesS)):
          coord = spacesS[i]
          row = coord[0]
          column = coord[1]
          self.addFlag(row,column)
      elif countF != 0:
        pass
    elif countF == number:
      if countS != 0:
        for i in range(len(spacesS)):
          coord = spacesS[i]
          row = coord[0]
      
          
      
    
    

    
  