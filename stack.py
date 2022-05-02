class Stack:
  def __init__(self,maxsize):
    self.maxsize = maxsize
    self.items = []

  def _isEmpty(self):
    if len(self.items) == 0:
      return True
    else:
      return False
    
  def _isFull(self):
    if len(self.items) == self.maxsize:
      return True
    else:
      return False

  def push(self,item):
    if not self._isFull():
      self.items.append(item)

  def pop(self):
    if not self._isEmpty():
      return self.items.pop()
    else:
      return False

  def peek(self):#for testing
    print(self.items[-1])

  def getSize(self):#for testing
    print(len(self.items))

  def showStack(self):#for testing
    print(self.items)

  def _hasItem(self,coord):
    if coord in self.items:
      return True
    else:
      return False
