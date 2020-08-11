import random
import math

#################################################################
class Col:
  def __init__(self):
    self.n = 0

#################################################################
class Num(Col):
  def __init__(self):
    self.mu = 0
    self.m2 = 0
    self.sd = 0
    self.n = 0
    self.numbers = []

  def addNumber(self, num):
    self.numbers.append(num)
    self.n += 1
    self.incrementMean(num)
    self.updateStandardDeviation()
  
  def removeNumber(self):
    self.n -= 1
    self.decrementMean(self.numbers.pop())
    self.updateStandardDeviation()

  def incrementMean(self,val):
    if self.n==1:
      self.mu = val
      self.m2 = val * val
    else:
      self.mu = ((self.mu*(self.n-1)) + val)/self.n
      self.m2 = ((self.m2*(self.n-1)) + math.pow(val, 2))/self.n
  
  def decrementMean(self,val):
    if self.n == 0:
      self.mu = 0
      self.m2 = 0
    else:
      self.mu = (((self.mu * (self.n+1)) - val)) / (self.n) 
      self.m2 = (((self.m2 * (self.n+1)) - math.pow(val,2))) / (self.n) 
          
  def updateStandardDeviation(self):
    #print("mu "+str(math.pow(self.mu, 2)))
    #print("m2 "+str(self.m2))
    self.sd = math.pow(self.m2 - (math.pow(self.mu,2)),0.5)
  
  def getMean(self):
    return self.mu
  
  def getStandardDeviation(self):
    return self.sd

#################################################################
class Sym(Col):
  def __init__(self):
    self.n = 0

#################################################################
class Some(Col):
  def __init__(self):
    self.n = 0

#################################################################
# make a list of 100 random numbers
rand_nums = []
for i in range(0,100):
  rand_nums.append(int(random.random() * 256))

# check random numbers
#for i in range(0,100):
#  print(rand_nums[i])

# make caches for mean and std dev
mean_cache = []
sd_cache = []

# make a Num object
num = Num()

# iterate through numbers
for i in range(0, 100):
  num.addNumber(rand_nums[i])
  if i % 10 == 9:
    mean_cache.append(num.getMean())
    print("Mean at index "+str(i)+": "+str(num.getMean()))
    sd_cache.append(num.getStandardDeviation())
    print("Standard Deviation at index "+str(i)+": "+str(num.getStandardDeviation()))

# check sd and mean cache
#for i in range(0,10):
#  print("Mean "+str(i)+", "+str(mean_cache[i]))
#  print("Standard Deviation "+str(i)+", "+str(sd_cache[i]))

for i in range(100, 10, -1):
  num.removeNumber()
  if i % 10 == 9:
    print("Got mean: " + str(num.getMean()) + " at index: " +str(i) )
    print("Expected mean: " + str(mean_cache.pop()) )
    print("Got standard deviation: " + str(num.getStandardDeviation()) + " at index: " + str(i) )
    print("Expected standard deviation: " + str(sd_cache.pop()) )
