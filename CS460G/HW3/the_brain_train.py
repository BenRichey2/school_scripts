"""
    The Brain Train
    by Ben Richey

    This script implements a multilayer perceptron feed forward neural
    network to predict the MNIST data set. This is implemented for the
    CS460G assignment 3 at the University of Kentucky. The data was
    provided by Dr. Brent Harrison at UK.

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
import os
import sys
import csv
import ast
import math
import time
from progress.spinner import Spinner

import ipdb

DATA_FILES = ["mnist_test_0_1.csv", "mnist_train_0_1.csv"]

def load_data(data_dir):
    """
        Load in training and test data for all models
        @param data_dir: directory containing training and test data
        @return: a dictionary where the keys are the file names and the
                 values are another dictionary. This inner dictionary's
                 keys are 'examples' and 'class' and the values
                 are either a nested list of the feature data for each example
                 or the classification for each example.
    """
    data = {}
    for root, dirs, files in os.walk(data_dir):
        for f in files: # Iterate through files in data_dir
            if f not in DATA_FILES:
                continue
            try:
                wheel = Spinner("Loading in {} data: ".format(f))
                with open(os.path.join(root, f)) as csvfile:
                    reader = csv.reader(csvfile)
                    data[f] = {}
                    data[f]["examples"] = []
                    data[f]["class"] = []
                    i = 0
                    for row in reader:
                        data[f]["examples"].append([ast.literal_eval(feature) for feature in row])
                        data[f]["class"].append(data[f]["examples"][i].pop(0))
                        i += 1
                        wheel.next()
                print("\n")
            except IOError:
                print("Error: Unable to open file '{}'".format(f))
                sys.exit()
    return data

def sigmoid(x):
    """
        Sigmoid activation function used for node in neural network.
        @param x: input value to be 'activated'
        @return: sigmoid(x)
    """
    return 1 / (1 + (math.e ** (-x)))

def sig_prime(x):
    """
        First derivative of sigmoid activation function.
        @param x: input value to pass to derivative of sigmoid
        @return: first derivative of sigmoid of value x
    """
    return sigmoid(x) * (1 - sigmoid(x))

if __name__ == "__main__":
    try:
        data_dir = sys.argv[1]
    except IndexError as err:
        print("Usage: python3 the_brain_train.py <path to directory containing training/test data>")
        sys.exit()
    start = time.time()
    data = load_data(data_dir)
    end = time.time()
    print("The program took {}s to run.".format(round(end - start, 2)))