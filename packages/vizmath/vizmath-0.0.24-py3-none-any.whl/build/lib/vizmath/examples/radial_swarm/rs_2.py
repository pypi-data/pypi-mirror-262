#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, interp1d
from scipy.integrate import cumtrapz
from bezier import curve as bezier_curve


#%%

# Function to compute cumulative distance along a path for a set of points
def cumulative_distance(points):
    cumdist = [0]
    for i in range(1, len(points)):
        cumdist.append(cumdist[-1] + distance(points[i], points[i-1]))
    return np.array(cumdist)

# Adjust cubic spline interpolation to work with percent of path
def cubic_spline_interpolation_adjusted(points, percent):
    # Convert points list to numpy array for convenience
    points_np = np.array(points)
    x, y = points_np[:, 0], points_np[:, 1]

    # Calculate cumulative distance to get total path length
    cumdist = cumulative_distance(points)
    total_length = cumdist[-1]
    target_length = percent * total_length

    # Create a spline for x and y over cumulative distance
    cs_x = CubicSpline(cumdist, x)
    cs_y = CubicSpline(cumdist, y)

    # Find the interpolated x, y at target length
    interp_x = cs_x(target_length)
    interp_y = cs_y(target_length)

    return interp_x, interp_y

# Re-define the distance function
def distance(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Re-define the linear interpolation function
def linear_interpolation(points, percent):
    lengths = [distance(points[i], points[i+1]) for i in range(len(points)-1)]
    total_length = sum(lengths)
    target_length = percent * total_length
    accumulated_length = 0
    for i, length in enumerate(lengths):
        if accumulated_length + length >= target_length:
            break
        accumulated_length += length
    t = (target_length - accumulated_length) / lengths[i]
    x = (1 - t) * points[i][0] + t * points[i+1][0]
    y = (1 - t) * points[i][1] + t * points[i+1][1]
    return x, y

# Define a function for Bezier curve interpolation
def bezier_interpolation(points, percent):
    # Convert points to format expected by bezier library
    nodes = np.asfortranarray(points).T
    curve = bezier_curve.Curve(nodes, degree=len(points)-1)
    
    # Use the parameter t in [0, 1] to find the point at the specified percent
    t = percent
    point = curve.evaluate(t).flatten()
    
    return point[0], point[1]

#%%
points = [(0, 0), (1, 2), (3, 1), (4, 3)]
percent = 0.75

# Execute linear interpolation
linear_point = linear_interpolation(points, percent)

# Execute adjusted cubic spline interpolation
cubic_point_adjusted = cubic_spline_interpolation_adjusted(points, percent)

# Bezier interpolation
bezier_point = bezier_interpolation(points, percent)

# Plotting both interpolations
fig, ax = plt.subplots(1, 3, figsize=(12, 6))
x, y = zip(*points)

# Linear
ax[0].plot(x, y, 'o-', label='Path')
ax[0].plot(linear_point[0], linear_point[1], 'ro', label='Interpolated Point')
ax[0].set_title('Linear Interpolation')

# Cubic Spline Adjusted
cumdist = cumulative_distance(points)
cs_x = CubicSpline(cumdist, x)
cs_y = CubicSpline(cumdist, y)
interp_cumdist = np.linspace(cumdist[0], cumdist[-1], 1000)
ax[1].plot(x, y, 'o', label='Path')
ax[1].plot(cs_x(interp_cumdist), cs_y(interp_cumdist), '-', label='Cubic Spline')
ax[1].plot(cubic_point_adjusted[0], cubic_point_adjusted[1], 'ro', label='Interpolated Point')
ax[1].set_title('Cubic Spline Interpolation Adjusted')

# Bezier
t = np.linspace(0, 1, 1000)
nodes = np.asfortranarray(points).T
curve = bezier_curve.Curve(nodes, degree=len(points)-1)
ax[2].plot(x, y, 'o', label='Path')
ax[2].plot(*curve.evaluate_multi(t), '-', label='Bezier Curve')
ax[2].plot(bezier_point[0], bezier_point[1], 'ro', label='Interpolated Point')
ax[2].set_title('Bezier Interpolation')

for a in ax:
    a.legend()

plt.tight_layout()
plt.show()

linear_point, cubic_point_adjusted, bezier_point

#%% ------------ tangent testing
def refined_perpendicular_line_at_spline_point(cs, t_75_percent, length=0.2, delta=1e-4):
    """
    Calculate start and end points of a line perpendicular to the cubic spline at a given parameter t,
    using a refined method to estimate the tangent vector.
    
    Parameters:
    - cs: CubicSpline object representing the spline.
    - t_75_percent: The parameter t corresponding to the 75% point along the spline.
    - length: The length of the perpendicular line.
    - delta: A small value to offset from t for estimating the tangent vector.
    
    Returns:
    - A tuple containing the start and end points of the perpendicular line.
    """
    # Calculate points just before and after the specified parameter t
    point_before = cs(t_75_percent - delta)
    point_after = cs(t_75_percent + delta)
    
    # Estimate the tangent vector as the difference between these points
    tangent_vector = point_after - point_before
    # Normalize the tangent vector
    tangent_vector_normalized = tangent_vector / np.linalg.norm(tangent_vector)
    
    # Calculate the perpendicular vector (rotate 90 degrees)
    perpendicular_vector = np.array([-tangent_vector_normalized[1], tangent_vector_normalized[0]])
    
    # Calculate the position of the interpolated point
    point = cs(t_75_percent)
    
    # Calculate the start and end points of the perpendicular line
    start_point = point - perpendicular_vector * (length / 2)
    end_point = point + perpendicular_vector * (length / 2)
    
    return start_point, end_point

# Define a function to generate 7 points on a circle
def generate_circle_points(radius, center=(0, 0), num_points=7):
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    return np.column_stack((x, y))

#%% new functions

# Define a function to generate 7 points on a circle
def generate_circle_points(radius, center=(0, 0), num_points=7):
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    return np.column_stack((x, y))

def cubic_spline_interpolation_with_perpendicular(points, percent, length=0.2, delta=1e-4):
    """
    Interpolate a point using cubic spline interpolation and calculate a perpendicular line at that point.
    
    Parameters:
    - points: Array of points [(x1, y1), (x2, y2), ...] defining the path.
    - percent: The percent along the path where the interpolation should occur.
    - length: The length of the perpendicular line.
    - delta: A small value to offset from t for estimating the tangent vector.
    
    Returns:
    - A tuple containing the interpolated point and the start and end points of the perpendicular line.
    """
    # Convert points list to numpy array for convenience
    points_np = np.array(points)
    x, y = points_np[:, 0], points_np[:, 1]

    # Calculate cumulative distance to parameterize by arc length
    cumdist = np.insert(np.cumsum(np.sqrt(np.sum(np.diff(points_np, axis=0)**2, axis=1))), 0, 0)
    total_length = cumdist[-1]
    target_length = percent * total_length

    # Create a spline for x and y over cumulative distance
    cs_x = CubicSpline(cumdist, x, bc_type='periodic')
    cs_y = CubicSpline(cumdist, y, bc_type='periodic')
    
    # Find the parameter t that corresponds to the target length
    t_target = np.interp(target_length, cumdist, np.linspace(0, 1, len(points_np)))
    
    # Interpolate the point at target length
    interp_x = cs_x(target_length)
    interp_y = cs_y(target_length)
    interp_point = np.array([interp_x, interp_y])
    
    # Calculate tangent vector at the interpolated point using refined method
    point_before = np.array([cs_x(target_length - delta), cs_y(target_length - delta)])
    point_after = np.array([cs_x(target_length + delta), cs_y(target_length + delta)])
    tangent_vector = point_after - point_before
    
    # Normalize the tangent vector
    tangent_vector_normalized = tangent_vector / np.linalg.norm(tangent_vector)
    
    # Calculate the perpendicular vector (rotate 90 degrees)
    perpendicular_vector = np.array([-tangent_vector_normalized[1], tangent_vector_normalized[0]])
    
    # Calculate the start and end points of the perpendicular line
    start_point = interp_point - perpendicular_vector * (length / 2)
    end_point = interp_point + perpendicular_vector * (length / 2)
    
    return interp_point, start_point, end_point

circle_points = generate_circle_points(1)

# Use the updated function to interpolate and calculate perpendicular line for the circle points
interp_point, perp_start, perp_end = cubic_spline_interpolation_with_perpendicular(circle_points, percent=0.75, length=0.5)

spline_t_fine = np.linspace(0, cumdist[-1], 1000)
spline_points_x = cs_x(spline_t_fine)
spline_points_y = cs_y(spline_t_fine)
spline_points = np.column_stack((spline_points_x, spline_points_y))

# Plotting
plt.figure(figsize=(8, 8))
plt.plot(circle_points[:, 0], circle_points[:, 1], 'o', label='Control Points')
plt.plot(spline_points[:, 0], spline_points[:, 1], '-', label='Cubic Spline')
plt.plot(interp_point[0], interp_point[1], 'ro', label='Interpolated Point')
# Plot the perpendicular line at the interpolated point
plt.plot([perp_start[0], perp_end[0]], [perp_start[1], perp_end[1]], 'g-', label='Perpendicular Line')
plt.axis('equal')
plt.legend()
plt.title('Cubic Spline with Perpendicular Line at Interpolated Point')
plt.show()

interp_point, perp_start, perp_end

#%%
def linear_interpolation_with_perpendicular(points, percent, length=0.2):
    """
    Interpolate a point using linear interpolation along a path defined by points and calculate
    a perpendicular line at that interpolated point.
    
    Parameters:
    - points: Array of points [(x1, y1), (x2, y2), ...] defining the path.
    - percent: The percent along the path where the interpolation should occur.
    - length: The length of the perpendicular line.
    
    Returns:
    - A tuple containing the interpolated point and the start and end points of the perpendicular line.
    """
    # Convert points list to numpy array for convenience
    points_np = np.array(points)
    cumdist = np.insert(np.cumsum(np.sqrt(np.sum(np.diff(points_np, axis=0)**2, axis=1))), 0, 0)
    total_length = cumdist[-1]
    target_length = percent * total_length
    
    # Find the segment where the interpolated point lies
    for i in range(len(cumdist) - 1):
        if cumdist[i] <= target_length <= cumdist[i + 1]:
            break
            
    # Calculate the parameter t for linear interpolation within the segment
    t = (target_length - cumdist[i]) / (cumdist[i + 1] - cumdist[i])
    interp_point = (1 - t) * points_np[i] + t * points_np[i + 1]
    
    # Calculate the direction vector of the segment
    direction_vector = points_np[i + 1] - points_np[i]
    # Normalize the direction vector
    direction_vector_normalized = direction_vector / np.linalg.norm(direction_vector)
    # Calculate the perpendicular vector (rotate 90 degrees)
    perpendicular_vector = np.array([-direction_vector_normalized[1], direction_vector_normalized[0]])
    
    # Calculate the start and end points of the perpendicular line
    start_point = interp_point - perpendicular_vector * (length / 2)
    end_point = interp_point + perpendicular_vector * (length / 2)
    
    return interp_point, start_point, end_point

# Use the linear interpolation function with perpendicular line calculation on the circle points
linear_interp_point, linear_perp_start, linear_perp_end = linear_interpolation_with_perpendicular(circle_points, percent=0.75, length=0.5)

# Plotting for linear interpolation
plt.figure(figsize=(8, 8))
plt.plot(circle_points[:, 0], circle_points[:, 1], 'o', label='Control Points')
plt.plot([point[0] for point in circle_points], [point[1] for point in circle_points], '-', label='Linear Path')
plt.plot(linear_interp_point[0], linear_interp_point[1], 'ro', label='Linear Interpolated Point')
# Plot the perpendicular line at the linear interpolated point
plt.plot([linear_perp_start[0], linear_perp_end[0]], [linear_perp_start[1], linear_perp_end[1]], 'g-', label='Perpendicular Line')
plt.axis('equal')
plt.legend()
plt.title('Linear Interpolation with Perpendicular Line at Interpolated Point')
plt.show()

linear_interp_point, linear_perp_start, linear_perp_end
