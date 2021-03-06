"""
    Subsequencinator
    by Ben Richey

    This script implements two functions that ultimately find and
    print the longest common subsequence between two strings. The
    two functions that do this are LCS_length and printLCS. LCS_length
    will construct an LCS matrix between the two strings that contains
    information that reveals the LCS between the two strings. The
    printLCS function returns the string containing the LCS between
    these two strings using the matrix generated by LCS_length.
"""

import argparse
import os
import sys
import ipdb

def LCS_length(x, y):
    b = [None] * len(x)
    for i in range(len(x)):
        b[i] = [None] * len(y) 
    c = [None] * (len(x) + 1)
    for i in range(len(x) + 1):
        c[i] = [None] * (len(y) + 1)
    for i in range(len(x) + 1):
        c[i][0] = 0
    for j in range(len(y) + 1):
        c[0][j] = 0
    for i in range(len(x)):
        for j in range(len(y)):
            if x[i] == y[j]:
                c[i+1][j+1] = c[i][j] + 1
                b[i][j] = "UL" # UL = upper left
            elif c[i][j+1] >= c[i+1][j]:
                c[i+1][j+1] = c[i][j+1]
                b[i][j] = "UP"
            else:
                c[i+1][j+1] = c[i+1][j]
                b[i][j] = "L" # L = left
    return (c[len(x)][len(y)], b)

def printLCS(b, x, i, j, lcs):
    if i < 0 or j < 0:
        return
    if b[i][j] == "UL":
        printLCS(b, x, i-1, j-1, lcs)
        lcs.append(x[i])
    elif b[i][j] == "UP":
        printLCS(b, x, i-1, j, lcs)
    else:
        printLCS(b, x, i, j-1, lcs)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Find the LCS of two DNA sequences")
    parser.add_argument("--data_path",
                        help="Full path to directory containing txt file w/ strings.",
                        required=True)
    args = parser.parse_args()
    x = str()
    y = str()
    try:
        for (root, dirs, files) in os.walk(args.data_path, topdown=True):
            if "dna.txt" in files:
                with open(os.path.join(root, "dna.txt")) as dna:
                    strings = dna.readlines()
                    x = strings[0]
                    x = x[:-1] # remove trailing \n
                    y = strings[1]
                    y = y[:-1] # remove trailing \n
    except (IOError) as err:
        print("Error: " + err)
        sys.exit()
    LCS_len, LCS_matrix = LCS_length(x, y)
    LCS = []
    printLCS(LCS_matrix, x, len(x) - 1, len(y) - 1, LCS)
    lcs = ""
    for char in LCS:
        lcs += char
    print("x = {}".format(x))
    print("y = {}".format(y))
    print("LCS Length = {}".format(LCS_len))
    print("LCS = {}".format(lcs))
    with open(os.path.join(os.getcwd(), "results.txt"), "w") as output:
        output.write("{}\n".format(LCS_len))
        output.write("{}\n".format(lcs))
    print("Wrote results to file: ./results.txt")
