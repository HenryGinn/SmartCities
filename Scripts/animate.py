import os
import io

import imageio
import PIL
import matplotlib.pyplot as plt

class Animate():

    def __init__(self, plotter):
        self.plotter = plotter
        self.plotter.format = "png"
        self.path_gif = f"{os.path.split(self.plotter.path_output)[0]}.gif"
    
    def create_animation(self):
        frames = self.get_frames()
        self.save_animation(frames)

    def get_frames(self):
        frames = [self.get_frame(time, index)
                  for index, time in enumerate(self.plotter.time_columns)]
        return frames

    def get_frame(self, time, index):
        print(time)
        buffer = self.get_buffer(time, index)
        image = self.get_image(buffer).copy()
        plt.close()
        return image

    def get_buffer(self, time, index):
        self.plotter.create_plot_time(time)
        buffer = io.BytesIO()
        return buffer

    def get_image(self, buffer):
        plt.savefig(buffer, bbox_inches="tight", pad_inches=self.plotter.crime.plot_obj.pad_inches)
        buffer.seek(0)
        image = PIL.Image.open(buffer)
        return image

    def save_animation(self, frames):
        frames[0].save(self.path_gif, loop=False, save_all=True,
                       append_images=frames[1:])
