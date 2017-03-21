class X(object):
  def __init__(self, x):
    pass

  def doit(self, bar):
    pass

class Y(X):
  def __init__(self):
    super(Y, self).__init__(123)

  def doit(self, foo):
    return super(Y, self).doit(foo)

class Z(Y):
  def __init__(self):
    super(Z, self).__init__()

z = Z()