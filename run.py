import pandas as pd
from multiprocessing.pool import ThreadPool
from scipy.spatial import distance
import pickle

f = open("d.pkl","rb")
dist = pickle.load(f)
f.close()

# df = pd.read_pickle("./normalized.pkl")



n = int(input("enter no of points: "))

def lof():
  k = int(input("Enter k for kth nearst neighbour: "))
  #step1
  #calculate k-distances
  k_distance = []
  for i in range(n):
    distance_list = []
    for j in range(n):
      distance_list.append(dist[(i,j)])
    distance_list.sort()
    k_distance.append(distance_list[k-1])
  
  #step2
  #reachability distance
  reach_dist = {}
  for i in range(n):
    for j in range(n):
      x = k_distance[j]
      if x < dist[(i,j)]:
        x = dist[(i,j)]
      reach_dist[(i,j)] = x
  
  #step3
  #lrd
  lrd = []
  for i in range(n):
    tmpList = []
    x = 0
    for j in range(n):
      if k_distance[i] == dist[(i,j)]:
        tmpList.append(j)
    for item in tmpList:
      x = x + reach_dist[(i,item)]
    if x != 0:
      x = len(tmpList)/x
    lrd.append(x)
  print(len(lrd))
    
  #step4
  #lof
  lof = []
  for i in range(n):
    tmpList = []
    x = 0
    for j in range(n):
      if k_distance[i] == dist[(i,j)]:
        tmpList.append(j)
    for item in tmpList:
      x = x + lrd[item]
    x = x/len(tmpList)
    if x != 0:
      x = x/lrd[i]
    lof.append(x)
  print(lof)
  max = 0
  for i in lof:
    if i > max:
      max = i
  print(max)
  return lof
  

  

def dbscan():
  points = []
  border = []
  outlier = []
  for i in range(n):
    border.append(0)
  for i in range(n):
    points.append([0])
  radius = float(input("Enter radius for min distance: "))
  minPts = float(input("Enter min number of points for a point to be core point: "))
  maxDist = 0
  for row1 in range(n):
    for row2 in range(n):
      distance = dist[(row1,row2)]
      if distance < radius:
        points[row1][0] = points[row1][0]+1
        points[row1].append(row2)
  for item in points:
    if item[0] > minPts:
      for i in item:
        border[i] = 1
  index = 0
  for item in border:
    if item == 0:
      outlier.append(index)
    index = index + 1
  return outlier

i = int(input("enter 1 for dbscan and 2 for lof: "))
f = open("result.pkl","wb")
if i == 1:
  outlier = dbscan()
  pickle.dump(outlier,f)
  print(outlier)
if i == 2:
  lof_list = lof()
  outlier = []
  index = 0
  for i in lof_list:
    if i > 1:
      outlier.append(index)
    index = index + 1
  pickle.dump(outlier,f)
  print(outlier)
  f.close()