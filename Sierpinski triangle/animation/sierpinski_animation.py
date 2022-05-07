from manim import *
from numpy import loadtxt
import sys

# import points approximating the fractal (created in sierpinski.jl)
file = open('../points.csv', 'rb')
data = loadtxt(file,delimiter = ",")

# an array of arrays, each entry is a point's coordinate 
points = []

for i in range(len(data[:,0])):
    x = float(data[i,0])
    y = float(data[i,1])

    point = [x,y,0]
    points.append(point)


config.background_color = "#FFFAF9"


class sierpinski(Scene):
    def construct(self):

        # create Axes upon which to plot points (custom ranges, more control over placement, etc.)
        axes = Axes(
            x_range = [0.01, 1.01, 0.1],
            y_range = [0.01, 0.9, 0.1],
            x_length = 12,
            axis_config = {"color": BLACK},
            tips = False,
            y_axis_config = {"numbers_to_include": [0.1,0.2,0.3,0.4, 0.9]}
        )
        axes_labels = axes.get_axis_labels(x_label = "x", y_label = "y").set_color(BLACK)
        axes.get_y_axis().numbers.set_color(BLACK)

        # create VGroup of Dots
        dots = VGroup(*[Dot(point = axes.c2p(point[0],point[1]), color=BLUE, radius=0.01) for point in points])

        # ANIMATIONS
        self.play(DrawBorderThenFill(axes))
        self.wait(0.5)

        # sequentially create each dot
        for i in range(50):
            self.play(Create(dots[i]), run_time = 0.01)


# code from: https://www.reddit.com/r/manim/comments/pfbb36/how_to_animate_scatter_plot_by_plotting_one_point/
class TestAnimation(Scene):
    def construct(self):
        coords = self.return_coords_from_csv("data")    # creates 1D array of arrays (each is a coord location)
        dots = VGroup(*[Dot(point = coord, color=BLUE, radius=0.02) for coord in coords]) # vector group of Dots for each coord

        # ANIMATION (creates each Dot from the dots VGroup)
        for i in range(50):
            self.play(Create(dots[i]))


    # creates 1D array of arrays (each is a coord location)
    def return_coords_from_csv(self,file_name):
        import csv
        coords = []
        with open(f'../points.csv', 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                x,y = row
                coord = [float(x),float(y),0]
                coords.append(coord)
        csvFile.close()
        return coords