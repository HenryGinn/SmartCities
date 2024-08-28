from os.path import split, join
import io

import imageio
import PIL
import matplotlib.pyplot as plt
from hgutilities import utils


class Animate():

    def __init__(self, plotter):
        self.plotter = plotter
        self.crime = plotter.crime
        self.set_path_fig()

    def set_path_fig(self):
        self.set_gif_name()
        self.path_base = split(self.plotter.path_output)[0]
        self.path_gif = join(self.path_base, f"{self.gif_name}.gif")
        utils.make_folder(self.path_base)

    def set_gif_name(self):
        self.gif_name = utils.get_file_name({
            "Region": split(self.plotter.path_region)[1],
            "Crime": split(self.plotter.path_crime)[1],
            "Time": self.plotter.time}, timestamp=False)
        print(self.gif_name)
    
    def create_animation(self):
        frames = self.get_frames()
        self.save_animation(frames)

    def get_frames(self):
        frames = [self.get_frame(time, index)
                  for index, time in enumerate(self.plotter.time_columns)]
        return frames

    def get_frame(self, time, index):
        buffer = self.get_buffer(time, index)
        image = self.get_image(buffer).copy()
        plt.close()
        return image

    def get_buffer(self, time, index):
        self.plotter.kwargs["animate"] = True
        self.plotter.create_plot_time(
            time, format="png", output=None)
        buffer = io.BytesIO()
        return buffer

    def get_image(self, buffer):
        plt.savefig(buffer, bbox_inches="tight",
                    pad_inches=self.crime.plot_obj.pad_inches)
        buffer.seek(0)
        image = PIL.Image.open(buffer)
        return image

    def save_animation(self, frames):
        frames[0].save(self.path_gif, loop=False, save_all=True,
                       append_images=frames[1:])
