"""
This is based on the following article:
https://en.wikipedia.org/wiki/Delaunay_triangulation#Relationship_with_the_Voronoi_diagram
"""


import numpy as np
import matplotlib.pyplot as plt

from delaunay_triangulation import Delaunay


class Voronoi():
    
    def __init__(self, points):
        self.points = points
        self.point_count = points.shape[0]
        self.delaunay = Delaunay(points)
    
    def construct_polygons(self):
        self.delaunay.triangulate()
        self.triangulation = self.delaunay.results
        self.set_maps()
        self.set_polygon_points()
    
    def set_maps(self):
        self.set_point_to_edges_map()
        self.set_edge_to_triangles_map()
    
    def set_point_to_edges_map(self):
        self.initialise_point_to_edges_map()
        for triangle in self.triangulation:
            self.add_edges_to_point_to_edges_map(triangle)
    
    def initialise_point_to_edges_map(self):
        self.point_to_edges = {point_index: []
                               for point_index, _ in enumerate(self.points)}
    
    def add_edges_to_point_to_edges_map(self, triangle):
        p1, p2, p3 = triangle["PointIndices"]
        self.add_edge_pair_to_point_to_edges_map(p1, p2, p3)
        self.add_edge_pair_to_point_to_edges_map(p2, p1, p3)
        self.add_edge_pair_to_point_to_edges_map(p3, p1, p2)
    
    def add_edge_pair_to_point_to_edges_map(self, p1, p2, p3):
        self.add_edge_to_point_edges_map(p1, p2)
        self.add_edge_to_point_edges_map(p1, p3)
    
    def add_edge_to_point_edges_map(self, p1, p2):
        p_min = min(p1, p2)
        p_max = max(p1, p2)
        self.point_to_edges[p1].append((p_min, p_max))
    
    def set_edge_to_triangles_map(self):
        self.edge_to_triangles = {}
        for triangle_index, triangle in enumerate(self.triangulation):
            points = triangle["PointIndices"]
            self.add_edges_to_map(triangle_index, points)
    
    def add_edges_to_map(self, triangle_index, points):
        self.add_edge_to_map(triangle_index, points[0], points[1])
        self.add_edge_to_map(triangle_index, points[1], points[2])
        self.add_edge_to_map(triangle_index, points[2], points[0])
    
    def add_edge_to_map(self, triangle_index, point_1, point_2):
        key = self.get_edge_to_map_key(point_1, point_2)
        if key in self.edge_to_triangles:
            self.edge_to_triangles[key].append(triangle_index)
        else:
            self.edge_to_triangles.update({key: [triangle_index]})
    
    def get_edge_to_map_key(self, point_1, point_2):
        point_A = min(point_1, point_2)
        point_B = max(point_1, point_2)
        key = (point_A, point_B)
        return key

    
    def set_polygon_points(self):
        self.initialise_point_to_triangles_map()
        for point_index in range(self.point_count):
            self.find_polygon(point_index)
            self.process_polygon(point_index)
    
    def initialise_point_to_triangles_map(self):
        self.point_to_triangles = {
            point_index: [] for point_index in range(self.point_count)}
    
    # The extra iteration is for invalid polygon detection
    def find_polygon(self, point_index):
        working_edge = self.point_to_edges[point_index][0]
        working_triangle = self.get_initial_triangle(working_edge, point_index)
        for triangle_index in range(len(self.point_to_edges[point_index])//2 + 1):
            working_triangle, working_edge = self.add_triangle_to_polygon(
                point_index, working_triangle, working_edge)
    
    def get_initial_triangle(self, initial_edge, point_index):
        triangles = self.edge_to_triangles[initial_edge]
        if len(triangles) == 1:
            return triangles[0]
        else:
            return self.get_anticlockwise_triangle(
                triangles, initial_edge, point_index)
    
    def get_anticlockwise_triangle(self, triangles, initial_edge, point_index):
        if self.is_anticlockwise_triangle(triangles[0], initial_edge, point_index):
            return triangles[0]
        else:
            return triangles[1]
    
    def is_anticlockwise_triangle(self, triangle_index, initial_edge, point_index):
        non_centre_point = [index for index in initial_edge
                            if index != point_index][0]
        oriented_edge = (point_index, non_centre_point)
        point_indices = self.triangulation[triangle_index]["PointIndices"]
        return self.is_anticlockwise(point_indices, oriented_edge)
    
    def is_anticlockwise(self, point_indices, oriented_edge):
        anticlockwise = (
            (point_indices[0], point_indices[1]) == oriented_edge or
            (point_indices[1], point_indices[2]) == oriented_edge or
            (point_indices[2], point_indices[0]) == oriented_edge)
        return anticlockwise
    
    def add_triangle_to_polygon(self, point_index, working_triangle, working_edge):
        new_working_edge = self.get_updated_working_edge(
            point_index, working_triangle, working_edge)
        new_working_triangle = self.get_new_working_triangle(new_working_edge, working_triangle)
        self.point_to_triangles[point_index].append(new_working_triangle)
        return new_working_triangle, new_working_edge
    
    def get_updated_working_edge(self, point_index, working_triangle, working_edge):
        edges = self.get_triangle_edges(working_triangle)
        updated_working_edge = [edge for edge in edges
                                if (point_index in edge and
                                    edge != working_edge)][0]
        return updated_working_edge
    
    def get_triangle_edges(self, working_triangle):
        points = self.triangulation[working_triangle]["PointIndices"]
        edges = [(min(points[0], points[1]), max(points[0], points[1])),
                 (min(points[1], points[2]), max(points[1], points[2])),
                 (min(points[2], points[0]), max(points[2], points[0]))]
        return edges
    
    def get_new_working_triangle(self, new_working_edge, working_triangle):
        triangles = self.edge_to_triangles[new_working_edge]
        possible_triangles = [triangle for triangle in triangles
                              if triangle != working_triangle]
        if len(possible_triangles) == 1:
            return possible_triangles[0]
        else:
            return working_triangle # This is for edge case detection
    
    # This is a horrible way of dealing with edge cases
    # Non-internal edges are ignored
    def process_polygon(self, point_index):
        if self.polygon_is_valid(point_index):
            self.point_to_triangles[point_index] = self.point_to_triangles[point_index][:-1]
        else:
            self.point_to_triangles[point_index] = None
    
    def polygon_is_valid(self, point_index):
        triangles = self.point_to_triangles[point_index]
        difference_iterable = zip(triangles[1:], triangles)
        differences = [triangle_2 - triangle_1
                       for triangle_1, triangle_2 in difference_iterable]
        return (0 not in differences)
    
    def plot(self):
        self.set_figure()
        self.plot_polygons()
        self.plot_points()
        self.delaunay.set_plot_limits(self.ax)
    
    def set_figure(self):
        if not hasattr(self, "ax"):
            self.fig, self.ax = plt.subplots(1)
    
    def plot_polygons(self):
        for point_index, triangle_indices in self.point_to_triangles.items():
            if triangle_indices is not None:
                self.plot_polygon(triangle_indices)
    
    def plot_polygon(self, triangle_indices):
        coordinates = [self.triangulation[triangle_index]["Centre"]
                       for triangle_index in triangle_indices]
        coordinates = np.array(coordinates)
        polygon = plt.Polygon(coordinates, fill=False, color="black")
        self.ax.add_patch(polygon)
    
    def plot_points(self):
        for point in self.points:
            self.ax.plot(*point, color="dodgerblue", marker="o")
    
    def save_figure(self, format="pdf"):
        plt.savefig(f"VoronoiDiagram.{format}", format=format, pad_inches=True)

points = np.array([
    [0, 0],
    [5, 0],
    [3, 2],
    [9, 1],
    [-1, 5],
    [6, 6],
    [10, 6],
    [8, 11],
    [10, 12],
    [3, 13]])
