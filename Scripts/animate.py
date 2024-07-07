import imageio

class Animate():

    def __init__(self, base_path):
        self.base_path = base_path
    
    def create_animation(self):
        self.set_path_gif()
        with imageio.get_writer(self.path_gif, mode='I') as writer:
            for filename in self.filenames:
                image = imageio.imread(filename)
                writer.append_data(image)

    def set_path_gif(self):
        self.path_gif = os.path.join(self.path_output, name)
