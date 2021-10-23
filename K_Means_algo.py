import numpy as np
import matplotlib.pyplot as plt
import random

data = np.load('kmeans_data.npy')
k = 5



def kmeans(data, k, iterations=10):
    print(k)
    centers = []
    for i in range(k):
        center = random.choice(range(len(data)))  # 10

        while center in centers:
            center = random.choice(range(len(data)))
        centers.append(center)

    centers = [data[x] for x in centers]

    print("Pirminiai centrai: ", centers)

    for iteration in range(iterations):
        y = []
        for point in data:
            distances = []
            for i, center in enumerate(centers):
                distances.append(np.linalg.norm(point - center))
            y.append(np.argmin(distances))
            # print(distances, np.argmin(distances))

        # print(y)

        # perskaiciuojame centrus
        for i, center in enumerate(centers):
            count = 0
            center_coords = np.array([0, 0], dtype=np.float64)
            for point, prediction in zip(data, y):
                if prediction == i:
                    count += 1
                    center_coords += point
            centers[i] = center_coords / count

        print("ITERACIJA: {}; perskaiciuoti centrai: {}".format(iteration, centers))

    return y, centers


y, centers = kmeans(data, k)


plt.scatter(data[:, 0], data[:, 1], c=y)


from sklearn.cluster import KMeans
kmeans1 = KMeans(n_clusters=2, random_state=0).fit(data)
kmeans1.cluster_centers_
plt.scatter(data[:, 0], data[:, 1])
plt.scatter(kmeans1.cluster_centers_[:, 0], kmeans1.cluster_centers_[:, 1])



