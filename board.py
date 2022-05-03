import random

class Board:
  def __init__(self,mines,height,width,minecoordinates):
    self.mines = mines
    self.height = height
    self.width = width
    self.mine = "*"
    self.flags = []
    self.visited = []
    self.stackFlag = []
    self.stackUncover = []
    self.number = [1,2,3,4,5,6,7,8] # all of the pissible numbers that a space can be
    self.minecoordinates = minecoordinates
    self.topGrid = [["-" for i in range(self.width)]for j in range(self.height)] # creates the player grid
    #self.dataGrid = [['*', 1, '-', '-', '-', '-', '-', '-', 1, '*'], [1, 1, '-', '-', '-', '-', '-', '-', 1, 1], ['-', '-', '-', '-', '-', 1, 1, 1, '-', '-'], ['-', '-', 1, 1, 1, 1, '*', 1, 1, 1], 
#['-', '-', 1, '*', 2, 3, 2, 2, 1, '*'], [1, 1, 2, 2, '*', 2, '*', 2, 3, 2], [1, '*', 2, 2, 3, 4, 4, '*', 2, '*'], [1, 
#1, 2, '*', 2, '*', '*', 2, 2, 1]]
    self.dataGrid = [["-" for i in range(self.width)]for j in range(self.height)] # creates the data grid
    self.offsets = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)] # offsets used for uncovering
    self.area = (self.height*self.width) - self.mines
    if self.minecoordinates == []:
      self._generateMines() # if there are no mine coordinates then generate them
    else:
      self._placeMines() # otherwise place the mines in the right spots
      self._placeNumbers() # and place numbers around the mines

      
  def getMinecoordinates(self):
    return self.minecoordinates  

    
  def showGrid(self,grid): # displays the grid specified in the parameter
    print(" ", end = " ")
    characters = 65 + self.width
    for i in range(65,characters): # on the top row displays letters for the coordinates
      print(chr(i), end = " ")
    print() 
    for y in range(self.height):
      print(y, end = " ")
      for x in range(self.width):
        print(grid[y][x], end = " ")
      print()

  
  def _generateMines(self): # generates mines
    placed = 0
    while placed < self.mines: # places exactly the number of mines specified by the difficulty
      row = random.randint(0, self.height - 1)
      column = random.randint(0, self.width - 1)
      if self.dataGrid[row][column] == "-": # only places mines in empty spaces
        self.dataGrid[row][column] = self.mine
        self.minecoordinates.append([row,column]) # stores the coordinates of the mines
        placed += 1
    self._placeNumbers() # calls the place numbers function

  
  def _placeMines(self): # places the mines on the grid
    for i in range(len(self.minecoordinates)):
      coords = self.minecoordinates[i] # splits the list into coordinates
      row = coords[0]
      column = coords[1]
      self.dataGrid[row][column] = self.mine # places mines
      
      
  def _placeNumbers(self):
    location = self.minecoordinates # places numbers around each mine
    offsets = self.offsets
    for i in range(len(location)):
      number = 0
      mcoords = location[i] # coordinates of the mine
      mRow = mcoords[0]
      mColumn = mcoords[1]
      for j in range(len(offsets)): # looks in the 3x3 grid around each mine
        offset = offsets[j]
        offsetRow = offset[0] + mRow
        offsetColumn = offset[1] + mColumn
        if offsetRow in range(0, self.height) and offsetColumn in range(0, self.width):
          if self.dataGrid[offsetRow][offsetColumn] == self.mine:
            pass # if there's a mine in the 3x3 grid then do nothing
          elif self.dataGrid[offsetRow][offsetColumn] == "-":
            self.dataGrid[offsetRow][offsetColumn] = 1 # if the space is blank then place 1
          elif self.dataGrid[offsetRow][offsetColumn] in [1,2,3,4,5,6,7]:
            number = int(self.dataGrid[offsetRow][offsetColumn]) + 1 # onto the number already placed add 1
            self.dataGrid[offsetRow][offsetColumn] = number


  def uncover(self,row,column): # uncovers a single space
    self.visited.append((row,column)) # saves the row, column to visited to not visit it again
    if self.dataGrid[row][column] == "*": # if mine is hit then end the game
      end = True
      win = False
      return end, win
    elif self.topGrid[row][column] in self.number: # if the coordinate is a number then count the number of flags
      count = self._countFlags(row,column)
      if count == self.topGrid[row][column]:
        row, column = self._offsetCoords(row,column)
        self.uncover(row,column)
      else:
        pass # if there isn't the same number of flags then don't uncover
    elif self.topGrid[row][column] == "F": # if the coordinate is a flag then do nothing 
      pass
    else:
      self.topGrid[row][column] = self.dataGrid[row][column] # copy the value from the data grid onto the top grid 
      if self.dataGrid[row][column] == "-": # if the space is blank then uncover that space
        self.topGrid[row][column] = " "
        self._offsetCoords(row,column) # calls the offset coords function to offset the original row, column
    win = self._countSpacesLeft()
    end = False
    return end, win

        
  def _offsetCoords(self,row,column):
    for i in range(len(self.offsets)):
      offset = self.offsets[i] # offsets the row, column using offsets
      offsetRow = offset[0] + row
      offsetColumn = offset[1] + column
      if offsetRow in range(0,self.height) and offsetColumn in range(0,self.width): # checks if the offset coordinates fit on the board
        if (offsetRow,offsetColumn) not in self.visited:
          self.uncover(offsetRow, offsetColumn)
        
  
  def _countFlags(self,row,column):
    countF = 0 
    for i in range(len(self.offsets)):
      offset = self.offsets[i] # offsets the row, column using offsets
      offsetRow = offset[0] + row
      offsetColumn = offset[1] + column
      if offsetRow in range(0,self.height) and offsetColumn in range(0,self.width):
        if self.topGrid[offsetRow][offsetColumn] == "-":
          countF += 1
    return countF


  def _countSpaces(self,row,column):
    countS = 0
    offsetRow, offsetColumn = self._offsetCoords(row,column)
    if self.topGrid[offsetRow][offsetColumn] == "-":
      countS += 1
    return countS
      
  
  def placeFlag(self,row,column):
    if self.topGrid[row][column] == "-": # only allows to place flags on uncovered spaces
      self.topGrid[row][column] = "F" # places a flag
      #print("Flag placed")
      if self.dataGrid[row][column] == "*": # if mine is flagged then add to list of correct flags
        self.flags.append([row,column])
        #print("Flag correctly placed")
    else:
      print("Flag not placed")
    end = False
    win = False
    return end, win

  
  def removeFlag(self,row,column): # removes a flag from a space 
    if self.topGrid[row][column] == "F": # only allows to remove an existing flag
      self.topGrid[row][column] = "-" # removes flag
      #print("Flag removed")
      if (row,column) in self.flags: # if the flag was correct then remove from list of correct flags
        self.flags.remove((row,column))
        #print("Flag removed from list")
    else:
      print("Flag not removed") 
    end = False
    win = False
    return end, win


  def _countSpacesLeft(self):
    countSpaces = 0
    win = False
    for y in range(self.height):
      for x in range(self.width):
        if self.topGrid[y][x] not in [1,2,3,4,5,6,7,8," "]:
          countSpaces += 1
    if countSpaces == self.mines:
      win = True
    return win