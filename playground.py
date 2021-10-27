import pandas as pd
import numpy as np
import random

from sklearn.cluster import KMeans

df = pd.DataFrame(np.random.randn(20, 5), columns=['one', 'two', 'three','four','five'])
ix = [(row, col) for row in range(df.shape[0]) for col in range(df.shape[1])]
for row, col in random.sample(ix, int(round(0.3*len(ix)))):
    df.iat[row, col] = np.nan

new_df =df[['one','three','five']].dropna().reset_index(drop=True)



model = KMeans(n_clusters=5).fit(new_df)
print(model.labels_)

print(new_df)