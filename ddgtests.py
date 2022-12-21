import ddg
from math import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt

n_points = 200
start = 0
end = 2 * pi

curve = ddg.discretize(lambda t: 2 * cos(t), lambda t: 1 * sin(t), start, end, n_points)
fixed_curvature = ddg.DiscretePlaneCurve.fixed_curvature(ddg.DiscretePlaneCurve.nth_half_sin_curvature, .5, .5)
discrete_curvatures = curve.get_curvatures_from_function(fixed_curvature)
params_s = curve.length_sum_function()
params = ddg.get_param_set(start, end, n_points)
actual_curvatures = [(2/(4 * sin(t)**2 + cos(t)**2)**(3/2)) for t in params]
actual_curvature_derivatives = [-9*sin(2*t)/(4 * sin(t)**2 + cos(t)**2)**(6/2) for t in params]
actual_curvature_2nd_der = [18 * (9 * sin(t) * sin(2*t)*cos(t)-cos(2*t)*(4*sin(t)**2+cos(t)**2)) / (4*sin(t)**2+cos(t)**2)**(9/2) for t in params]
discrete_derivative_funtion = curve.discrete_derivative(lambda i: fixed_curvature(curve, i), 1)
discrete_2nd_derivative_function = curve.discrete_derivative(lambda i: fixed_curvature(curve, i), 2)
discrete_derivatives = [discrete_derivative_funtion(i) for i in range(n_points)]
discrete_2nd_derivatives = [discrete_2nd_derivative_function(i) for i in range(n_points)]

fig = plt.figure()

plot_derivative = True

#plt.get_

option = 0

if option == 0:
    plt.plot(params_s, actual_curvatures)
    plt.plot(params_s, discrete_curvatures)
elif option == 1:
    plt.plot(params_s, actual_curvature_derivatives)
    plt.plot(params_s, discrete_derivatives)
else:
    plt.plot(params_s, actual_curvature_2nd_der)
    plt.plot(params_s, discrete_2nd_derivatives)

plt.show()

