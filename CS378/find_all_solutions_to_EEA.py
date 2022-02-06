#!/usr/bin/python3
import sys
import ast
from math import gcd

def extended_euclidean_algorithm(a, b):
    if b > a:
        tmp = a
        a = b
        b = tmp
    if a == 0:
        return b, 0, 1
    GCD, x1, y1 = extended_euclidean_algorithm(b % a, a)
    x = y1 - (b//a) * x1
    y = x1
    return GCD, x, y

def get_all_solutions_to_EEA(a, b):
    if b > a:
        tmp = a
        a = b
        b = tmp
    GCD, smallest_x, smallest_y = extended_euclidean_algorithm(a, b)
    max_x = abs(b / GCD)
    max_y = abs(a / GCD)
    solutions = []
    for i in range(smallest_x, max_x):
        for j in range(smallest_y, max_y):
            if (GCD == a * i + b * j):
                solutions.append((i, j))
            if (GCD == a * -i + b * -j):
                solutions.append((-i, -j))
    return GCD, solutions

def print_solutions_to_EEA(solutions, GCD, a, b):
    solution_string = "All solutions to EEA for {} and {}\n".format(a, b)
    for solution in solutions:
        solution_string += "{} = {} * {} + {} * {}\n".format(GCD, a, solution[0], b, solution[1])
    print(solution_string)

if __name__ == "__main__":
    try:
        a = ast.literal_eval(sys.argv[1])
        b = ast.literal_eval(sys.argv[2])
        GCD, solutions = get_all_solutions_to_EEA(a,b)
        print_solutions_to_EEA(solutions, GCD, a, b)
    except IndexError:
        print("Usage: ./find_all_solutions_to_EEA.py <a> <b>")
        sys.exit()
