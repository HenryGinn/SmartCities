import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Simulated data
data = np.random.normal(loc=0, scale=1, size=1000)

# Create histograms with different bin counts
for bins in [10, 30, 50]:
    plt.figure(figsize=(10, 6))

    # Plot histogram
    plt.hist(data, bins=bins, density=True, alpha=0.6, edgecolor='black')

    # Fit normal distribution
    mean, std_dev = norm.fit(data)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mean, std_dev)
    plt.plot(x, p, 'k', linewidth=2)

    # Add labels and title
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.title(f'Histogram with {bins} Bins and Fitted Normal Distribution')
    plt.show()
