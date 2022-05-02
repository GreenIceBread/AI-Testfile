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

  def getMove(self, currentRow, currentColumn):
    move, row, column = self._chooseMove(currentRow, currentColumn)
    self.visited.append((row,column))
    print("This coordinate ", row,column," and this move ",move," will be returned")
    return move,row,column

  def randomMove(self):
    print("Making a random move")
    valid = False
    while not valid:
      row = random.randint(0, self.height - 1)
      column = random.randint(0, self.width - 1)
      if self.topGrid[row][column] == "-" and (row,column) not in self.visited:
        valid = True
      else:
        valid = False
    move = "U"
    return move, row, column

  def addFlag(self, row, column):
    print("Adding this coordinate ",row,column," to the flag stack")
    coord = (row,column)
    if self.stackFlag._hasItem(coord) == False:
      self.stackFlag.push(coord)
    self.stackFlag.showStack()

  def addUncover(self, row, column):
    print("Adding this coordinate ",row,column," to the uncover stack")
    coord = (row,column)
    if self.stackUncover._hasItem(coord) == False: # check that the same coordinate isnt being added twice
      self.stackUncover.push(coord)
    self.stackUncover.showStack()

  def getFlagCoord(self):
    print("Getting coordinate from the flag stack")
    self.stackFlag.peek()
    coord = self.stackFlag.pop()
    row = coord[0]
    column = coord[1]
    move = "F"
    return move, row, column

  def getUncoverCoord(self):
    print("Getting coordinate from the uncover stack")
    self.uncoverStack.peek()
    coord = self.stackUncover.pop()
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
          for offset in self.offsets:
            offsetRow = offset[0] + y
            offsetColumn = offset[1] + x
            if offsetRow in range(0, self.height) and offsetColumn in range(0, self.width):
              if self.topGrid[offsetRow][offsetColumn] in [1,2,3,4,5,6,7,8] and (offsetRow,offsetColumn) not in boundaries:
                boundaries.append((offsetRow,offsetColumn))
    print("The boundaries")
    print(boundaries)
    return boundaries

  def getPossibleCoords(self):
    print("Getting possible coordinates")
    if len(self.possibleCoords) == 0:
      boundaries = self.getBoundaries()
      for coord in boundaries:
        if coord not in self.possibleCoords and coord not in self.visited:
          self.possibleCoords.append(coord)
    print("These are the coordinates which will be checked later")
    print(self.possibleCoords)

  def countFlags(self,row,column):
    countF = 0
    spacesF = []
    for offset in self.offsets:
      offsetRow = offset[0] + row
      offsetColumn = offset[1] + column
      if offsetRow in range(0, self.height) and offsetColumn in range(0, self.width):
        if self.topGrid[offsetRow][offsetColumn] == "F":
          countF += 1
          spacesF.append((offsetRow,offsetColumn))
    print("There are ",countF, " flags in the 3x3 grid")
    print("These are their coordinates", spacesF)
    return countF, spacesF

  def countSpaces(self,row, column):
    countS = 0
    spacesS = []
    for offset in self.offsets:
      offsetRow = offset[0] + row
      offsetColumn = offset[1] + column
      if offsetRow in range(0, self.height) and offsetColumn in range(0, self.width):
        if self.topGrid[offsetRow][offsetColumn] == "-":
          countS += 1
          spacesS.append((offsetRow,offsetColumn))
    print("There are ",countS, " flags in the 3x3 grid")
    print("These are their coordinates", spacesS)
    return countS, spacesS
    
  def _checkMove(self):
    if self.stackFlag._isEmpty() == False:
      move, row, column = self.getFlagCoord()
      return move, row, column
    else: 
      print("Flag stack is empty so check uncover stack")
      if self.stackUncover._isEmpty() == False:
        move, row, column = self.getUncoverCoord()
        return move, row, column 
      else:
        print("Both stacks are empty")
        return " ", 0, 0

  def _chooseMove(self, currentRow, currentColumn):
    move, newRow, newColumn = self._checkMove()
    if move == " ": # if there are no coords in stacks
      self.compare(currentRow,currentColumn)
      move, newRow, newColumn = self._checkMove() # get coord from stack
      if move == " ": # if no coords were added to stacks
        if len(self.possibleCoords) != 0: # if there are possible coords
          move, newRow, newColumn = self._lol()
          print(move,newRow,newColumn)
          return move, newRow, newColumn
        else: # if possible coords is empty
          self.getPossibleCoords() # find boundaries and possible coords
          if len(self.possibleCoords) == 0: # if possible coords is still empty
            move, newRow, newColumn = self.randomMove() # make a random move
            print(move,newRow,newColumn)
            return move, newRow, newColumn
          else: # if there are possible coords
            move, newRow, newColumn = self._lol()
            print(move,newRow,newColumn)
            return move, newRow, newColumn
      else:
        print(move,newRow,newColumn)
        return move, newRow, newColumn
    else:
      print(move,newRow,newColumn)
      return move, newRow, newColumn


  def _lol(self):
    for coord in self.possibleCoords: # cycle through the possible coords
      row = coord[0]
      column = coord[1]
      self.possibleCoords.remove(coord)
      self.compare(row,column) # compare them
    move, newRow, newColumn = self._checkMove() # check if anything has been added to the stacks
    if move == " ":
      move, newRow, newColumn = self.randomMove() # if not then make random move
    else:
      pass
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
      elif countS == 0:
        pass
       # pick a new coordinate to compare
    elif countS == number:
      if countF == 0:
        for i in range(len(spacesS)):
          coord = spacesS[i]
          row = coord[0]
          column = coord[1]
          self.addFlag(row,column)
      elif countF != 0:
        pass
       # pick a new coordinate to compare
    elif countF + countS == number:
      for i in range(len(spacesS)):
        coord = spacesS[i]
        row = coord[0]
        column = coord[1]
        self.addFlag(row,column)

    else:
      pass
     # pick a new coordinate to compare

     
    
      
          
      
    
    

    
  