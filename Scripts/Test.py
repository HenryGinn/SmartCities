import os
import imageio

path = "/media/henry/DATA/Documents/Python/SmartCities/Output/Per 100k/Boroughs/Westminster/Crime: Major Categories/Theft/All"
file_paths = [os.path.join(path, filename)
              for filename in os.listdir(path)]

path_gif = os.path.join(path, "Gif.gif")

images = []
for file_path in file_paths:
    images.append(imageio.imread(file_path))

imageio.mimsave(path_gif, images)
