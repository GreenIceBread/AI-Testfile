import random

board = [['*', 1, '-', '-', '-', '-', '-', '-', 1, '*'], [1, 1, '-', '-', '-', '-', '-', '-', 1, 1], ['-', '-', '-', '-', '-', 1, 1, 1, '-', '-'], ['-', '-', 1, 1, 1, 1, '*', 1, 1, 1], 
['-', '-', 1, '*', 2, 3, 2, 2, 1, '*'], [1, 1, 2, 2, '*', 2, '*', 2, 3, 2], [1, '*', 2, 2, 3, 4, 4, '*', 2, '*'], [1, 
1, 2, '*', 2, '*', '*', 2, 2, 1]]
uncoverStack = []
flagStack = []
visited = []
possibleCoords= []
offsets = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
height = 8
width = 10
row = 1
column = 0


def getMove(row,column):
    found = compare(row,column)



def addFlag(row,column):
    flagStack.append((row,column))

def addUncover(row,column):
    uncoverStack((row,column))

def getBoundaries(height,width):
    boundaries = []
    for y in range(height):
      for x in range(width):
        if board[y][x] == " ":
          for offset in offsets:
            offsetRow = offset[0] + y
            offsetColumn = offset[1] + x
            if offsetRow in range(0, height) and offsetColumn in range(0, width):
              if board[offsetRow][offsetColumn] in [1,2,3,4,5,6,7,8] and (offsetRow,offsetColumn) not in boundaries:
                boundaries.append((offsetRow,offsetColumn))
    print(boundaries)
    return boundaries


def getCoord():
    boundaries = getBoundaries()
    for coord in boundaries:
        if coord not in possibleCoords and coord not in visited:
            possibleCoords.append(coord)

    if len(possibleCoords) != 0:
        newcoord = possibleCoords[-1]
        newrow = newcoord[0]
        newcolumn = newcoord
        return newrow, newcolumn
    else:
        newrow = -1
        newcolumn = -1
        return newrow, newcolumn


def countFlags(row,column):
    countF = 0
    spacesF = []
    for offset in offsets:
        offsetRow = offset[0] + row
        offsetColumn = offset[1] + column
        if offsetRow in range(0, height) and offsetColumn in range(0, width):
            if board[offsetRow][offsetColumn] == "F":
                countF += 1
                spacesF.append((offsetRow,offsetColumn))
    return countF, spacesF

def countSpaces(row, column):
    countS = 0
    spacesS = []
    for offset in offsets:
      offsetRow = offset[0] + row
      offsetColumn = offset[1] + column
      if offsetRow in range(0, height) and offsetColumn in range(0, width):
        if board[offsetRow][offsetColumn] == " ":
          countS += 1
          spacesS.append((offsetRow,offsetColumn))
    return countS, spacesS




def compare(row, column):
    number = board[row][column]
    countF, spacesF = countFlags(row, column)
    countS, spacesS = countSpaces(row,column)
    if countF == number:
      if countS != 0:
        for i in range(len(spacesS)):
          coord = spacesS[i]
          row = coord[0]
          column = coord[1]
          addUncover(row,column)
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
          addFlag(row,column)
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
        addFlag(row,column)
        found = True
        return found
    else:
      found = False
      return found


getMove(row,column)
print(uncoverStack)
print(flagStack)