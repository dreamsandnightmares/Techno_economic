from sympy import *

i = 0.1
A_o2 = 2.8
P_o2_an = 1.2 + A_o2 * 0.5
print(P_o2_an)

b = -(1.2 + 3.4 * 0.5)

c = 1.03 * 0.5 * P_o2_an
x = Symbol('x')


a = solve([x ** 2 + b * x + c], [x])
d,e =a
print(e[0])




