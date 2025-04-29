class State:
  def __init__(self, value=False):
    self.__value = value
  
  def __call__(self, *args, **kwds):
    return self.__value
    
  def get(self):
    return self.__value

  def set(self, value):
    self.__value = value
    return self.__value