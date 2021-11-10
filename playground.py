import random
import numpy as np
import matplotlib.pyplot as plt

rand0 = []
rand1 = []
rand2=[]
main_list= []
for i in range(0,20):
    n = random.randint(1,30)
    b = random.randint(1, 30)
    c = random.randint(1, 30)
    rand0.append(n)
    rand1.append(b)
    rand2.append(c)

main_list.append(rand0)
main_list.append(rand1)
main_list.append(rand2)

print(main_list)

# spread = np.random.rand(50) * 100
# center = np.ones(25) * 50
# flier_high = np.random.rand(10) * 100 + 100
# flier_low = np.random.rand(10) * -100
# data = np.concatenate((spread, center, flier_high, flier_low))

spread = np.random.rand(50) * 100
center = np.ones(25) * 40
flier_high = np.random.rand(10) * 100 + 100
flier_low = np.random.rand(10) * -100
d2 = np.concatenate((spread, center, flier_high, flier_low))


data = [spread,center,flier_high,flier_low]
fig7, ax7 = plt.subplots()
ax7.set_title('Multiple Samples with Different sizes')
ax7.boxplot(data)

plt.show()


