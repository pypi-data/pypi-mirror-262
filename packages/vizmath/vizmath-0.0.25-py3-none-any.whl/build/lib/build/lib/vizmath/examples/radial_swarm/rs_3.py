#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from vizmath import functions as vf

#%%
def generate_circle_points(radius, center=(0, 0), num_points=7):
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    return np.column_stack((x, y))

def cubic_spline_interpolation_with_perpendicular(points, percent, length=0.2, delta=1e-4, closed=False):
    points_np = np.array(points)
    x, y = points_np[:, 0], points_np[:, 1]
    cumdist = np.insert(np.cumsum(np.sqrt(np.sum(np.diff(points_np, axis=0)**2, axis=1))), 0, 0)
    total_length = cumdist[-1]
    target_length = percent * total_length
    bc_type = 'natural'
    if points[0][0] == points[-1][0] and points[0][1] == points[-1][1] and closed:
        bc_type = 'periodic'
    cs_x = CubicSpline(cumdist, x, bc_type=bc_type)
    cs_y = CubicSpline(cumdist, y, bc_type=bc_type)
    interp_x = cs_x(target_length)
    interp_y = cs_y(target_length)
    interp_point = np.array([interp_x, interp_y])
    point_before = np.array([cs_x(target_length - delta), cs_y(target_length - delta)])
    point_after = np.array([cs_x(target_length + delta), cs_y(target_length + delta)])
    tangent_vector = point_after - point_before
    tangent_vector_normalized = tangent_vector / np.linalg.norm(tangent_vector)
    perpendicular_vector = np.array([-tangent_vector_normalized[1], tangent_vector_normalized[0]])
    start_point = interp_point - perpendicular_vector * (length / 2)
    end_point = interp_point + perpendicular_vector * (length / 2)
    return interp_point, start_point, end_point

def linear_interpolation_with_perpendicular(points, percent, length=0.2):
    points_np = np.array(points)
    cumdist = np.insert(np.cumsum(np.sqrt(np.sum(np.diff(points_np, axis=0)**2, axis=1))), 0, 0)
    total_length = cumdist[-1]
    target_length = percent * total_length
    for i in range(len(cumdist) - 1):
        if cumdist[i] <= target_length <= cumdist[i + 1]:
            break
    t = (target_length - cumdist[i]) / (cumdist[i + 1] - cumdist[i])
    interp_point = (1 - t) * points_np[i] + t * points_np[i + 1]
    direction_vector = points_np[i + 1] - points_np[i]
    direction_vector_normalized = direction_vector / np.linalg.norm(direction_vector)
    perpendicular_vector = np.array([-direction_vector_normalized[1], direction_vector_normalized[0]])
    start_point = interp_point - perpendicular_vector * (length / 2)
    end_point = interp_point + perpendicular_vector * (length / 2)
    return interp_point, start_point, end_point

#%%
# Generate circle points
circle_points = generate_circle_points(1)
circle_points = np.append(circle_points, [circle_points[0]], axis=0)
circle_points
#%%
circle_points = vf.circle(0,0, points=7, end_cap=False)
circle_points = np.array([[x,y] for x,y,_ in circle_points])
circle_points = np.append(circle_points, [circle_points[0]], axis=0)
circle_points

#%%
circle_points[0]

#%%
# Cubic spline interpolation and plot
percent = 0.8
closed = True
cubic_interp_point, cubic_perp_start, cubic_perp_end = cubic_spline_interpolation_with_perpendicular(circle_points, percent, 0.5, closed=closed)
linear_interp_point, linear_perp_start, linear_perp_end = linear_interpolation_with_perpendicular(circle_points, percent, 0.5)

#%%
# Plotting for cubic spline interpolation
plt.figure(figsize=(16, 8))

bc_type='natural'
if circle_points[0][0] == circle_points[-1][0] and circle_points[0][1] == circle_points[-1][1] and closed:
     bc_type = 'periodic'

plt.subplot(1, 2, 1)
plt.plot(circle_points[:, 0], circle_points[:, 1], 'o', label='Control Points')
spline_points = CubicSpline(np.linspace(0, 1, len(circle_points)), circle_points, bc_type=bc_type)(np.linspace(0, 1, 1000)) #'periodic'
plt.plot(spline_points[:, 0], spline_points[:, 1], '-', label='Cubic Spline')
plt.plot(cubic_interp_point[0], cubic_interp_point[1], 'ro', label='Interpolated Point')
plt.plot([cubic_perp_start[0], cubic_perp_end[0]], [cubic_perp_start[1], cubic_perp_end[1]], 'g-', label='Perpendicular Line')
plt.axis('equal')
plt.legend()
plt.title('Cubic Spline Interpolation')

plt.subplot(1, 2, 2)
plt.plot(circle_points[:, 0], circle_points[:, 1], 'o', label='Control Points')
plt.plot([point[0] for point in circle_points], [point[1] for point in circle_points], '-', label='Linear Path')
plt.plot(linear_interp_point[0], linear_interp_point[1], 'ro', label='Linear Interpolated Point')
plt.plot([linear_perp_start[0], linear_perp_end[0]], [linear_perp_start[1], linear_perp_end[1]], 'g-', label='Perpendicular Line')
plt.axis('equal')
plt.legend()
plt.title('Linear Interpolation with Perpendicular Line')

plt.tight_layout()
plt.show()