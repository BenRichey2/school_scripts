#!/usr/bin/python3
import sys
import ast

def modInverse(a, m):
        for x in range(1, m):
            if (((a % m) * (x % m)) % m == 1):
                return x
        return "Not found"

if __name__ == "__main__":

    a = ast.literal_eval(sys.argv[1])
    m = ast.literal_eval(sys.argv[2])
    print(modInverse(a, m))
