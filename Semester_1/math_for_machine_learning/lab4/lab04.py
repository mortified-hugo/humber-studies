# 1 Find the derivative of the functions
import sympy as sp


# w, y, z = sp.symbols('w y z')
#
# S = ((w ** 2) * (2-w) + w**5) / 3*w
# h = (3*(y**-6)) - (8*(y**-3)) + (9*(y**-1))
# G = (z**2) * ((z-1)**2)
#
# derivative_S = sp.diff(S, w)
# derivative_h = sp.diff(h, y)
# derivative_G = sp.diff(G, z)
#
# print("Deriviative of S with respect to w:")
# sp.pprint(derivative_S)
#
# print("\nDeriviative of h with respect to y:")
# sp.pprint(derivative_h)
#
# print("\nDeriviative of G with respect to z:")
# sp.pprint(derivative_G)


# 2 From first principles find the slope of the tangent to the curve x = 1

# def power_rule(symbol, exponent):
#     return exponent * symbol**(exponent - 1)
#
#
# def chain_rule(outer_func, inner_func, symbol):
#     outer_derivative = sp.diff(outer_func, inner_func)
#     inner_derivative = sp.diff(inner_func, symbol)
#     return outer_derivative * inner_derivative
#
#
# x = sp.symbols('x')
# f = (3-(2*(x**3)))**2
#
# slope_at_x1 = sp.diff(f).subs(x, 1)
# print("\nSlope of the tangent to the curve at x = 1:")
# sp.pprint(slope_at_x1)

# 3 Determine where the function is increasing and decreasing

t = sp.symbols('t')
V = t**3 - 24*t**2 + 192*t - 50

V_derivative = sp.diff(V, t)
critical_points = sp.solve(V_derivative, t)


print(f"With only one critical point at t = {critical_points[0]}, we can determine the intervals "
      f"of increase and decrease by testing values around this point.")
print("The function is increasing on the interval (-∞, 8) stops increasing at 8 "
      "and then goes back to increasing on the interval (8, ∞).")

