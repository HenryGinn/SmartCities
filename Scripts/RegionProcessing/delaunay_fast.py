"""
Based on https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm

A triangle is stored as a tuple of IDs to corners.
The corners are given in anticlockwise order.

The original naive implementation was O(n^2), and this implementation
aims to be faster. All the points need to be added so it is at least
O(n), and the speed increase comes from a better way of finding bad
triangles.

This fast implementation does not check all the triangles when finding
triangles where the new point is inside their circumcentre. Once a bad
triangle has been identified, the triangles connected to it are added
to the set of potentially bad triangles. These are then tested, adding
to the set as it is explored, until all potentially bad triangles have
been explored. Roughly, this is guaranteed to find all bad triangles as
if the new point was contained in the circumcircle and the circle was
not connected to any other bad triangles, then that would contradict
the fact that the previous triangulation was a valid Delaunay
triangulation.

To find an initial triangle we cannot find the nearest points by
computing distances, and then checking triangles involving those points.
This would be O(n) which is too slow, and for N = 250,000 this step
alone would take over 6 hours. Instead the points will be added in a
precomputed order where previously added points are nearby.
"""

# Importing
import numpy as np
import matplotlib.pyplot as plt


class Delaunay():
    
    def __init__(self, points):
        self.points = points
        self.triangles = []
        self.add_super_triangle()
    
    def triangulate(self):
        for point_index, point in enumerate(self.points):
            if point_index >= 3:
                self.add_point(point_index, point)
        self.remove_super_triangle()
        self.set_results()
    
    # Initialisation
    def add_super_triangle(self):
        minimum = np.min(self.points) - 1
        maximum = np.max(self.points[:, 0] + self.points[:, 1]) + 5
        super_triangle = self.get_super_triangle(minimum, maximum)
        self.points = np.concatenate((super_triangle, self.points), axis=0)
        self.triangles.append(np.array([0, 1, 2]))
    
    def get_super_triangle(self, minimum, maximum):
        super_triangle_coordinates = np.array([
            [minimum, minimum],
            [maximum, minimum],
            [minimum, maximum]])
        return super_triangle_coordinates
    
    
    # Iteration part of algorithm
    def add_point(self, point_index, point):
        self.set_bad_triangles(point_index, point)
        self.set_polygon_edges(point_index)
        self.filter_triangles()
        self.add_new_triangles(point_index)
    
    # Identifying bad triangles
    def set_bad_triangles(self, index, point):
        self.bad_triangles = []
        for triangle_index, triangle in enumerate(self.triangles):
            if self.triangle_is_bad(triangle, point):
                self.bad_triangles.append(triangle_index)
    
    # This is based on the formula from the following:
    # https://en.wikipedia.org/wiki/Delaunay_triangulation#Algorithms
    def triangle_is_bad(self, triangle, point):
        matrix = self.get_triangle_matrix(triangle, point)
        determinant = np.linalg.det(matrix)
        triangle_bad = (determinant > 0)
        return triangle_bad
    
    def get_triangle_matrix(self, triangle, point):
        triangle_points = self.points[triangle, :]
        x_differences = triangle_points[:, 0] - point[0]
        y_differences = triangle_points[:, 1] - point[1]
        distances = x_differences**2 + y_differences**2
        matrix = np.stack((x_differences, y_differences, distances), axis=1)
        return matrix
    
    
    # Identifying boundary edges of collection of bad triangles
    def set_polygon_edges(self, index):
        if len(self.bad_triangles) > 0:
            self.set_polygon_edges_non_trivial(index)
        else:
            self.polygon_edges = []
    
    def set_polygon_edges_non_trivial(self, index):
        edges = [edge for triangle_index in self.bad_triangles
                 for edge in self.get_triangle_edges(self.triangles[triangle_index])]
        edges_distinct = set(edges)
        self.polygon_edges = [edge for edge in edges_distinct
                              if edges.count(edge) == 1]
    
    def get_triangle_edges(self, triangle):
        edge_1 = self.get_triangle_edge(triangle[0], triangle[1])
        edge_2 = self.get_triangle_edge(triangle[1], triangle[2])
        edge_3 = self.get_triangle_edge(triangle[2], triangle[0])
        return [edge_1, edge_2, edge_3]
    
    def get_triangle_edge(self, vertex_1, vertex_2):
        if vertex_1 < vertex_2:
            return (vertex_1, vertex_2)
        else:
            return (vertex_2, vertex_1)
    
    
    def filter_triangles(self):
        self.triangles = [
            triangle for triangle_index, triangle in enumerate(self.triangles)
            if triangle_index not in self.bad_triangles]
    
    def add_new_triangles(self, point_index):
        for edge in self.polygon_edges:
            triangle = self.get_anticlockwise_triangle(point_index, edge)
            self.triangles.append(triangle)
    
    # This is needed as the check for whether a point is inside the circumcircle
    # relies on the circumcircle points being anticlockwise
    def get_anticlockwise_triangle(self, point_index, edge):
        sign = self.get_triangle_direction(point_index, edge)
        if sign > 0:
            return (point_index, edge[0], edge[1])
        else:
            return (point_index, edge[1], edge[0])
    
    def get_triangle_direction(self, point_index, edge):
        x1, y1 = self.points[point_index]
        x2, y2 = self.points[edge[0]]
        x3, y3 = self.points[edge[1]]
        dot_product = (y1-y2)*(x3-x1) + (x2-x1)*(y3-y1)
        return (dot_product > 0)
    
    def remove_super_triangle(self):
        self.points = self.points[3:, :]
        self.remove_super_triangle_connecting_triangles()
        self.shift_point_indices()
    
    def remove_super_triangle_connecting_triangles(self):
        self.triangles = [triangle for triangle in self.triangles
                          if min(triangle) > 2]
    
    def shift_point_indices(self):
        self.triangles = [tuple(np.array(triangle) - 3)
                          for triangle in self.triangles]
            
    
    def set_results(self):
        self.results = [self.get_results_triangle(triangle)
                        for triangle in self.triangles]
    
    def get_results_triangle(self, triangle):
        centre, radius = self.get_circumcircle_properties(triangle)
        results_triangle = {"PointIndices": triangle,
                            "Centre": centre,
                            "Radius": radius}
        return results_triangle
    
    # Based on https://en.wikipedia.org/wiki/Circumcircle#Cartesian_coordinates
    def get_circumcircle_properties(self, triangle):
        circle_matrix = self.get_circle_matrix(triangle)
        a, b, s_x, s_y = self.get_circle_matrix_determinants(circle_matrix)
        centre, radius = self.get_circle(a, b, s_x, s_y)
        return centre, radius
    
    def get_circle_matrix(self, triangle):
        x, y = self.points[triangle, 0], self.points[triangle, 1]
        distance = x**2 + y**2
        ones = np.ones(3)
        matrix = np.stack((distance, x, y, ones), axis=1)
        return matrix
    
    def get_circle_matrix_determinants(self, circle_matrix):
        a   = np.linalg.det(circle_matrix[:, [1, 2, 3]])
        b   = np.linalg.det(circle_matrix[:, [1, 2, 0]])
        s_x = np.linalg.det(circle_matrix[:, [0, 2, 3]])/2
        s_y = np.linalg.det(circle_matrix[:, [1, 0, 3]])/2
        return a, b, s_x, s_y
    
    def get_circle(self, a, b, s_x, s_y):
        centre = [s_x/a, s_y/a]
        radius = np.sqrt(b/a + (s_x**2+s_y**2)/a**2)
        return centre, radius
    
    
    # Plotting
    def set_figure(self):
        if not hasattr(self, "ax"):
            self.fig, self.ax = plt.subplots(1)
        
    def plot_all(self):
        self.set_figure()
        self.plot_points()
        self.plot_triangles()
        self.plot_circles()
        self.set_plot_limits()
    
    def plot_points(self):
        for point in self.points[3:, :]:
            self.ax.plot(*point, marker=".")
    
    def plot_triangles(self):
        for triangle in self.triangles:
            triangle_points = self.points[triangle, :]
            self.ax.add_patch(plt.Polygon(triangle_points, fill=False))
    
    def plot_circles(self):
        for triangle in self.results:
            self.ax.add_patch(plt.Circle(
                triangle["Centre"], triangle["Radius"],
                fill=False, color="#BBBBBB"))

    def set_plot_limits(self):
        min_x, max_x = self.get_plot_bounds(0)
        min_y, max_y = self.get_plot_bounds(1)
        difference = max(max_x - min_x, max_y - min_y)
        max_x, max_y = min_x + difference, min_y + difference
        self.ax.set_xlim(min_x, max_x)
        self.ax.set_ylim(min_y, max_y)
        plt.gca().set_aspect('equal')
    
    def get_plot_bounds(self, dimension):
        values = list(self.points[:, dimension])
        minimum, maximum = min(values), max(values)
        buffer = (maximum - minimum)/10
        minimum, maximum = minimum - buffer, maximum + buffer
        return minimum, maximum
