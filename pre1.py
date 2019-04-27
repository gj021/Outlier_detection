import pandas as pd
from multiprocessing.pool import ThreadPool
from scipy.spatial import distance
import pickle
import itertools
import time

#getting the entire dataframe in a variable df

df = pd.read_csv("creditcard.csv")
# given a column returns the min and max value in that column
def calEdge(col):
  min = df.loc[0,col]
  max = df.loc[0,col]
  for item in df.loc[:,col].values:
    if item < min:
      min = item
    if item > max:
      max = item
  return min,max

def doNormalise(item):
  start = time.time()
  min,max = calEdge(item)
  print(item)
  for element in range(1000):
    df.loc[element,item] = df.loc[element,item] - min
    df.loc[element,item] = df.loc[element,item]/(max-min)
  end = time.time()
  print(end-start)

#normalises the database
def normalise():
  item = list(df)
  print(item)
  pool=ThreadPool()
  pool.map(lambda x: doNormalise(x), item)

   
normalise()
df.to_pickle("./nor.pkl")

f = open("nor.pkl","rb")
df = pickle.load(f)
f.close()
dist = {}

def calcDist(row):
  print(row)
  a = list(df.loc[row[1],:])
  b = list(df.loc[row[0],:])
  distance = 0
  for item in range(0,len(a)-1):
    x = (a[item] - b[item])**2
    x = x/len(a)
    distance = distance + x
  dist[(row[0],row[1])] = distance
  return distance

item = []
for row1 in range(1000):
  for row2 in range(1000):
    itemElement = [row1,row2]
    item.append(itemElement)
pool = ThreadPool()
pool.map(lambda x: calcDist(x), item)

f = open("d.pkl","wb")
pickle.dump(dist,f)
f.close()