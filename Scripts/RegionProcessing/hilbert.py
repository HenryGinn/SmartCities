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
import time
import matplotlib.pyplot as plt

class Hilbert():

    def __init__(self, data, maximum_order=5):
        self.data = data
        self.maximum_order = maximum_order
        self.set_bounds()
        self.initialise_indices()

    def set_bounds(self):
        minima = np.min(self.data, axis=0)
        maxima = np.max(self.data, axis=0)
        self.size = np.max(maxima - minima)
        self.min_x, self.min_y = minima
        self.max_x, self.max_y = minima + self.size

    def print_bounds(self):
        print(f"Mininum x: {self.min_x}\n"
              f"Maximum x: {self.max_x}\n"
              f"Mininum y: {self.min_y}\n"
              f"Maximum y: {self.max_y}\n")

    def initialise_indices(self):
        self.indices = {tuple(position): ""
                        for position in self.data}

    def sort(self):
        self.find_hilbert_indices()
        self.sort_data()

    def find_hilbert_indices(self):
        for position in self.data:
            point = Point(self, position)
            self.place_point_on_curve(point)
            self.indices[tuple(position)] = point.index

    def place_point_on_curve(self, point):
        for order in range(self.maximum_order):
            point.place_point_in_quadrant()

    def sort_data(self):
        sorting_function = lambda position: self.indices[tuple(position)]
        self.sorted_data = sorted(self.data, key=sorting_function)
        self.sorted_data = np.array(self.sorted_data)

class Point():

    @classmethod
    def set_place_in_quadrant_functions(cls):
        cls.place_in_quadrant_functions = {
            **cls.set_place_in_quadrant_functions_A(),
            **cls.set_place_in_quadrant_functions_B(),
            **cls.set_place_in_quadrant_functions_C(),
            **cls.set_place_in_quadrant_functions_D()}

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


    def __init__(self, hilbert, position):
        self.position = tuple(position)
        self.set_initial_quadrant_bounds(hilbert)
        self.index = ""
        self.orientation = "C"

    def set_initial_quadrant_bounds(self, hilbert):
        attributes = ["min_x", "max_x", "min_y", "max_y"]
        defaults.inherit(self, hilbert, attributes)

    def place_point_in_quadrant(self):
        midpoint_x, midpoint_y = self.get_midpoints()
        quadrant_tuple = self.get_quadrant_tuple(midpoint_x, midpoint_y)
        placing_function = (
            self.place_in_quadrant_functions[quadrant_tuple])
        placing_function(self, midpoint_x, midpoint_y)
        self.update_bounds(quadrant_tuple, midpoint_x, midpoint_y)

    def get_quadrant_tuple(self, midpoint_x, midpoint_y):
        is_right = (midpoint_x < self.position[0])
        is_top =   (midpoint_y < self.position[1])
        quadrant_tuple = (self.orientation, is_right, is_top)
        return quadrant_tuple

    def get_midpoints(self):
        midpoint_x = (self.min_x + self.max_x) / 2
        midpoint_y = (self.min_y + self.max_y) / 2
        return midpoint_x, midpoint_y

    def place_in_quadrant_from_A_top_right(self, midpoint_x, midpoint_y):
        self.index += "2"
        self.orientation = "A"

    def place_in_quadrant_from_A_bottom_right(self, midpoint_x, midpoint_y):
        self.index += "3"
        self.orientation = "B"

    def place_in_quadrant_from_A_top_left(self, midpoint_x, midpoint_y):
        self.index += "1"
        self.orientation = "A"

    def place_in_quadrant_from_A_bottom_left(self, midpoint_x, midpoint_y):
        self.index += "0"
        self.orientation = "D"

    def place_in_quadrant_from_B_top_right(self, midpoint_x, midpoint_y):
        self.index += "0"
        self.orientation = "C"

    def place_in_quadrant_from_B_bottom_right(self, midpoint_x, midpoint_y):
        self.index += "3"
        self.orientation = "A"

    def place_in_quadrant_from_B_top_left(self, midpoint_x, midpoint_y):
        self.index += "1"
        self.orientation = "B"

    def place_in_quadrant_from_B_bottom_left(self, midpoint_x, midpoint_y):
        self.index += "2"
        self.orientation = "B"

    def place_in_quadrant_from_C_top_right(self, midpoint_x, midpoint_y):
        self.index += "0"
        self.orientation = "B"

    def place_in_quadrant_from_C_bottom_right(self, midpoint_x, midpoint_y):
        self.index += "1"
        self.orientation = "C"

    def place_in_quadrant_from_C_top_left(self, midpoint_x, midpoint_y):
        self.index += "3"
        self.orientation = "D"

    def place_in_quadrant_from_C_bottom_left(self, midpoint_x, midpoint_y):
        self.index += "2"
        self.orientation = "C"

    def place_in_quadrant_from_D_top_right(self, midpoint_x, midpoint_y):
        self.index += "2"
        self.orientation = "D"

    def place_in_quadrant_from_D_bottom_right(self, midpoint_x, midpoint_y):
        self.index += "1"
        self.orientation = "D"

    def place_in_quadrant_from_D_top_left(self, midpoint_x, midpoint_y):
        self.index += "3"
        self.orientation = "C"

    def place_in_quadrant_from_D_bottom_left(self, midpoint_x, midpoint_y):
        self.index += "0"
        self.orientation = "A"

    def update_bounds(self, quadrant_tuple, midpoint_x, midpoint_y):
        self.update_x_bound(quadrant_tuple[1], midpoint_x)
        self.update_y_bound(quadrant_tuple[2], midpoint_y)

    def update_x_bound(self, is_right, midpoint_x):
        if is_right:
            self.min_x = midpoint_x
        else:
            self.max_x = midpoint_x

    def update_y_bound(self, is_top, midpoint_y):
        if is_top:
            self.min_y = midpoint_y
        else:
            self.max_y = midpoint_y

Point.set_place_in_quadrant_functions()

def sort_full_grid(n, N):
    data = np.array([(i, j) for i in range(N) for j in range(N)])
    hilbert = Hilbert(data, maximum_order=n)
    hilbert.min_x = hilbert.min_x - 0.5
    hilbert.min_y = hilbert.min_y - 0.5
    hilbert.max_x = hilbert.max_x + 0.5
    hilbert.max_y = hilbert.max_y + 0.5
    hilbert.sort()
    return hilbert

hilbert = sort_full_grid(5, 2**5)
x = hilbert.sorted_data[:, 0]
y = hilbert.sorted_data[:, 1]
plt.plot(x, y)
plt.show()
