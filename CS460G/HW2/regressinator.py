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
import numpy as np
from tqdm import tqdm
import yaml

# Debugging
import ipdb

WINE_FILE = "winequality-red.csv"
SYNTHETIC_FILES = ["synthetic-1.csv", "synthetic-2.csv"]

REG_MODELS = {} # Contains theta values for each model
ALPHAS = {}     # Contains alpha parameter for each model
ALPHAS["wine"] = 0.00000001
ALPHAS["synthetic-1.csv"] = 0.00000001
ALPHAS["synthetic-2.csv"] = 0.00000001
TIME_STEPS = 10000

def load_file_data(data_dir, filename):
    data = {}
    for root, dirs, files in os.walk(data_dir):
        for f in files: # Iterate through files in data_dir
            if f != filename:
                continue
            try:
                with open(os.path.join(root, f)) as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        for i in range(len(row)):
                            data[row[i]] = []
                        break
                    keys = [key for key in data.keys()]
                    for row in reader:
                        for i in range(len(row)):
                            data[keys[i]].append(ast.literal_eval(row[i]))
            except IOError:
                print("Error: Unable to open file '{}'".format(f))
                sys.exit()
    return data

def preprocess_data(data):
    """
        Converts each feature value for each feature to a value between zero and 1
        while preserving the weights of each value.
        @param data: dictionary containing data set. Keys = feature names,
                     Values = feature vals for each example. One special key, called
                     'classification', has a value of a list of the correct classification
                     for each example.
    """
    for feature in data.keys():
        if feature == "classification":
            continue
        the_sum = sum(data[feature])
        new_vals = [val / the_sum for val in data[feature]]
        data[feature] = new_vals
    return

def linear_reg(x_vals, model):
    """
        Linear Regression Function
        @param x_vals: numpy ndarray of input values for each feature where first element is always 1
                       to account for theta_0. The rest are the theta_n to be multiplied by x_n
        @param model: which model to use
        @return:  h(X) = theta_0 + summation[theta_i*x_i for i in range(num_features)]
    """
    return np.dot(x_vals, REG_MODELS[model].transpose())

def lin_loss_pdwrtj(j, model, data):
    """
        Partial derivative w/ respect to feature j of the loss function (0.5*mean squared error)
        for linear regression
        @param j: the index of the theta we are computing the partial derivative w.r.t
        @param model: the model we're using
        @param data: dictionary containing data set. Keys = feature names,
                     Values = feature vals for each example. One special key, called
                     'classification', has a value of a list of the correct classification
                     for each example.
        @return: value computed from partial derivative of loss fnxn w.r.t theta_j
    """
    sum = 0
    keys = [ k for k in data.keys() if k != "classification"]
    m = len(data[keys[0]])
    for i in range(m):
        vals = [data[f][i] for f in keys]
        vals.insert(0, 1.0) # Prepend w/ 1 to account for theta_0
        x_vals = np.asarray(vals, dtype=float)
        sum += (linear_reg(x_vals, model) - data["classification"][i]) * x_vals[j]
    return sum * (1 / m)

def linear_gradient_descent(data, model):
    """
        Trains theta_0 through theta_n values for n feature linear gradient descent
        @param data: dictionary where key = feature name and value = list of values
                     for that feature. One special key, called 'classification',
                     has a value of a list of the correct classification for each
                     example.
        @param model: model to train
        @result: Trains the given model TIME_STEPS times, storing the theta values
                 in REG_MODELS[model]. Uses full batch update for updating theta vals.
    """
    for step in tqdm(range(TIME_STEPS), desc="Training {} model".format(model)):
        for j in range(len(REG_MODELS[model])):
            new_theta = REG_MODELS[model][j] - (ALPHAS[model] * lin_loss_pdwrtj(j, model, data))
            REG_MODELS[model][j] = new_theta

if __name__ == "__main__":

    try:
        data_dir = sys.argv[1]
    except IndexError as err:
        print("Usage: python3 regressinator.py <path to data directory>")
        sys.exit()

    wine_data = load_file_data(data_dir, WINE_FILE)
    wine_data["classification"] = wine_data["quality"]
    del wine_data["quality"]
    preprocess_data(wine_data)
    # Randomly initialize theta vals
    REG_MODELS["wine"] =  np.asarray([np.random.rand() for theta in range(len(wine_data.keys()))])
    linear_gradient_descent(wine_data, "wine")
    try:
        with open(os.path.join(data_dir, "model_parameters.yaml")) as f:
            yaml.dump(REG_MODELS, f)
            print("Saved training parameters to {}".format(os.path.join(data_dir, "model_parameters.yaml")))
    except IOError as err:
        print("Error: unable to store training data to {}".format(os.path.join(data_dir, "model_parameters.yaml")))