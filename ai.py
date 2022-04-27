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
    self.corners = [(1,-1,1,0,0,-1),
           (1,1,1,0,0,1),
           (-1,-1,0,-1,-1,0),
           (-1,1,-1,0,0,1)]
    self.visited = []
    self.possibleCoords = []
    #self.boundaries = self.getBoundaries()

  def getMove(self, currentRow, currentColumn):
    move, row, column = self._chooseMove(currentRow, currentColumn)
    self.visited.append((row,column))
    return move,row,column

  def randomMove(self):
    valid = False
    while not valid:
      row = random.randint(0, self.height - 1)
      column = random.randint(0, self.width - 1)
      if self.topGrid[row][column] == "-":
        valid = True
      else:
        valid = False
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
    return move, row, column

  def getUncoverCoord(self):
    coord = self.uncoverStack.pop()
    row = coord[0]
    column = coord[1]
    move = "U"
    return move, row, column

  def offsetCoord(self, row, column):
    for offset in self.offsets:
      offsetRow = offset[0] + row
      offsetColumn = offset[1] + column
      if offsetRow in range(0, self.height) and offsetColumn in range(0, self.width):
        return offsetRow, offsetColumn

  def getBoundaries(self):
    boundaries = []
    for y in range(self.height):
      for x in range(self.width):
        if self.topGrid[y][x] == " ":
          offsetRow, offsetColumn = self.offsetCoord(y,x)
          if self.topGrid[offsetRow][offsetColumn] in [1,2,3,4,5,6,7,8]:
            if (offsetRow,offsetColumn) not in boundaries:
              boundaries.append((offsetRow,offsetColumn))
            
    return boundaries

  def getPossibleCoords(self):
    row = 0
    column = 0
    boundaries = self.getBoundaries()
    for coord in boundaries:
      if coord not in self.possibleCoords and coord not in self.visited:
        self.possibleCoords.append(coord)
    if len(self.possibleCoords) != 0:
      coord = self.possibleCoords[-1]
      self.possibleCoords.remove(coord)
      row = coord[0]
      column = coord[1]
      return row, column
    else:
      row = -1
      column = -1
      return row, column

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
    
  def _checkMove(self):
    if self.stackFlag._isEmpty == False:
      move, row, column = self.getFlagCoord()
      return move, row, column
    else:
      if self.stackUncover._isEmpty == False:
        move, row, column = self.getUncoverCoord()
        return move, row, column 
      else:
        return " ", 0, 0

  def _chooseMove(self, currentRow, currentColumn):
    move, newRow, newColumn = self._checkMove()
    if move == " ":
      found = self.compare(currentRow,currentColumn)
      if found == True:
        move, newRow, newColumn = self._checkMove()
        return move, newRow, newColumn
      elif found == False:
        newRow, newColumn = self.getPossibleCoords()
        if newRow == -1: # if the get possible coords is empty
          move, newRow, newColumn = self.randomMove()
          return move, newRow, newColumn
        else:
          for i in range(len(self.possibleCoords)):
            found = self.compare(currentRow, currentColumn)
          if found == True:
            move, newRow, newColumn = self._checkMove()
            return move, newRow, newColumn
    elif move != " ":
      return move, newRow, newColumn
      
  def compare(self,row, column):
    number = self.topGrid[row][column]
    countF, spacesF = self.countFlags(row, column)
    countS, spacesS = self.countSpaces(row,column)
    if countF == number:
      if countS != 0:
        for i in range(len(spacesS)):
          coord = spacesS[i]
          row = coord[0]
          column = coord[1]
          self.addUncover(row,column)
          found = True
          return found
      elif countS == 0:
        found = False
        return found
    elif countS == number:
      if countF == 0:
        for i in range(len(spacesS)):
          coord = spacesS[i]
          row = coord[0]
          column = coord[1]
          self.addFlag(row,column)
          found = True
          return found
      elif countF != 0:
        found = False
        return found
    elif countF + countS == number:
      for i in range(len(spacesS)):
        coord = spacesS[i]
        row = coord[0]
        column = coord[1]
        self.addFlag(row,column)
        found = True
        return found
    else:
      found = False
      return found
      #if there are no coords to add to the stack then pick a new possible coordinate
    
    
      
          
      
    
    

    
  