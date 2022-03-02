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
import yaml
from progress.spinner import Spinner

# Debugging
import ipdb
import time

WINE_FILE = "winequality-red.csv"
SYNTHETIC_FILES = ["synthetic-1.csv", "synthetic-2.csv"]

REG_MODELS = {} # Contains theta values for each model
ALPHAS = {}     # Contains alpha hyper parameter for each model
ALPHAS["wine"] = 0.001
ALPHAS["synthetic_1_o2"] = 0.001
ALPHAS["synthetic_1_o3"] = 0.6
ALPHAS["synthetic_1_o5"] = 0.65
ALPHAS["synthetic_2_o2"] = 0.6
ALPHAS["synthetic_2_o3"] = 0.1
ALPHAS["synthetic_2_o5"] = 0.1
TIME_STEPS = 100000 # Hyper parameter limiting how long any one model can train
BENCHMARKS = {}
BENCHMARKS["wine"] = 1.2
BENCHMARKS["synthetic_1_o2"] = 33.0
BENCHMARKS["synthetic_1_o3"] = 9.0
BENCHMARKS["synthetic_1_o5"] = 9.5
BENCHMARKS["synthetic_2_o2"] = 0.35
BENCHMARKS["synthetic_2_o3"] = 0.35
BENCHMARKS["synthetic_2_o5"] = 0.35
ALPHA_ADAPTATION = 0.000001 # Hyper parameter determining how much alpha gets adjusted on each time step

def load_file_data(data_dir, filename, synthetic):
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
                        data["order_1"] = []
                        data["classification"] = []
                        for row in reader:
                            data["order_1"].append(ast.literal_eval(row[0]))
                            data["classification"].append(ast.literal_eval(row[1]))
            except IOError:
                print("Error: Unable to open file '{}'".format(f))
                sys.exit()
    return data

def store_models(data_dir):
    """
        Store the trained theta parameters for each model to a yaml file on disk.
        @param data_dir: the directory containing the data used for training/testing
        @result: Stores a dictionary to a yaml file where the keys are the model names
                 and the values are theta 0, theta 1, theta 2, ..., theta n.
    """
    # Convert np.ndarray objects to lists for writing to disk
    for model in REG_MODELS.keys():
        theta_vals = REG_MODELS[model].tolist()
        REG_MODELS[model] = theta_vals
    try:
        with open(os.path.join(data_dir, "model_parameters.yaml"), "w+") as f:
            yaml.dump(REG_MODELS, f)
            print("Saved training parameters to {}".format(os.path.join(data_dir, "model_parameters.yaml")))
    except IOError as err:
        print("Error: unable to store training data to {}".format(os.path.join(data_dir, "model_parameters.yaml")))

def preprocess_data(data):
    """
        Converts each feature value for each feature to a value between zero and 1
        while preserving the relationships between values in a feature set.
        @param data: dictionary containing data set. Keys = feature names,
                     Values = feature vals for each example. One special key, called
                     'classification', has a value of a list of the correct classification
                     for each example.
    """
    for feature in data.keys():
        if feature == "classification":
            continue
        the_max = max(data[feature])
        the_min = min(data[feature])
        new_vals = [((val - the_min) / (the_max - the_min)) for val in data[feature]]
        data[feature] = new_vals
    return

def basis_expansion(data, order):
    """
        Perform basis expansion on single feature data by creating new features using
        <data>'s features up to the power of the given order.
        @param data: dictionary containing single feature data set. Keys = feature names,
                     Values = feature vals for each example. One special key, called
                     'classification', has a value of a list of the correct classification
                     for each example.
        @param order: the highest polynomal order desired. Must be at least 2
    """
    if order < 2:
        print("Basis Expansion Error: Cannot raise features to a power lower than 2")
        sys.exit()
    new_data = {}
    new_data["classification"] = [val for val in data["classification"]]
    new_data["order_1"] = [val for val in data["order_1"]]
    for i in range(2, order+1):
        new_data["order_{}".format(i)] = [data["order_1"][j]**i for j in range(len(data["order_1"]))]
    return new_data

def linear_reg(x_vals, model):
    """
        Linear Regression Function
        @param x_vals: numpy ndarray of input values for each feature where first element is always 1
                       to account for theta_0. The rest are the theta_n to be multiplied by x_n
        @param model: which model to use
        @return:  h(X) = theta_0 + summation[theta_i*x_i for i in range(num_features)]
    """
    return np.dot(x_vals, REG_MODELS[model].transpose())

