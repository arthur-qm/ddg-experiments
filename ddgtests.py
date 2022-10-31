import ddg
from math import degrees

points = [ddg.Point(-0.46, 5.8), ddg.Point(-3.86, 3.94), ddg.Point(-5.49, 0.08), ddg.Point(-4.82, -4.22),
                  ddg.Point(-2.8, -5.97), ddg.Point(-0.99, -5.18), ddg.Point(4.07, -5.85), ddg.Point(1.9, -0.62), 
                  ddg.Point(3.07, 3.82)]
curve = ddg.DiscretePlaneCurve(points, is_closed=True, compression=2)

print(*map(degrees, curve.get_turning_angles()))

