"""

manim -pql evolute_experiments.py EvoluteFigure

"""


import ddg
from manim import *
from math import sin, cos, pi

class EvoluteFigure(Scene):
    def construct(self):

        for n_points in range(5, 17):

            # curve = ddg.discretize(lambda t: t if t <= 1 else 2-t, lambda t: (t - t**3)**.5 if t <= 1 else -((2-t) - ((2-t)**3))**.5, 0, 2, n_points)
            curve = ddg.discretize(lambda t: t, lambda t: t**3, -1, 0.99, n_points)
            evolute = curve.get_evolute(ddg.DiscretePlaneCurve.nth_circumradius_curvature, ddg.DiscretePlaneCurve.nth_unit_vector_along_circumcenter)

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