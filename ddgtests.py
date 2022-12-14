import ddg
from math import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt

n_points = 10
start = 0
end = 2 * pi

curve = ddg.discretize(lambda t: 2 * cos(t), lambda t: 1 * sin(t), start, end, n_points)
fixed_curvature = ddg.DiscretePlaneCurve.fixed_curvature(ddg.DiscretePlaneCurve.nth_half_sin_curvature, .5, .5)
discrete_curvatures = curve.get_curvatures_from_function(fixed_curvature)
params = ddg.get_param_set(start, end, n_points)
actual_curvatures = [(2/(4 * sin(t)**2 + cos(t)**2)**(3/2)) for t in params]
actual_curvature_derivatives = [-9*sin(2*t)/(4 * sin(t)**2 + cos(t)**2)**(5/2) for t in params]
discrete_derivatives = [ddg.discrete_derivative(params, discrete_curvatures, 1, pos) for pos in range(n_points)]

fig = plt.figure()

plot_derivative = True

if not plot_derivative:
    plt.plot(params, actual_curvatures)
    plt.plot(params, discrete_curvatures)
else:
    plt.plot(params, actual_curvature_derivatives)
    plt.plot(params, discrete_derivatives)

plt.show()

