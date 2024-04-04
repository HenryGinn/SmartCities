"""
This algorithm starts by finding the extreme points to determine the
box that the curve will fill. For each point it determines which
quadrant it is in, records the result, and then increases the order
and repeats. This means the algorithm is linear in the maximum order
and the number of points.

Each point of the curve is defined as a list giving instructions on
which quadrant the point is in within the previous quadrant. The
quadrant number increases along the curve. This list can be read as
a base 4 number by which the points are ordered.

Each U shape has an orientation defined below. Note that these
correspond to the descriptions on Wikipedia
https://en.wikipedia.org/wiki/Hilbert_curve#/media/
File:Hilbert_curve_production_rules!.svg
A: bottom left, top left, top right, bottom right (gap at bottom)
B: top right, top left, bottom left, bottom right (gap at right)
C: top right, bottom right, bottom left, top left (gap at top)
D: bottom left, bottom right, top right, top left (gap at left)
"""


import numpy as np
import hgutilities.defaults as defaults

class Hilbert():

    def __init__(self, data, maximum_order=5):
        self.data = data
        self.maximum_order = maximum_order
        self.set_bounds()

    def set_bounds(self):
        minima = np.min(self.data, axis=0)
        maxima = np.max(self.data, axis=0)
        self.size = np.max(maxima - minima)
        self.min_x, self.min_y = minima
        self.max_x, self.max_y = minima + self.size

    def sort(self):
        self.place_points_on_curve()

    def place_points_on_curve(self):
        for position in self.data:
            point = Point(self, position)
            self.place_point_on_curve(point)
            print(f"{point.index}\n")

    def place_point_on_curve(self, point):
        for order in range(self.maximum_order):
            point.place_point_in_quadrant()
            

class Point():

    def __init__(self, hilbert, position):
        self.position = tuple(position)
        self.set_initial_quadrant_bounds(hilbert)
        self.index = []
        self.orientation = "C"

    @classmethod
    def set_place_in_quadrant_functions(cls):
        cls.place_in_quadrant_functions = {
            **cls.get_place_in_quadrant_functions_A(),
            **cls.get_place_in_quadrant_functions_B(),
            **cls.get_place_in_quadrant_functions_C(),
            **cls.get_place_in_quadrant_functions_D()}

    @classmethod
    def set_place_in_quadrant_functions_A(cls):
        return {
            ("A", True, True):   cls.place_in_quadrant_from_A_top_right,
            ("A", True, False):  cls.place_in_quadrant_from_A_bottom_right,
            ("A", False, True):  cls.place_in_quadrant_from_A_top_left,
            ("A", False, False): cls.place_in_quadrant_from_A_bottom_left}

    @classmethod
    def set_place_in_quadrant_functions_B(cls):
        return {
            ("B", True, True):   cls.place_in_quadrant_from_B_top_right,
            ("B", True, False):  cls.place_in_quadrant_from_B_bottom_right,
            ("B", False, True):  cls.place_in_quadrant_from_B_top_left,
            ("B", False, False): cls.place_in_quadrant_from_B_bottom_left}

    @classmethod
    def set_place_in_quadrant_functions_C(cls):
        return {
            ("C", True, True):   cls.place_in_quadrant_from_C_top_right,
            ("C", True, False):  cls.place_in_quadrant_from_C_bottom_right,
            ("C", False, True):  cls.place_in_quadrant_from_C_top_left,
            ("C", False, False): cls.place_in_quadrant_from_C_bottom_left}

    @classmethod
    def set_place_in_quadrant_functions_D(cls):
        return {
            ("D", True, True):   cls.place_in_quadrant_from_D_top_right,
            ("D", True, False):  cls.place_in_quadrant_from_D_bottom_right,
            ("D", False, True):  cls.place_in_quadrant_from_D_top_left,
            ("D", False, False): cls.place_in_quadrant_from_D_bottom_left}

    def set_initial_quadrant_bounds(self, hilbert):
        attributes = ["min_x", "max_x", "min_y", "max_y"]
        defaults.inherit(self, hilbert, attributes)

    def place_point_in_quadrant(self):
        midpoint_x, midpoint_y = self.get_midpoints()
        quadrant_tuple = self.get_quadrant_tuple(midpoint_x, midpoint_y)
        placing_function = (
            self.place_in_quadrant_functions[quadrant_tuple])
        placing_function(self, midpoint_x, midpoint_y)

    def get_quadrant_tuple(self, midpoint_x, midpoint_y):
        is_right = (midpoint_x > self.position[0])
        is_top =   (midpoint_y > self.position[1])

    def get_midpoints(self):
        midpoint_x = (self.min_x + self.max_x) / 2
        midpoint_y = (self.min_y + self.max_y) / 2
        return midpoint_x, midpoint_y

    def place_in_quadrant_from_A_top_right(self, midpoint_x, midpoint_y):
        print("A")

    def place_in_quadrant_from_A_bottom_right(self, midpoint_x, midpoint_y):
        print("A")

    def place_in_quadrant_from_A_top_left(self, midpoint_x, midpoint_y):
        print("A")

    def place_in_quadrant_from_A_bottom_left(self, midpoint_x, midpoint_y):
        print("A")

    def place_in_quadrant_from_B_top_right(self, midpoint_x, midpoint_y):
        print("B")

    def place_in_quadrant_from_B_bottom_right(self, midpoint_x, midpoint_y):
        print("B")

    def place_in_quadrant_from_B_top_left(self, midpoint_x, midpoint_y):
        print("B")

    def place_in_quadrant_from_B_bottom_left(self, midpoint_x, midpoint_y):
        print("B")

    def place_in_quadrant_from_C_top_right(self, midpoint_x, midpoint_y):
        print("C")

    def place_in_quadrant_from_C_bottom_right(self, midpoint_x, midpoint_y):
        print("C")

    def place_in_quadrant_from_C_top_left(self, midpoint_x, midpoint_y):
        print("C")

    def place_in_quadrant_from_C_bottom_left(self, midpoint_x, midpoint_y):
        print("C")

    def place_in_quadrant_from_D_top_right(self, midpoint_x, midpoint_y):
        print("D")

    def place_in_quadrant_from_D_bottom_right(self, midpoint_x, midpoint_y):
        print("D")

    def place_in_quadrant_from_D_top_left(self, midpoint_x, midpoint_y):
        print("D")

    def place_in_quadrant_from_D_bottom_left(self, midpoint_x, midpoint_y):
        print("D")

Point.set_place_in_quadrant_functions()

N = 5
data = np.random.rand(N, 2)
hilbert = Hilbert(data)
hilbert.sort()
