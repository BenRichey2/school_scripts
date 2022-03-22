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
import numpy as np

import ipdb

DATA_FILES = ["mnist_test_0_1.csv", "mnist_train_0_1.csv"]
NUM_HIDDEN_NODES = 2
NUM_FEATURES = 784
ALPHA = 0.005
TIME_STEPS = 100
BENCHMARK = 99.0

def load_file_data(data_dir, filename):
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
            if f != filename:
                continue
            try:
                print("Loading in {} data...".format(f))
                with open(os.path.join(root, f)) as csvfile:
                    reader = csv.reader(csvfile)
                    data["examples"] = []
                    data["class"] = []
                    i = 0
                    for row in reader:
                        data["examples"].append([float(ast.literal_eval(feature)) for feature in row])
                        data["class"].append(data["examples"][i].pop(0))
                        i += 1
            except IOError:
                print("Error: Unable to open file '{}'".format(f))
                sys.exit()
    return data

def preprocess_data(data):
    """
        Converts each feature value for each feature to a value between zero and 1
        while preserving the relationships between values in a feature set.
        @param data: list of lists where each inner list is the set of feature values
                     for an example
    """
    for i in range(NUM_FEATURES):
        the_max = data[:, i].max()
        the_min = data[:, i].min()
        if the_max == 0.0: # To account for features where all values are zero
            new_vals = [0.0 for val in data[:, i]]
        else:
            new_vals = [((val - the_min) / (the_max - the_min)) for val in data[:, i]]
        data[:, i] = new_vals
    return np.asarray(data)

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

def train_model(examples, classes, hidden_weights, output_weights, hidden_bias, output_bias):
    """
        Trains feed forward neural network containing one hidden layer and a
        single node output layer
        @param examples: Nested numpy array of training data where rows are feature values
        for one example. Columns are feature values for one feature.
        @param classes: Single numpy array of class values for each example
        @param hidden_weights: Nested numpy array where rows are weights for one node of
        hidden layer. Columns are weights for one feature for all hidden layer nodes.
        @param output_weights: Single numpy array where each element is the weight between
        the a hidden layer node and the output layer node.
        @param hidden_bias: bias terms for hidden layer
        @param output_bias: bias terms for output layer
        @return: tuple containing trained (hidden_weights, output_weights) pair
    """
    prev_acc = None
    last_10_accs = []
    divergence = False
    for epoch in range(TIME_STEPS):
        for i in range(len(examples)): # This is one epoch
            # Generate output at hidden layer
            hidden_input = np.dot(hidden_weights, examples[i]) + hidden_bias # NUM_HIDDEN_NODES x 1
            hidden_output = np.asarray(list(map(sigmoid, hidden_input))) # NUM_HIDDEN_NODES x 1
            # Generate input to output layer
            output_layer_input = np.dot(output_weights.transpose(), hidden_output) + output_bias # scalar value
            output = sigmoid(output_layer_input)
            # Calculate output error
            error = classes[i] - output
            # Compute output layer delta
            output_delta = error * sig_prime(output_layer_input)
            # Propagate delta to hidden layer
            hidden_deltas = [sig_prime(hidden_input[j]) * output_weights[j] * output_delta
                             for j in range(len(hidden_input))]
            # Update weights for all layers
            output_weights = [output_weights[j] + (ALPHA * hidden_output[j] * output_delta)
                              for j in range(len(output_weights))]
            output_weights = np.asarray(output_weights) # Convert back to numpy array
            output_bias = output_bias + (ALPHA * output_delta)
            old_hidden_weights = hidden_weights
            hidden_weights = []
            for node_idx in range(len(old_hidden_weights)):
                hidden_weights.append([old_hidden_weights[node_idx, j] +
                                                       (ALPHA * examples[i, j] * hidden_deltas[node_idx])
                                                       for j in range(NUM_FEATURES)])
            hidden_weights = np.asarray(hidden_weights) # Convert back to numpy array
            hidden_bias = np.asarray([(hidden_bias[j] + (ALPHA * hidden_deltas[j])) for j in range(len(hidden_bias))])
            if i % 1000 == 0:
                accuracy = compute_accuracy(examples, classes, hidden_weights, output_weights, hidden_bias, output_bias)
                # Check for divergence
                if prev_acc:
                    if prev_acc > accuracy:
                        print("Divergence detected. Restarting training.")
                        return "D"
                prev_acc = accuracy
                if len(last_10_accs) < 10:
                    last_10_accs.append(accuracy)
                else:
                    last_10_accs.pop(0)
                    last_10_accs.append(accuracy)
                    for i in range(len(last_10_accs)):
                        if last_10_accs[0] == last_10_accs[i]:
                            divergence = True
                        else:
                            divergence = False
                    if divergence:
                        print("Divergence detected. Restarting training.")
                        return "D"
                print("Accuracy: {}%".format(round(accuracy, 2)))
                if accuracy > BENCHMARK:
                    print("Training accuracy reached {}%. Ending Training.".format(round(accuracy, 2)))
                    return (hidden_weights, output_weights, hidden_bias, output_bias)
    print("Completed {} epochs and was unable to reach benchmark. Stopping training.".format(TIME_STEPS))
    return None

