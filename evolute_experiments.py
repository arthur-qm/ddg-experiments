"""

manim -pql evolute_experiments.py EvoluteFigure

"""


import ddg
from manim import *
from math import sin, cos, pi

class EvoluteFigure(Scene):
    def construct(self):

        for n_points in range(4, 33):

            curve = ddg.discretize(lambda t: 2 * cos(t), lambda t: 1 * sin(t), 0, 2*pi, n_points)
            evolute = curve.get_evolute(ddg.DiscretePlaneCurve.fixed_curvature(ddg.DiscretePlaneCurve.nth_half_sin_curvature, .5, .5), ddg.DiscretePlaneCurve.nth_angle_bisector)

            curve_dots = [Dot(radius=0.05, color=BLUE).move_to([p.x, p.y, 0]) for p in curve.points]
            evolute_dots = [Dot(radius=0.03, color=RED).move_to([p.x, p.y, 0]) for p in evolute.points]
            
            curve_edges = [Line([*e1, 0], [*e2, 0]) for e1, e2 in curve.get_edge_endpoints()]
            evolute_edges = [Line([*e1, 0], [*e2, 0], color=GREEN) for e1, e2 in evolute.get_edge_endpoints()]
            
            self.add(*curve_dots)
            self.add(*curve_edges)

            self.add(*evolute_dots)
            self.add(*evolute_edges)

            self.wait()

            self.remove(*curve_dots, *curve_edges, *evolute_dots, *evolute_edges)