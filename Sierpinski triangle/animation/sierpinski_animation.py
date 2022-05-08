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
myBlue = "#001A33"


class sierpinski(Scene):
    def construct(self):

        title_card = Text(
            " approximating the sierpinski\ntriangle using the chaos game", 
            font_size = 40,
            color = myBlue, 
            font = "BITSTREAM VERA SERIF",
            line_spacing = 1,
            should_center = True
        )

        # create Axes upon which to plot points (custom ranges, more control over placement, etc.)
        axes = Axes(
            x_range = [0.0, 1.01, 0.1],
            y_range = [0.0, 0.9, 0.1],
            x_length = 8,
            axis_config = {"color": "#FFFAF9"},
            tips = False,
            y_axis_config = {"numbers_to_include": [0.1, 0.9]}
        )
        # axes_labels = axes.get_axis_labels(x_label = "x", y_label = "y").set_color(BLACK)
        # axes.get_y_axis().numbers.set_color(BLACK)

        # create VGroup of Dots
        dots = VGroup(*[Dot(point = axes.c2p(point[0],point[1]), color=myBlue, radius=0.01) for point in points])

        # POINT COUNTER 
        n = ValueTracker(0)     # initialize value tracker

        # label and integer value
        label = Text(
            "points:",
            font_size = 20,
            color = myBlue, 
            font = "BITSTREAM VERA SERIF",
            ).to_corner(corner=UP + LEFT, buff=0.5)
        number = always_redraw( lambda : Integer(
            color = myBlue, font_size = 30
            ).set_value(n.get_value()).next_to(label, RIGHT, buff=0.1).shift(UP * 0.02))


        ## ANIMATIONS

        # create title card 
        self.play(Write(title_card), run_time=3)
        self.wait()
        self.play(FadeOut(title_card))

        # create point counter label/text
        self.play(Write(label), run_time=0.5)
        self.play(Write(number), run_time=0.5)

        # create axes
        self.add(axes)

        # sequentially create each dot (smooth rate function)
        numb = 100
        self.play(
            ShowIncreasingSubsets(dots[:numb]), 
            n.animate.set_value(numb), 
            run_time = 39, 
            rate_func = rate_functions.smooth)

        ## Dumb solution left for posterity + for my future-self to laugh at haha
        # sequentially create each dot (perhaps add a smoothing curve)
        # for i in range(500):
        #     if i < 100:
        #         self.play(Create(dots[i]), run_time = 0.001)
        #         n.set_value(i)   # update the value tracker
        #     else:
        #         self.play(Create(dots[i:i+10]), run_time=1e-6)
        #         n.set_value(i+10)   # update the value tracker




# reference code from: https://www.reddit.com/r/manim/comments/pfbb36/how_to_animate_scatter_plot_by_plotting_one_point/
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