def compute_accuracy(examples, classes, hidden_weights, output_weights, hidden_bias, output_bias):
    """
        Tests the accuracy of FFNN represented by one hidden layer containing two nodes and
        one output layer contianing one node. This test is specific to the FFNN used to
        classify MNIST images as either the handwritten number zero or one.
        @param examples: Nested numpy array of training data where rows are feature values
        for one example. Columns are feature values for one feature.
        @param classes: Single numpy array of class values for each example
        @param hidden_weights: Nested numpy array where rows are weights for one node of
        hidden layer. Columns are weights for one feature for all hidden layer nodes.
        @param output_weights: Single numpy array where each element is the weight between
        the a hidden layer node and the output layer node.
        @param hidden_bias: bias terms for hidden layer
        @param output_bias: bias terms for output layer
        @return: percent correctly predicted from given dataset
    """
    num_correct = 0
    for i in range(len(examples)):
        # Generate output at hidden layer
        hidden_input = np.dot(hidden_weights, examples[i]) + hidden_bias # NUM_HIDDEN_NODES x 1
        hidden_output = np.asarray(list(map(sigmoid, hidden_input))) # NUM_HIDDEN_NODES x 1
        # Generate input to output layer
        output_layer_input = np.dot(output_weights.transpose(), hidden_output) + output_bias # scalar value
        output = sigmoid(output_layer_input)
        if output > 0.5:
            prediction = 1
        else:
            prediction = 0
        if prediction == classes[i]:
            num_correct += 1
    return (num_correct / len(examples)) * 100

if __name__ == "__main__":
    try:
        data_dir = sys.argv[1]
    except IndexError as err:
        print("Usage: python3 the_brain_train.py <path to directory containing training/test data>")
        sys.exit()
    start = time.time()
    load_start = time.time()
    training_data = load_file_data(data_dir, DATA_FILES[1])
    load_end = time.time()
    load_time = load_end - load_start
    print("Beginning training")
    train_start = time.time()
    # Extract training data into ndarray objects
    training_examples = training_data["examples"]
    training_examples = np.asarray(training_examples)
    training_class = training_data["class"]
    # Preprocess feature data
    training_examples = preprocess_data(training_examples)
    # Randomly initialize layer weights
    # NUM_HIDDEN_NODES x NUM_FEATURES
    hidden_weights = np.random.uniform(-1.0, 1.0, (NUM_HIDDEN_NODES, NUM_FEATURES))
    # NUM_HIDDEN_NODES x 1
    hidden_bias = np.random.uniform(-1.0, 1.0, NUM_HIDDEN_NODES)
    # NUM_HIDDEN_NODES x 1 b/c we only want one output node
    output_weights = np.random.uniform(-1.0, 1.0, NUM_HIDDEN_NODES)
    hidden_weights = np.random.uniform(-1.0, 1.0, (NUM_HIDDEN_NODES, NUM_FEATURES))
    # scalar value b/c 1 output node
    output_bias = np.random.uniform(-1.0, 1.0, 1)[0]
    # Begin training
    model = train_model(training_examples, training_class, hidden_weights, output_weights, hidden_bias, output_bias)
    while model == "D":
        hidden_weights = np.random.uniform(-1.0, 1.0, (NUM_HIDDEN_NODES, NUM_FEATURES))
        hidden_bias = np.random.uniform(-1.0, 1.0, NUM_HIDDEN_NODES)
        output_weights = np.random.uniform(-1.0, 1.0, NUM_HIDDEN_NODES)
        output_bias = np.random.uniform(-1.0, 1.0, 1)[0]
        model = train_model(training_examples, training_class, hidden_weights, output_weights, hidden_bias, output_bias)
    train_end = time.time()
    # Load in test data
    load_start = time.time()
    test_data = load_file_data(data_dir, DATA_FILES[0])
    load_end = time.time()
    load_time += load_end - load_start
    test_examples = np.asarray(test_data["examples"])
    test_class = test_data["class"]
    # Preprocess feature data
    test_examples = preprocess_data(test_examples)
    # Test model
    hidden_weights = model[0]
    output_weights = model[1]
    hidden_bias = model[2]
    output_bias = model[3]
    accuracy = compute_accuracy(test_examples, test_class, hidden_weights, output_weights, hidden_bias, output_bias)
    print("Test accuracy: {}%".format(round(accuracy, 2)))
    end = time.time()
    print("The program took {}s to run.".format(round(end - start, 2)))
    print("The program spent {}s loading in file data".format(round(load_time, 2)))
    print("The program spent {}s training".format(round(train_end - train_start, 2)))