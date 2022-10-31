"""

Create animation video file from this python file by running

manim -pql half_sin_curvature.py HalfSinCollapsingDiscreteCurve

"""


from manim import *
from copy import copy, deepcopy

# ddg module python file is one directory above
import ddg




class HalfSinCollapsingDiscreteCurve(Scene):
    def construct(self):

        points = [ddg.Point(-0.46, 5.8), ddg.Point(-3.86, 3.94), ddg.Point(-5.49, 0.08), ddg.Point(-4.82, -4.22),
                  ddg.Point(-2.8, -5.97), ddg.Point(-0.99, -5.18), ddg.Point(4.07, -5.85), ddg.Point(1.9, -0.62), 
                  ddg.Point(3.07, 3.82)]
        curve = ddg.DiscretePlaneCurve(points, is_closed=True, compression=2)

        axes_drift = Axes(x_range=[-1, 1, 1], y_range=[-1, 1, 1], x_length=3, y_length=3, axis_config={'include_tip' : False, 'numbers_to_exclude' : [-1, 0, 1]}).add_coordinates()
        axes_drift.to_edge(UR)
        axes_drift_labels = axes_drift.get_axis_labels(x_label='x', y_label='y')

        axes_curvature = Axes(x_range=[-1, 1, 1], y_range=[-1, 1, 1], x_length=3, y_length=3, axis_config={'include_tip' : False, 'numbers_to_exclude' : [-1, 0, 1]}).add_coordinates()
        axes_curvature.to_edge(DR)
        axes_curvature_labels = axes_curvature.get_axis_labels(x_label='t', y_label='\kappa')


        # graph = axes.plot(lambda x: x ** 0.5, x_range=[0, 4], color=YELLOW)
        # graphing_stuff = VGroup(axes, graph, axis_labels)

        self.play(DrawBorderThenFill(axes_drift), Write(axes_drift_labels),
                  DrawBorderThenFill(axes_curvature), Write(axes_curvature_labels))
        # self.play(Create(graph))
        #self.play(graphing_stuff.animate.shift(DOWN*4))
        #self.play(axes.animate.shift(LEFT*3), run_time=3)
        # print(list(axes.get_center_of_mass())[:-1])
        # print(Point(*list(axes.get_center_of_mass())[:-1]))
        initial_cm = curve.center_of_mass()
        cm = Dot(radius=0.01, color=YELLOW).move_to(list(curve.center_of_mass()-initial_cm+ddg.Point(*list(axes_drift.get_origin())[:-1])) + [0])
        tp_cm = TracedPath(cm.get_center, stroke_color=YELLOW, stroke_width=5)
        self.add(cm, tp_cm)

        t = 0
        curr_curvature = Dot(radius=0.01, color=GREEN).move_to(list(ddg.Point(t, curve.total_curvature_half_sin()/5)+ddg.Point(*list(axes_curvature.get_origin())[:-1])) + [0])
        tp_curr_curvature = TracedPath(curr_curvature.get_center, stroke_color=GREEN_C, stroke_width=5)
        self.add(curr_curvature, tp_curr_curvature)

        for _ in range(330):
            dots = [Dot(radius=0.03, color=BLUE).move_to([p.x, p.y, 0]) for p in curve.points]
            edges = [Line([*e1, 0], [*e2, 0]) for e1, e2 in curve.get_edge_endpoints()]
            vectors = [Vector(list(curve.nth_angle_bisector(i) * curve.nth_half_sin_curvature(i)), color=DARK_BLUE) for i in range(len(curve))]

            for i in range(len(curve)):
                vi = vectors[i]
                vi.shift(list(curve.points[i]) + [0])

            curve = curve.timestep_from_half_sin_curvature(time_step=0.008)
            t += 0.008
            
            new_dots = [Dot(radius=0.03, color=BLUE).move_to([p.x, p.y, 0]) for p in curve.points]
            points = deepcopy(curve.points)
            new_edges = [Line([*e1, 0], [*e2, 0]) for e1, e2 in curve.get_edge_endpoints()]
            new_vectors = [Vector(list(curve.nth_angle_bisector(i) * curve.nth_half_sin_curvature(i)), color=DARK_BLUE) for i in range(len(curve))]

            for i in range(len(curve)):
                vi = new_vectors[i]
                vi.shift(list(curve.points[i]) + [0])

            self.add(*dots)
            self.add(*edges)
            self.add(*vectors)

            self.play(*[Transform(dots[i], new_dots[i]) for i in range(len(points))],
                      *[Transform(edges[i], new_edges[i]) for i in range(len(edges))], 
                      *[Transform(vectors[i], new_vectors[i]) for i in range(len(vectors))],
                      ApplyMethod(cm.move_to, list(50*(curve.center_of_mass()-initial_cm)+ddg.Point(*list(axes_drift.get_origin())[:-1])) + [0]), 
                      ApplyMethod(curr_curvature.move_to, list(ddg.Point(t/2, curve.total_curvature_half_sin()/5)+ddg.Point(*list(axes_curvature.get_origin())[:-1])) + [0]), run_time=0.1)
            
            #print(list(ddg.Point(t, curve.total_curvature_turning_angle())+ddg.Point(*list(axes_curvature.get_origin())[:-1])))
            #print(list(50*(curve.center_of_mass()-initial_cm)+ddg.Point(*list(axes_drift.get_origin())[:-1])))
            # print(list(curve.center_of_mass()))

            self.remove(*dots)
            self.remove(*edges)
            self.remove(*vectors)

