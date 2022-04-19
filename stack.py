class Stack:
  def __init__(self,maxsize):
    self.maxsize = maxsize
    self.items = []

  def _isEmpty(self):
    return len(self.items) == 0

  def _isFull(self):
    return len(self.items) == self.maxsize

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