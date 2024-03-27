"""
Based on https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm

A triangle is stored as a tuple of IDs to corners.
The corners are given in anticlockwise order.
"""

# Importing
import numpy as np
import matplotlib.pyplot as plt
import itertools


class Delaunay():
    
    def __init__(self):

# Initialisation
def add_super_triangle(data, triangles):
    minimum = np.min(points) - 1
    maximum = np.max(points[:, 0] + points[:, 1]) + 5
    super_triangle = get_super_triangle(minimum, maximum)
    data = np.concatenate((super_triangle, points), axis=0)
    triangles.append(np.array([0, 1, 2]))
    return data

def get_super_triangle(minimum, maximum):
    super_triangle_coordinates = np.array([
        [minimum, minimum],
        [maximum, minimum],
        [minimum, maximum]])
    return super_triangle_coordinates


# Iteration part of algorithm
def add_point(point_index, point, triangles):
    bad_triangles = get_bad_triangles(point_index, point, triangles)
    polygon_edges = get_polygon_edges(point_index, bad_triangles)
    filter_triangles(bad_triangles)
    add_new_triangles(point_index, polygon_edges)

# Identifying bad triangles
def get_bad_triangles(index, point):
    bad_triangles = []
    for triangle_index, triangle in enumerate(triangles):
        if triangle_is_bad(triangle, point):
            bad_triangles.append(triangle_index)
    return bad_triangles

# This is based on the formula from the following:
# https://en.wikipedia.org/wiki/Delaunay_triangulation#Algorithms
def triangle_is_bad(triangle, point):
    matrix = get_triangle_matrix(points, triangle)
    determinant = np.linalg.det(matrix)
    triangle_bad = (determinant > 0)
    return triangle_bad

def get_triangle_matrix(points, triangle):
    triangle_points = points[triangle, :]
    x_differences = triangle_points[:, 0] - point[0]
    y_differences = triangle_points[:, 1] - point[1]
    distances = x_differences**2 + y_differences**2
    matrix = np.stack((x_differences, y_differences, distances), axis=1)
    return matrix


# Identifying boundary edges of collection of bad triangles
def get_polygon_edges(index, bad_triangles):
    if len(bad_triangles) > 0:
        return get_polygon_edges_non_trivial(index, bad_triangles)
    else:
        return []

def get_polygon_edges_non_trivial(index, bad_triangles):
    edges = [edge for triangle_index in bad_triangles
             for edge in get_triangle_edges(triangles[triangle_index])]
    edges_distinct = set(edges)
    polygon_edges = [edge for edge in edges_distinct
                     if edges.count(edge) == 1]
    return polygon_edges

def get_triangle_edges(triangle):
    edge_1 = get_triangle_edge(triangle[0], triangle[1])
    edge_2 = get_triangle_edge(triangle[1], triangle[2])
    edge_3 = get_triangle_edge(triangle[2], triangle[0])
    return [edge_1, edge_2, edge_3]

def get_triangle_edge(vertex_1, vertex_2):
    if vertex_1 < vertex_2:
        return (vertex_1, vertex_2)
    else:
        return (vertex_2, vertex_1)


def filter_triangles(bad_triangles):
    global triangles
    triangles = [triangle for triangle_index, triangle in enumerate(triangles)
                 if triangle_index not in bad_triangles]

def add_new_triangles(point_index, polygon_edges):
    global triangles
    for edge in polygon_edges:
        triangle = get_anticlockwise_triangle(point_index, edge)
        triangles.append(triangle)

# This is needed as the check for whether a point is inside the circumcircle
# relies on the circumcircle points being anticlockwise
def get_anticlockwise_triangle(point_index, edge):
    sign = get_triangle_direction(point_index, edge)
    if sign > 0:
        return (point_index, edge[0], edge[1])
    else:
        return (point_index, edge[1], edge[0])

def get_triangle_direction(point_index, edge):
    x1, y1 = points[point_index]
    x2, y2 = points[edge[0]]
    x3, y3 = points[edge[1]]
    dot_product = (y1-y2)*(x3-x1) + (x2-x1)*(y3-y1)
    return (dot_product > 0)

def remove_super_triangle_connecting_triangles(triangles):
    triangles = [triangle for triangle in triangles
                 if min(triangle) > 2]
        

def get_results():
    results = [get_results_triangle(triangle)
               for triangle in triangles]
    return results

def get_results_triangle(triangle):
    centre, radius = get_circumcircle_properties(triangle)
    results_triangle = {"PointIndices": triangle,
                        "Centre": centre,
                        "Radius": radius}
    return results_triangle

# Based on https://en.wikipedia.org/wiki/Circumcircle#Cartesian_coordinates
def get_circumcircle_properties(triangle):
    circle_matrix = get_circle_matrix(triangle)
    a, b, s_x, s_y = get_circle_matrix_determinants(circle_matrix)
    centre, radius = get_circle(a, b, s_x, s_y)

def get_circle_matrix(triangle):
    x, y = points[triangle, 0], points[triangle, 1]
    distance = x**2 + y**2
    ones = np.ones(3)
    matrix = np.stack((distance, x, y, ones), axis=1)
    return matrix

def get_circle_matrix_determinants(circle_matrix):
    a   = np.linalg.det(circle_matrix[:, [1, 2, 3]])
    b   = np.linalg.det(circle_matrix[:, [1, 2, 0]])
    s_x = np.linalg.det(circle_matrix[:, [0, 2, 3]])/2
    s_y = np.linalg.det(circle_matrix[:, [1, 0, 3]])/2
    return a, b, s_x, s_y

def get_circle(a, b, s_x, s_y):
    centre = [s_x/a, s_y/a]
    radius = np.sqrt(b/a + (s_x**2+s_y**2)/a**2)
    return centre, radius


# Plotting
def get_figure():
    fig, ax = plt.subplots(1)
    points = add_super_triangle(points)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    return fig, ax

def plot_points(ax):
    for point in points[3:, :]:
        ax.plot(*point, marker=".")

def plot_triangles(ax):
    for triangle in triangles:
        triangle_points = points[triangle, :]
        ax.add_patch(plt.Polygon(triangle_points, fill=False))

def plot_circles(ax):
    for triangle in results:
        ax.add_patch(plt.Circle(
            triangle["Centre"], triangle["Radius"],
            fill=False, color="#BBBBBB"))

# Problem definition
N = 6
points = np.random.rand(N, 2)*10
triangles = []

for point_index, point in enumerate(points):
    if point_index >= 3:
        add_point(point_index, point, triangles)

remove_super_triangle_connecting_triangles(triangles)
results = get_results()


# Interfacing with plotting functions
"""
fig, ax = get_figure()
plot_points(ax)
plot_triangles(ax)

# Only for verificaion purposes on small problems
plot_circles(ax)
"""














