

#%%
from vizmath.beeswarm import swarm
from vizmath import functions as vf
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

#%%
# o_swarm = swarm.random_swarm(10)
# o_swarm.beeswarm_plot()
# o_swarm.o_beeswarm.dataframe_to_csv('rs_test_1')
#%%
df = pd.read_csv(os.path.dirname(__file__) + '/rs_test_1.csv')
df = df.loc[df['path'] == 1].copy(deep=True)
df = df[['id','x','area']].sort_values(by='x')
#%%
o_swarm = swarm(df, id_field='id', position_field='x', size_field='area')
o_swarm.beeswarm_plot()

#%%
rel_to = 4
rad = 100

min = df['x'].min()
xs = [x - min for x in df['x']]
max = np.max(xs)
c_pts = [vf.polarize(x, max, rad) for x in xs]
xya = [(x,y,vf.angle_of_two_points(0,0,x,y)) for (x,y) in c_pts]
xyr = [tuple(list(vf.rotate(x, y, -xya[rel_to][2])) + [a_] + [a-xya[rel_to][2]]) for (x,y,a),a_ in zip(xya,df['area'])]
xyr

#%%
# Prepare figure and axes
fig, ax = plt.subplots()

# Calculate max radius to adjust limits dynamically
max_radius = np.max([np.sqrt(area / np.pi) for x, y, area, a in xyr])

# Calculate bounds for the plot
min_x = np.min([x - max_radius for x, _, _, _ in xyr])
max_x = np.max([x + max_radius for x, _, _, _ in xyr])
min_y = np.min([y - max_radius for _, y, _, _ in xyr])
max_y = np.max([y + max_radius for _, y, _, _ in xyr])

# Set limits dynamically based on the circles
ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)

# Ensure that the axes are evenly spaced
ax.set_aspect('equal', adjustable='box')

# Iterate over each set of coordinates and area
for x, y, area, _ in xyr:
    # Calculate the radius of the circle from the area
    radius = np.sqrt(area / np.pi)
    # Create a circle with the calculated radius and specified center
    circle = plt.Circle((x, y), radius, edgecolor='r', facecolor='none')
    # Add the circle to the plot
    ax.add_artist(circle)

# Show plot
plt.show()
# %%
