import pandas as pd
import re

df1 = pd.DataFrame({'A': ['19M', 2, "3B", 4, '5%', "(6)", 7], 'B': ['(1B)', 2, 3, 4, 5, '-', 7], 'C': ['1B', 2, 3, 4, 5, 6, 7], 'D': ['1B', 2, 3, 4, 5, 6, 7]},)

print(df1)
df1 = df1.astype(str)

for column in df1.iloc[:, :]:
    for i in column:
        print(i)


print(df1)


# number1 = -abs(1)
#
# print(number1)






























