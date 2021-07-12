import os
import sys
from manimlib.imports import *
import random

# As we are using a beta version of the manim library
# Fixed config settings are used to avoid errors with the library


def getMovieConfig(renderVideo, renderMovieSettings):
    if renderVideo:
        return {'window_config': {'size': (960, 540)},
                'camera_config': {'pixel_width': 3840, 'pixel_height': 2160, 'frame_rate': 60, 'background_color': rgb_to_color(hex_to_rgb("#4A1A37"))},
                'file_writer_config': {'write_to_movie': True, 'break_into_partial_movies': False, 'save_last_frame': False, 'save_pngs': False, 'png_mode': 'RGB', 'movie_file_extension': '.mp4', 'mirror_module_path': False,
                                       'output_directory': '', 'file_name': renderMovieSettings['filename'], 'input_file_path': 'manimVid.py', 'open_file_upon_completion': True, 'show_file_location_upon_completion': False, 'quiet': False},
                'skip_animations': False,
                'leave_progress_bars': False,
                'preview': False}
    else:
        return {
            'camera_config': {'pixel_width': 3840, 'pixel_height': 2160, 'frame_rate': 60, 'background_color': rgb_to_color(hex_to_rgb("#4A1A37"))}
        }


class Video(Scene):
    def __init__(self, simplification, **kwargs):
        # Load the configuration into the Scene class
        super().__init__(**kwargs)
        self.output_file = "myscene"
        self.simplification = simplification
        self.function = self.simplification.getProblem()

    def addTex(self, newTex):
        newTexes = newTex.split("\\newline")
        # Lines of workings need to be shifted more if previous lines are multiline
        if len(newTexes) == 1:
            shiftIndex = 3
        else:
            shiftIndex = len(newTexes)+3
        # Move everything up by the required number of lines
        self.play(*[Transform(mobject, mobject.copy().shift(shiftIndex*UP))
                    for mobject in self.get_mobjects()])

        def getTexMobject(tex, shiftFactor):
            texMobject = Tex(tex, color=WHITE)
            texMobject.shift(DOWN*shiftFactor)
            return texMobject
        for i in range(len(newTexes)):
            self.play(Write(getTexMobject(newTexes[i], (i+1)-len(newTexes))))

    def construct(self):
        latestTex = ""
        # Display initial problem
        self.addTex(self.function.toTex())
        for step in self.simplification.getSteps():
            if(not step.isTrivial()):
                latestTex = step.toTex()
                self.addTex(latestTex)
        if not self.simplification.getResultTex() == latestTex:
            self.addTex(self.simplification.getResultTex())
