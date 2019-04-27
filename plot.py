import pandas as pd
from sklearn.decomposition import PCA
import pickle
import matplotlib.pyplot as plt

f = open("normalized.pkl","rb")
dist = pickle.load(f)
f.close()
f = open("result.pkl","rb")
outlier_index = pickle.load(f)
f.close()
print(outlier_index)
print(dist,type(dist))
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(dist)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])
print(principalDf)
a = list(principalDf['principal component 1'])
b = list(principalDf['principal component 2'])
# a = list(principalDf.loc[:,'principal component 1'])
# b = list(principalDf.loc[:,'principal component 2'])
plt.scatter(a[:1000],b[:1000])
a = []
b = []
for item in outlier_index:
  print(item)
  a.append(principalDf.loc[item,'principal component 1'])
  b.append(principalDf.loc[item,'principal component 2'])
plt.scatter(a,b,c='red')
plt.show()