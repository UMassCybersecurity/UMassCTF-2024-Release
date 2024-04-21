from sol.modpoly import lagrange_interpolation
import numpy as np
from sys import argv

p = int(argv[1])
degree = int(argv[2])

flag = 'UMASS{1nt3rpr3t_n0r_1nt3rp0l@t3}'

flag_y = [ord(char) for char in flag]
# print(flag_y)

original_points = [(i, np.random.randint(45, 127)) for i in range(degree + 1 - len(flag))]
flag_points = [(degree + i + 1, flag_y[i]) for i in range(len(flag))]

P = lagrange_interpolation(original_points + flag_points, p)

remaining_points = [(i, P(i)) for i in range(degree + 1 - len(flag), degree + 1)]

Q = lagrange_interpolation(original_points + remaining_points, p)

with open('static/journal.txt', 'w') as f:
    f.write(f'p = {p}\n\n')
    for x, y in original_points + remaining_points:
        f.write(f'DAY({x}) = {y}\n')
    f.write(f"\n{'-' * 40}\n\n")
    for x, _ in flag_points:
        f.write(f'DAY({x}) = ???\n')
