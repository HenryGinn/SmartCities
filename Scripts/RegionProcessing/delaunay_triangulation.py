"""
Based on https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm

A triangle is stored as a tuple of IDs to corners.
The corners are given in anticlockwise order.
"""


import numpy as np
import matplotlib.pyplot as plt

N = 5
points = np.random.rand(N, 2)*10
triangles = []

def add_super_triangle(data):
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

def plot_points():
    for point in points[3:, :]:
        ax.plot(*point, marker=".")

def plot_triangles():
    for triangle in triangles:
        triangle_points = points[triangle, :]
        ax.add_patch(plt.Polygon(triangle_points, fill=False))


def add_point(point_index, point):
    bad_triangles = get_bad_triangles(point_index, point)
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

def remove_super_triangle_connecting_triangles():
    global triangles
    triangles = [triangle for triangle in triangles
                 if min(triangle) > 2]

fig, ax = plt.subplots(1)
points = add_super_triangle(points)

for point_index, point in enumerate(points):
    if point_index >= 3:
        add_point(point_index, point)

remove_super_triangle_connecting_triangles()
plot_points()
plot_triangles()
















