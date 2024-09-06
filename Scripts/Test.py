import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.interpolate import PchipInterpolator


x = np.array([0, 1, 2, 3, 4])
y = np.array([10, 0, 10, 0, 10])

cs = PchipInterpolator(x, y)
x_smooth = np.linspace(x.min(), x.max(), 100)
y_smooth = cs(x_smooth)

plt.plot(x_smooth, y_smooth, label='Cubic Spline Interpolation')
plt.scatter(x, y, color='red', label='Data Points')
plt.legend()
plt.title('Cubic Spline Interpolation of Data Points')
plt.show()