def loss_pdwrtj(j, model, data):
    """
        Partial derivative w/ respect to feature j of the loss function (0.5*mean squared error)
        for multiple regression
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

def gradient_descent(data, model):
    """
        Trains theta_0 through theta_n values for n feature gradient descent
        @param data: dictionary where key = feature name and value = list of values
                     for that feature. One special key, called 'classification',
                     has a value of a list of the correct classification for each
                     example.
        @param model: model to train
        @result: Trains the given model TIME_STEPS times, storing the theta values
                 in REG_MODELS[model]. Uses full batch update for updating theta vals.
    """
    wheel = Spinner("Training {} model: ".format(model))
    prev_loss = None
    for step in range(TIME_STEPS):
        wheel.next()
        curr_loss = 0
        for j in range(len(REG_MODELS[model])):
            loss = loss_pdwrtj(j, model, data)
            new_theta = REG_MODELS[model][j] - (ALPHAS[model] * loss)
            REG_MODELS[model][j] = new_theta
            curr_loss += loss
        curr_loss = curr_loss / len(REG_MODELS[model])
        # Adaptive alpha
        if prev_loss:
            if prev_loss < curr_loss: # If avg loss increases, decrease alpha
                ALPHAS[model] *= (1 - ALPHA_ADAPTATION)
            else: # If avg loss decreases, increase alpha
                ALPHAS[model] *= (1 + ALPHA_ADAPTATION)
            prev_loss = curr_loss
        else:
            prev_loss = curr_loss
        m = mse(data, model)
        if m < BENCHMARKS[model]:
            print("\n\nMSE reached {} for {} model. Ending training.".format(m, model))
            print("{} model's theta 0 through theta n values are: {}".format(model, REG_MODELS[model].tolist()))
            return
    print("{} model unable to reach benchmark in {} time steps. It may have diverged or".format(model, TIME_STEPS)
          + " the hyper parameters need to be adjusted.")

def mse(data, model):
    """
        Computes the mean squared error for the given model
        @param data: dictionary where key = feature name and value = list of values
                     for that feature. One special key, called 'classification',
                     has a value of a list of the correct classification for each
                     example.
        @param model: model to train
        @return: mean squared error of model on training data
    """
    sum = 0
    keys = [ k for k in data.keys() if k != "classification"]
    m = len(data[keys[0]])
    for i in range(m):
        vals = [data[f][i] for f in keys]
        vals.insert(0, 1.0) # Prepend w/ 1 to account for theta_0
        x_vals = np.asarray(vals, dtype=float)
        sum += (linear_reg(x_vals, model) - data["classification"][i]) ** 2
    return sum * (1 / m)

def train_multiple_order_poly_models(data, model):
    """
        Trains polynomial regression models for orders 2, 3, and 5 for the given dataset.
        @param data: dictionary where key = feature name and value = list of values
                     for that feature. One special key, called 'classification',
                     has a value of a list of the correct classification for each
                     example.
    """
    orders = [2, 3, 5]
    for order in orders:
        order_data = basis_expansion(data, order)
        curr_model = model + "_o{}".format(order)
        REG_MODELS[curr_model] = np.asarray([np.random.rand() for theta in range(order+1)])
        gradient_descent(order_data, curr_model)

if __name__ == "__main__":

    start_time = time.time()
    try:
        data_dir = sys.argv[1]
    except IndexError as err:
        print("Usage: python3 regressinator.py <path to data directory>")
        sys.exit()

    # Load in wine data
    wine_data = load_file_data(data_dir, WINE_FILE, False)
    wine_data["classification"] = wine_data["quality"]
    del wine_data["quality"]
    # Standardize wine data
    preprocess_data(wine_data)
    # Randomly initialize theta vals
    REG_MODELS["wine"] =  np.asarray([np.random.rand() for theta in range(len(wine_data.keys()))])
    # Train wine model
    gradient_descent(wine_data, "wine")
    # Load in synthetic 1 data
    synthetic_1_data = load_file_data(data_dir, SYNTHETIC_FILES[0], True)
    # Standardize synthetic 1 data
    preprocess_data(synthetic_1_data)
    # Train models of order 2, 3, and 5 for synthetic 1 data
    train_multiple_order_poly_models(synthetic_1_data, "synthetic_1")
    # Load in synthetic 2 data
    synthetic_2_data = load_file_data(data_dir, SYNTHETIC_FILES[1], True)
    # Standardize synthetic 2 data
    preprocess_data(synthetic_2_data)
    # Train models of order 2, 3, and 5 for synthetic 2 data
    train_multiple_order_poly_models(synthetic_2_data, "synthetic_2")
    store_models(data_dir)
    end_time = time.time()
    time_elapsed = (end_time - start_time) / 60
    print("The program took {} minutes to run.".format(time_elapsed))