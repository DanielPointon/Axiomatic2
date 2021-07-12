from manimlib.imports import *
from .manimVid import getMovieConfig
from deps.algebra.base_classes.base import *
import math



class GraphAreaPlot(Scene):
    def __init__(self, function, variable, start, stop, numberOfTrapeziums,  **kwargs):
        super().__init__(**kwargs)
        self.function = function
        self.variable = variable
        self.numberOfTrapeziums = numberOfTrapeziums.evaluate()
        self.start = start.evaluate()
        self.stop = stop.evaluate()
        self.height = (self.stop-self.start)/self.numberOfTrapeziums
        self.graphStep=(self.stop-self.start)/4

    def construct(self):
        print(self.start, self.stop, self.graphStep)
        # axes = Axes(x_range=(self.start, self.stop, self.graphStep), y_range=(0, 8, 1))
        axes=Axes()
        axes.add_coordinate_labels()

        curveOne = axes.get_graph(lambda x: self.function.substitute(
            self.variable, Num(x)).evaluate(), color=BLUE)
        self.play(Write(axes))
        self.play(Write(curveOne))

        for i in range(int(self.numberOfTrapeziums)):
            curvePoint1 = axes.input_to_graph_point(self.start+self.height*i, curveOne)
            curvePoint2 = axes.input_to_graph_point(self.start+self.height*(i+1), curveOne)
            xIntercept1 = axes.c2p(self.start+self.height*i, 0)
            xIntercept2 = axes.c2p(self.start+self.height*(i+1), 0)
            polygon = Polygon(xIntercept1, curvePoint1, curvePoint2,
                              xIntercept2, color=YELLOW, fill_opacity=0.4)
            self.play(ShowCreation(polygon).set_run_time(0.4))
