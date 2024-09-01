import matplotlib.pyplot as plt

# Create a figure and axis
fig, ax = plt.subplots()

# Plot something for demonstration
ax.plot([0, 1, 2], [0, 1, 4])

# Set axis labels
ax.set_xlabel('X-axis label')
ax.set_ylabel('Y-axis label', position=(0.5, 0.5))

# Show the plot
plt.show()
