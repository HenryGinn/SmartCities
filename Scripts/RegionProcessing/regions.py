import os

#import matplotlib.pyplot as plt
import numpy as np

#from voronoi import Voronoi

def read_from_path(path, separater="\t", skip_first_n=0):
    with open(path, "r") as file:
        skip_first_lines(file, skip_first_n)
        keys = file.readline().strip("% \n").split(separater)
        values = get_data_from_file(file, separater)
        return dict(zip(keys, values))

def skip_first_lines(file, skip_first_n):
    for line_number in range(skip_first_n):
        file.readline()

def get_data_from_file(file, separater):
    rows = [[number
             for number in line.strip().split(separater)]
            for line in file]
    columns = [np.array(column) for column in zip(*rows)]
    return columns

regions = [
    "en", "wd", "ub", "ha", "tw", "kt", "sm", "cr", "br", "da", "rm", "ig",
    "n", "e", "s", "w", "ec", "wc", "nw", "sw", "se"]

path = os.path.abspath(os.path.dirname(__file__))
path = os.path.dirname(os.path.dirname(os.path.dirname(path)))
base_path = os.path.join(path, "Data", "Postcodes", "Data")

postcode_counts = {}

for region in regions:
    postcode_path = os.path.join(base_path, f"{region}.csv")
    data = read_from_path(postcode_path)
    postcode_count = len(data[list(data.keys())[0]])
    postcode_counts.update({region: postcode_count})

for key, value in postcode_counts.items():
    print(f"{key}: {value}")

total = sum(list(postcode_counts.values()))
print(f"Total: {total}")