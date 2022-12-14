from typing import List, TypeVar, Iterable
from cmath import phase
from math import sin, factorial
from sympy import Point as spPoint, Triangle
import numpy as np


int_float = TypeVar('int_float', int, float)


class Point:

    __precision = 10 ** (-9)

    def __check_equals(val1 : int_float, val2 : int_float) -> bool:
        return abs(val1 - val2) <= Point.__precision

    def __init__(self, x : int_float, y : int_float) -> None:
        self.x = x
        self.y = y
    
    def mag(self) -> int_float: # magnetude
        return (self.x ** 2 + self.y ** 2) ** (0.5)

    def normalized(self):
        return self / self.mag()
    
    def rotated90anti(self):
        return Point(-self.y, self.x)
    
    def dist(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** (1/2) 

    @staticmethod
    def from_complex(z : complex):
        return Point(z.real, z.imag)

    def complex_phase(self):
        return phase(complex(self))

    def __abs__(self):
        return (self.x**2+self.y**2)**.5

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if type(other) == int or type(other) == float or type(other) == np.float64:
            return Point(self.x * other, self.y * other)
        else:
            return self.x * other.x + self.y * other.y
    
    def __rmul__(self, other):
        R = self * other
        # print(R, self, other)
        return R

    def __truediv__(self, other):
        return self * (1/other)
    
    def __eq__(self, other):
        return Point.__check_equals(self.x, other.x) and Point.__check_equals(self.y, other.y)

    def __neq__(self, other):
        return not (self == other)

    def eq_zero(self):
        return Point.__check_equals(self.x, 0) and Point.__check_equals(self.y, 0)

    def __neg__(self):
        return Point(-self.x, -self.y)
    
    def __complex__(self):
        return complex(self.x, self.y)

    def complex_division(self, other):
        return Point.from_complex(complex(self)/complex(other))
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'
    
    def __iter__(self):
        yield self.x
        yield self.y
    
    def __copy__(self):
        return Point(self.x, self.y)
    
    

class DiscretePlaneCurve:
    """
    A discrete plane curve is a map \gamma : I \to \mathbbR^2 where I is the index
    set (0, 1, 2, ..., n-1) where n is a positive integer.

    Here, self._points[i] (or more adequately, self.ithpoint(i) ) represents \gamma(i).
    """

    def __init__(self, points : Iterable[Point], is_closed : bool=True, compression:int_float = 1) -> None:
        self.points = [pt/compression for pt in points]
        self.point_number = len(self.points)
        self.is_closed = is_closed

    def nth_point(self, ind : int) -> Point:
        return self.points[ind % self.point_number]            

    def nth_edge_vector(self, ind : int) -> Point:
        """
        Returns the edge vector v_(i, i+1), definedby gamma(i+1) - gamma(i) 
        """
        return self.nth_point(ind+1) - self.nth_point(ind)
    
    def get_edge_vectors(self) -> List[Point]:
        return [self.nth_edge_vector(i) for i in range(len(self))]
    
    def get_edge_endpoints(self) -> List[List[Point]]:
        return [[self.nth_point(i), self.nth_point(i+1)] for i in range(len(self))]

    def nth_tangent_vector(self, ind : int) -> Point:
        """
        Returns the tangent vector T_(i, i+1), defined by the normalization of the
        edge vector v_(i, i+1) (when it is nonzero)
        """
        return self.nth_edge_vector(ind).normalized()
    
    def get_tangent_vectors(self) -> List[Point]:
        return [self.nth_tangent_vector(i) for i in range(len(self))]
    
    def nth_normal_vector(self, ind : int) -> Point:
        return self.nth_tangent_vector(ind).rotated90anti()
    
    def total_length(self) -> int_float:
        return sum(self.nth_edge_vector(i).mag() for i in range(len(self)))
    
    def is_regular(self) -> bool:
        tangent_vectors = self.get_tangent_vectors()
        return all(tangent_vectors[i] != -tangent_vectors[i+1] for i in range(len(tangent_vectors) - 1))
    
    def arclength_parametrized(self) -> bool:
        edge_vectors = self.get_edge_vectors()
        return all(edge_vectors[i] == edge_vectors[i+1] for i in range(len(edge_vectors)-1))

    def nth_turning_angle(self, ind : int) -> int_float:
        return self.nth_edge_vector(ind).complex_division(self.nth_edge_vector(ind-1)).complex_phase()
    
    def get_turning_angles(self) -> List[int_float]:
        relevant_length = len(self)
        if not self.is_closed:
            relevant_length -= 2
        return [self.nth_turning_angle(i) for i in range(relevant_length)]

    def total_curvature_turning_angle(self):
        return sum(self.get_turning_angles())
    
    def nth_half_sin_curvature(self, ind : int) -> int_float:
        return 2 * sin(self.nth_turning_angle(ind)/2)
    
    def get_half_sin_curvatures(self) -> List[int_float]:
        relevant_length = len(self)
        if not self.is_closed:
            relevant_length -= 2
        return [self.nth_half_sin_curvature(i) for i in range(relevant_length)] 

    def total_curvature_half_sin(self):
        return sum(self.get_half_sin_curvatures())

    def nth_circumradius_curvature(self, ind : int) -> int_float:
        return 2 * sin(self.nth_turning_angle(ind)) / self.nth_point(ind-1).dist(self.nth_point(ind+1))
    
    def get_circumradius_curvatures(self) -> List[int_float]:
        relevant_length = len(self)
        if not self.is_closed:
            relevant_length -= 2
        return [self.nth_circumradius_curvature(i) for i in range(relevant_length)] 

    def total_curvature_circumradius(self):
        return sum(self.get_circumradius_curvatures())
    
    def nth_unit_vector_along_circumcenter(self, ind : int) -> Point:
        p1, p2, p3 = spPoint(*self.nth_point(ind)), spPoint(*self.nth_point(ind+1)), spPoint(*self.nth_point(ind-1))
        cc = Triangle(p1, p2, p3).circumcenter

        return (Point(float(cc.x), float(cc.y)) - self.nth_point(ind)).normalized()

    def nth_angle_bisector(self, ind : int) -> Point:
        diff = self.nth_normal_vector(ind) + self.nth_normal_vector(ind-1)
        
        if diff.eq_zero():
            return self.nth_normal_vector(ind)
        else:
            return diff.normalized()
    
    def get_angle_bisectors(self) -> List[Point]:
        return [self.nth_angle_bisector(i) for i in range(len(self))]

    def timestep_from_angle_curvature(self, time_step=0.01):
        relevant_length = len(self)
        if not self.is_closed:
            relevant_length -= 2
        
        return DiscretePlaneCurve([self.points[i] + ((time_step * self.nth_turning_angle(i)) * self.nth_angle_bisector(i)) for i in range(relevant_length)], 
                                   is_closed=self.is_closed)

    def timestep_from_half_sin_curvature(self, time_step=0.01):
        relevant_length = len(self)
        if not self.is_closed:
            relevant_length -= 2
        
        fixed_half_sin = DiscretePlaneCurve.fixed_curvature(DiscretePlaneCurve.nth_half_sin_curvature, 1/2, 1/2)

        return DiscretePlaneCurve([self.points[i] + ((time_step * fixed_half_sin(self, i)) * self.nth_angle_bisector(i)) for i in range(relevant_length)], 
                                   is_closed=self.is_closed)

    def timestep_from_circumradius_curvature(self, time_step=0.01):
        relevant_length = len(self)
        if not self.is_closed:
            relevant_length -= 2
        
        return DiscretePlaneCurve([self.points[i] + ((time_step * self.nth_circumradius_curvature(i)) * self.nth_unit_vector_along_circumcenter(i)) for i in range(relevant_length)], 
                                   is_closed=self.is_closed)        

    def center_of_mass(self):
        return sum(self.points, start=Point(0, 0)) / len(self.points)

    def get_evolute(self, curvature_function, normal_vector_function):
        return DiscretePlaneCurve([self.points[i] + (1/curvature_function(self, i)) * normal_vector_function(self, i) for i in range(len(self))], is_closed=self.is_closed)

    @staticmethod
    def fixed_curvature(curvature_function, frac1, frac2):
        if frac1 is None or frac2 is None:
            return lambda self, i: curvature_function(self, i)
        return lambda self, i : curvature_function(self, i) / (abs(self.nth_edge_vector(i-1)) * frac1 + abs(self.nth_edge_vector(i)) * frac2)

    def get_curvatures_from_function(self, curvature_function):
        relevant_length = len(self)
        if not self.is_closed:
            relevant_length -= 2
        return [curvature_function(self, i) for i in range(relevant_length)]
        

    def __len__(self):
        return self.point_number if self.is_closed else self.point_number - 1

    def discrete_derivative(self, function, order=0):
        if order == 0:
            return function
        else:
            function_prime = lambda i: ((function(i+1)-function(i))/(self.nth_point(i).dist(self.nth_point(i+1)))
                            + (function(i)-function(i-1))/self.nth_point(i-1).dist(self.nth_point(i))
            )/2
            return self.discrete_derivative(function_prime, order=order-1) 

    def length_sum_function(self):
        L = [0]
        for i in range(len(self)-1):
            L.append(self.nth_point(i).dist(self.nth_point(i+1))+L[-1])
        return L

def get_vec_at_ind(vec, ind):
    return vec[ind % len(vec)]

def get_param_set(start, end, num_points):
    return np.linspace(start, end, num=num_points+1)[:-1]

def discretize(lambdax, lambday, start, end, num_points):
    params = get_param_set(start, end, num_points)
    return DiscretePlaneCurve([Point(lambdax(t), lambday(t)) for t in params], is_closed=True)

# Assumes circular data
def discrete_derivative(info_xs, info_ys, order, position):
    info_xs = list(info_xs)
    info_ys = list(info_ys)
    rate = info_xs[1] - info_xs[0]
    #print(info_xs)
    #print(info_ys)

    if order % 2 == 0:
        n = order // 2
        hs = [#-get_vec_at_ind(info_xs, position) + get_vec_at_ind(info_xs, position + i)
                rate*i
                        for i in range(-n, n+1)]
        matrix = []

        for i in range(order+1):
            if i == 0:
                matrix.append([1 for _ in range(order+1)])
            else:
                matrix.append([hs[j]**i for j in range(order+1)])
        
        matrix = np.array(matrix)
        vec = np.reshape(np.array([0 for _ in range(order)] + [factorial(order)]), (order+1, 1))

        coeffs = np.matmul(np.linalg.inv(matrix), vec)

        return sum(coeffs[i][0] * get_vec_at_ind(info_ys, position+i-n) for i in range(order+1))
    else:
        n = order // 2 + 1
        hs = [#-get_vec_at_ind(info_xs, position) + get_vec_at_ind(info_xs, position + i)
              rate * i
                     for i in range(-n, n+1) if i != 0]
        matrix = []

        for i in range(order+1):
            if i == 0:
                matrix.append([1 for _ in range(order+1)])
            else:
                matrix.append([hs[j]**i for j in range(order+1)])
        
        matrix = np.array(matrix)
        vec = np.reshape(np.array([0 for _ in range(order)] + [factorial(order)]), (order+1, 1))

        coeffs = np.matmul(np.linalg.inv(matrix), vec)
        #print(coeffs)

        return sum(coeffs[i][0] * get_vec_at_ind(info_ys, position-n+(i+1 if i >= n else i)) for i in range(order+1))
