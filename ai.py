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
    if self.topGrid[row][column] != "-":
      move, row, column = self._chooseMove(currentRow, currentColumn)
    print("These are visited")
    print(self.visited)
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
    self.stackUncover.peek()
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

  def hehe(self):
    stuff = []
    for y in range(self.height):
      for x in range(self.width):
        if self.topGrid[y][x] in [1,2,3,4,5,6,7,8] and (y,x)not in self.visited:
          stuff.append((y,x))
    print("The stuff")
    print(stuff)
    return stuff

  def getBoundaries(self):
    boundaries = []
    for y in range(self.height):
      for x in range(self.width):
        if self.topGrid[y][x] == " ":
          for offset in self.offsets:
            offsetRow = offset[0] + y
            offsetColumn = offset[1] + x
            if offsetRow in range(0, self.height) and offsetColumn in range(0, self.width):
              if self.topGrid[offsetRow][offsetColumn] in [1,2,3,4,5,6,7,8] and (offsetRow,offsetColumn) not in boundaries and (offsetRow,offsetColumn not in self.visited):
                boundaries.append((offsetRow,offsetColumn))
    print("The boundaries")
    print(boundaries)
    return boundaries

  def getPossibleCoords(self):
    print("Getting possible coordinates")
    #if len(self.possibleCoords) == 0:
    boundaries = self.getBoundaries()
    stuff = self.hehe()
   # if len(self.possibleCoords) == 0:
    for coord in boundaries:
      if coord not in self.possibleCoords:
        self.possibleCoords.append(coord)
    for coord2 in stuff:
      if coord2 not in self.possibleCoords and coord2 not in boundaries:
        self.possibleCoords.append(coord2)
    print("Remove visited coords??")
    self._removeVisitedCoords()
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
    print("There are ",countS, " spaces in the 3x3 grid")
    print("These are their coordinates", spacesS)
    return countS, spacesS
    
  def _checkMove(self):
    if self.stackFlag._isEmpty() == False:
      print("Flag stack is not empty")
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
    print("Cheking if there are coordinates in stacks")
    move, newRow, newColumn = self._checkMove()
    if move == " ": # if there are no coords in stacks
      print("There are no coordinates in stacks")
      print("Will check the current row and column to find coords to uncover/flag")
      self.compare(currentRow,currentColumn)
      print("Check stacks again")
      move, newRow, newColumn = self._checkMove() # get coord from stack
      if move == " ": # if no coords were added to stacks
        print("No coordinates were added to the stacks")
        print("Each coordinate in possible coordinates will be checked for coordinates to uncover/flag")
        self.getPossibleCoords()
        if len(self.possibleCoords) != 0: # if there are possible coords
          move, newRow, newColumn = self._lol()
          print(move,newRow,newColumn)
          return move, newRow, newColumn
        else: # if possible coords is empty
          print("There were no possible coordiantes, so new ones will be generated")
          self.getPossibleCoords() # find boundaries and possible coords
          if len(self.possibleCoords) == 0: # if possible coords is still empty
            print("possible coordinates is empty so make a random move")
            move, newRow, newColumn = self.randomMove() # make a random move
            print(move,newRow,newColumn)
            return move, newRow, newColumn
          else: # if there are possible coords
            print("Each coordinate in possible coordinates will be checked for coordinates to uncover/flag")
            move, newRow, newColumn = self._lol()
            print(move,newRow,newColumn)
            return move, newRow, newColumn
      else:
        print("There were coordinates in the stacks")
        print(move,newRow,newColumn)
        return move, newRow, newColumn
    else:
      print("There were coordinates in the stacks")
      print(move,newRow,newColumn)
      return move, newRow, newColumn

  def _lol(self):
    print("CHECKING THESE")
    print(self.possibleCoords)
    for coord in self.possibleCoords: # cycle through the possible coords
      row = coord[0]
      column = coord[1]
      self.compare(row,column) # compare them
      #self.possibleCoords.remove(coord)
    move, newRow, newColumn = self._checkMove() # check if anything has been added to the stacks
    if move == " ":
      move, newRow, newColumn = self.randomMove() # if not then make random move
    return move, newRow, newColumn

  def _removeVisitedCoords(self):
    for coord in self.possibleCoords:
      if coord in self.visited:
        print("Removing ",coord," from possible coords")
        self.possibleCoords.remove(coord)

  def compare(self,row, column):
    print("Checking this coordinate", row,column)
    number = self.topGrid[row][column]
    countF, spacesF = self.countFlags(row, column)
    countS, spacesS = self.countSpaces(row,column)
    print("The number in the middle is ",number)
    if countF == number:
      print("Number of flags is the same as the number")
      if countS != 0:
        print("There are spaces to uncover")
        self.visited.append((row,column))
        for i in range(len(spacesS)):
          coord = spacesS[i]
          row = coord[0]
          column = coord[1]
          self.addUncover(row,column)
      elif countS == 0:
        print("Adding ", row,column," to visited")
        self.visited.append((row,column))
        print("There are no spaces to uncover")
        print("So pick a new coordinate to compare")
      
      # pick a new coordinate to compare
    elif countS == number:
      print("Number of spaces is the same as the number")
      if countF == 0:
        print("There are no flags")
        print("So flag remaining spaces")
        print("Adding ", row,column," to visited")
        self.visited.append((row,column))
        for i in range(len(spacesS)):
          coord = spacesS[i]
          row = coord[0]
          column = coord[1]
          self.addFlag(row,column)
      elif countF != 0:
        print("There are flags")
        print("So pick a new coordinate to compare")
        
      # pick a new coordinate to compare
    elif countF + countS == number:
      print("Number of flags and spaces adds up to the number")
      print("So flag the remaining spaces")
      print("Adding ", row,column," to visited")
      self.visited.append((row,column))
      for i in range(len(spacesS)):
        coord = spacesS[i]
        row = coord[0]
        column = coord[1]
        self.addFlag(row,column)
    else:
      print("Pick new coordinate to compare")
      
      # pick a new coordinate to compare
    

     
  