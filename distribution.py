import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import csv
import random
import statistics
import matplotlib.animation as animation


boys = []
girls = []

with open('heights2.csv', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[2] == 'Female':
            girls.append(float(row[0]))
        elif row[2] == 'Male':
            boys.append(float(row[0]))

# Shuffle for random order sampling without replacement
random.shuffle(boys)
random.shuffle(girls)

# Store original sizes
total_frames = max(len(boys), len(girls))

# Initialize figure
fig, ax = plt.subplots(figsize=(10, 5))
boyHeights = []
girlHeights = []

# Animation update function
def update(frame):
    ax.clear()

    if boys:
        boyHeights.append(boys.pop(0))
    if girls:
        girlHeights.append(girls.pop(0))
    
    
    sb.histplot(boyHeights, bins=60, kde=True, color='blue', label='Boys', stat='density', ax=ax)
    sb.histplot(girlHeights, bins=60, kde=True, color='pink', label='Girls', stat='density', ax=ax)
    
    # Calculate stats and update title
    if len(boyHeights) > 1 and len(girlHeights) > 1:
        boyMean = statistics.mean(boyHeights)
        girlMean = statistics.mean(girlHeights)
        boySD = statistics.stdev(boyHeights)
        girlSD = statistics.stdev(girlHeights)
        ax.set_title(f"Means → Boys: {boyMean:.2f} cm, Girls: {girlMean:.2f} cm\n"
                     f"SDs → Boys: {boySD:.2f}, Girls: {girlSD:.2f}")
        
        min_height = min(min(boyHeights), min(girlHeights)) - 5
        max_height = max(max(boyHeights), max(girlHeights)) + 5
        ax.set_xlim(min_height, max_height)

    # Dynamic y-limit based on histogram and KDE heights
    y_max = 0
    for container in ax.containers:
        for bar in container:
            y_max = max(y_max, bar.get_height())
    for line in ax.lines:
        if len(line.get_ydata()) > 0:
            y_max = max(y_max, max(line.get_ydata()))
    ax.set_ylim(0, y_max * 1.1 if y_max > 0 else 1)

   
    ax.set_xlabel("Height (cm)")
    ax.set_ylabel("Density")
    ax.legend()
    ax.grid(True)

    # --- Progress bar ---
    completed = frame + 1
    progress = completed / total_frames
    bar_width = ax.get_xlim()[1] - ax.get_xlim()[0]
    ax.barh(y=ax.get_ylim()[0] - y_max * 0.08, width=progress * bar_width, height=y_max * 0.02,
            left=ax.get_xlim()[0], color='green', alpha=0.5)
    ax.text(ax.get_xlim()[0], ax.get_ylim()[0] - y_max * 0.12,
            f"Progress: {int(progress * 100)}%", fontsize=9)


ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=100, repeat=False)

plt.show()
