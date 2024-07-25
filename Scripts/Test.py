import numpy as np
import matplotlib.pyplot as plt


n = 100000

y = np.random.normal(size=n)
#y = y[y < 2.5]
y = np.exp(y)
mean = np.mean(y)

fig, ax = plt.subplots(1)
ax.hist(y, bins=200, density=True)
ax.plot([1, 1], [0, 0.6], color="blue")
ax.plot([mean, mean], [0, 0.6], color="red")
plt.show()
