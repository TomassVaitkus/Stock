from sklearn.cluster import KMeans
import pandas as pd
import random
import numpy as np
from sklearn.model_selection import train_test_split

data_set = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

(X_train, X_test) = train_test_split(data_set,test_size=0.30)
kmeans = KMeans.fit(X_train[['A','B']])

print(X_test)















