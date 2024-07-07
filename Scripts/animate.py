class Animate():

    def __init__(self, crime, path):
        self.crime = crime
        self.path = path
    
    def create_animation(self):
        self.set_path_gif()
        with imageio.get_writer(self.path_gif, mode='I') as writer:
            for filename in self.filenames:
                image = imageio.imread(filename)
                writer.append_data(image)

    def set_path_gif(self):
        self.crime.month = "All"
        self.crime.year = "All"
        self.crime.plot_obj.do_set_name()
        name = f"{self.crime.plot_obj.name}.gif"
        self.path_gif = os.path.join(self.path_output, name)
