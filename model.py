import numpy as np # magic sauce

def norm(x, y): # restrains x and y-values between a range of 0-1 for better training (x <- (x - min(x)) / range(x))
  xC = np.zeros(x.shape) # xC - x changed
  yC = np.zeros(y.shape)
  maxx = max(x)
  maxy = max(y)
  # technically you're supposed to normalize (from 0-1) by doing xC = (x - min) / (maxX - minX) but for this dataset, I know that the minimum has to be 0 so I didn't bother
  if maxy != 0: # you don't want divide by zero errors so we do this, we have to do this since some datasets are just zeros for y-values
    yC = y / maxy 
  xC = x / maxx

  return xC, yC

def expander(x, n): # transforms x -> [1, x, x^2, ... x^(n-1)] for an array of x-values (m x 1 -> m x n)
  acts = np.zeros(shape=(x.shape[0], n)) # i instantiate an np array instead of a list because np arrays can do matrix multplication and are more big brain than lists in general

  for i in range(n): # turn every column in the expanded inputs into the original inputs to the power of the column's index
    acts[:, i] = x[:, 0] ** i

  return acts

def normal(acts, y, lb=0): # regularized normal equation, weightV = inv(X'X + λI) * X'Y, 'weightV' is the weight vector
  xtx = np.dot(acts.T, acts) # we're using acts instead of X since expanded activations allow us to make more complex curves to fit the data
  regMat = (lb * np.eye(acts.shape[1]))
  regMat[0][0] = 0 # we don't want to have bias regularization since a high bias won't cause overfitting
  return np.dot(np.dot(np.linalg.inv(xtx + regMat), acts.T), y)

class Model: # convenient way to store data relating to a model
  def __init__(self, x, y, n, lb=0):
    self.x, self.y  = norm(x, y)
    self.x = self.x
    self.y = self.y
    self.acts = expander(self.x, n)
    self.weightV = None
    self.lb = lb

  def normal(self):
    self.weightV = normal(self.acts, self.y, self.lb)
