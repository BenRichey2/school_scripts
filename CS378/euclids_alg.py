#!/usr/bin/python3
import sys
import ast

def ea(n, d):
    print("{} = {} * {} + {}".format(n, d, n // d, n % d))
    q = n // d
    r = n % d
    while r != 0:
        n = d
        d = r
        q = n // d
        r = n % d
        print("{} = {} * {} + {}".format(n, d, q, r))

if __name__ == "__main__":
    ea(ast.literal_eval(sys.argv[1]), ast.literal_eval(sys.argv[2]))
