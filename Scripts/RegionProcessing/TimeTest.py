import time

import matplotlib.pyplot as plt
import numpy as np

from voronoi import Voronoi


N = [10, 50, 250, 1000, 2500, 5000, 10000]
delaunay_times = []
voronoi_times = []

for n in N:
    continue
    points = np.random.rand(n, 2)
    voronoi = Voronoi(points)
    start_time = time.time()
    voronoi.construct_polygons()
    total_time_taken = time.time() - start_time
    delaunay_times.append(voronoi.delaunay.time_taken)
    voronoi_times.append(total_time_taken - voronoi.delaunay.time_taken)
    print(n, total_time_taken)

voronoi_times = [
    0.0,
    0.0019943714141845703,
    0.009973287582397461,
    0.03889584541320801,
    0.10171890258789062,
    0.25147390365600586,
    0.5124607086181641]

delaunay_times = [
    0.003991603851318359,
    0.06984186172485352,
    1.5907185077667236,
    24.6480929851532,
    160.15788292884827,
    628.0600385665894,
    2483.8676755428314]

fig, ax = plt.subplots(1)
ax.plot(N, delaunay_times, label="Delaunay", color="red")
ax.plot(N, voronoi_times, label="Voronoi", color="dodgerblue")
ax.legend()
plt.savefig("SlowDelaunayTimeTest.pdf", format="pdf", pad_inches="tight")