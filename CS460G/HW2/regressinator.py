"""
    Regressinator
    by Ben Richey

    This script contains implementations of gradient descent to perform
    linear regression to classify wine data and synthetic data. Both data
    sets have been provided by Dr. Brent Harrison at the University of
    Kentucky.

    This is intended to meet the requirements for homework 2 of machine
    learning (CS460G) at UK.

    Copyright © 2022 Ben Richey

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the “Software”), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is furnished
    to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies
    or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
    PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
    FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE
"""
import sys
import os
import csv
import ast
import math

# Debugging
import ipdb

WINE_FILE = "winequality-red.csv"
SYNTHETIC_FILES = ["synthetic-1.csv", "synthetic-2.csv"]

def load_file_data(data_dir, synthetic, filename):
    data = {}
    for root, dirs, files in os.walk(data_dir):
        for f in files: # Iterate through files in data_dir
            if f != filename:
                continue
            try:
                with open(os.path.join(root, f)) as csvfile:
                    reader = csv.reader(csvfile)
                    if not synthetic:
                        for row in reader:
                            for i in range(len(row)):
                                data[row[i]] = []
                            break
                        keys = [key for key in data.keys()]
                        for row in reader:
                            for i in range(len(row)):
                                data[keys[i]].append(ast.literal_eval(row[i]))
                    else:
                        keys_established = False
                        for row in reader:
                            if not keys_established:
                                for i in range(len(row)):
                                    data["f{}".format(i)] = []
                                keys = [k for k in data.keys()]
                                keys_established = True
                            else:
                                for i in range(len(row)):
                                    data[keys[i]].append(ast.literal_eval(row[i]))
            except IOError:
                print("Error: Unable to open file '{}'".format(f))
                sys.exit()
    return data

if __name__ == "__main__":

    try:
        data_dir = sys.argv[1]
    except IndexError as err:
        print("Usage: python3 regressinator.py <path to data directory>")
        sys.exit()
    
    wine_data = load_file_data(data_dir, False, WINE_FILE)
    synthetic_data = {}
    for i in range(len(SYNTHETIC_FILES)):
        synthetic_data[SYNTHETIC_FILES[i]] = load_file_data(data_dir, True, SYNTHETIC_FILES[i])