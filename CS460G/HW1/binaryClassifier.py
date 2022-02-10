"""
    Binary Data Classifier
    by Ben Richey

    The following program contains solutions to two problems assigned
    as a part of homework 1 for CS460G (Machine Learning) given by Dr.
    Brent Harrison at the University of Kentucky.

    The first part implements the training and testing of a decision tree
    of maximum depth = 3 to classify (binary classification of) synthetic data
    provided by Dr. Harrison. We are training and testing on the same data set
    in this case.

    The second part implements the training and testing of a decision tree of
    maximum depth = 3 to classify Pokemon as either legendary or not legendary.
    This data was also provided by Dr. Harrison and we are testing on the same
    data we trained on.
    
    The MIT License (MIT)
    Copyright © 2022 <Ben Richey>

    Permission is hereby granted, free of charge, to any person obtaining a copy 
    of this software and associated documentation files (the “Software”), to deal
    in the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is furnished to do
    so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
    PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
    CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
    OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import os
import csv
import ast
import math
from treelib import Node, Tree
import ipdb

SYNTHETIC_AVOID_FILES = ["pokemonLegendary.csv", "pokemonStats.csv", "README.txt"]
POKEMON_AVOID_FILES = ["synthetic-1.csv", "synthetic-2.csv", "synthetic-3.csv",
                       "synthetic-4.csv", "README.txt"]
SYNTHETIC_1_NUM_BINS = 2
SYNTHETIC_2_NUM_BINS = 2
SYNTHETIC_3_NUM_BINS = 2
SYNTHETIC_4_NUM_BINS = 2

class TreeNode(object):

    def __init__(self, features, chosen_f, possible_f_vals, prediction):
        self.features = features
        self.chosenFeature = chosen_f
        self.children = possible_feature_vals
        self.prediction = prediction

class SyntheticDataSet:

    def __init__(self):
        self.features = {}
        self.classlist = [] 

    def __str__(self): # For debugging
        return "f1={}\nf2={}\nclass={}".format(self.feature1list, self.feature2list,
                                               self.classlist)

def check_all_same_class(data):
    """
        @param data = list of class values for each example in data set
        @return = False if the data is not pure or the class that the entire set is if pure
    """
    first_class = data[0]
    for item in data:
        if first_class != item:
            return False
    return first_class

def create_single_class(tree, data, the_class):
    prediction = the_class
    features = data.features.keys()
    chosen_f = None
    possible_f_vals = None
    tree.create_node("Root", "root", data=TreeNode(features, chosen_f, possible_f_vals, prediction))

def find_most_common_class(data, possible_class_vals):
    most_common = possible_class_vals[0]
    the_max = 0
    for val in possible_class_vals:
        if num_samples_of_class(data, val) > the_max:
            the_max = num_samples_of_class(data, val)
            most_common = val
    return most_common

def check_no_features(tree, data):
    if len(data.features.keys()) == 0:
        the_class = find_most_common_class(data.classlist, possible_class_vals)
        create_single_class(tree, data, the_class)

def syntheticID3(tree, data):
    one_class = check_all_same_class(data.classlist)
    if (one_class):
        create_single_class(tree, data, one_class)
        return
    if (check_no_features(tree, data)):
        return

def entropy(data, possible_classes):
    """
        @param data = python list containing class value for each example in data set
        @param possible_classes = all possible class values. ex: binary classes = [0,1]
    """
    entropy = 0
    # iterate through all possible classes
    for clss in possible_classes:
        # calculate probability of current class
        prob = num_samples_of_class(data, clss) / len(data)
        if prob == 0.0:
            return prob
        # add to entropy summation
        entropy += -prob * math.log(prob, 2)
    return entropy

def num_samples_of_class(class_data, clss):
    count = 0
    for example in class_data:
        if example == clss:
            count += 1
    return count

def get_subset(data, feature, val):
    subset = SyntheticDataSet()
    for f in data.features.keys():
        subset.features[f] = []
    for i in range(len(data.features[feature])):
        if data.features[feature][i] == val:
            for f in subset.features.keys():
                subset.features[f].append(data.features[f][i])
            subset.classlist.append(data.classlist[i])
    return subset

def information_gain(data, feature, possible_feature_vals, possible_class_vals):
    """
        @param data = SyntheticDataSet object
        @param feature = feature you're splitting on
        @param possible_feature_vals = possible values a feature could be
        @return information gained by splitting on given feature
    """
    e = entropy(data.classlist, possible_class_vals)
    summation = 0
    for val in possible_feature_vals:
        subset = get_subset(data, feature, val)
        prob =  len(subset.classlist) / len(data.classlist)
        summation += prob * entropy(subset.classlist, possible_class_vals)
    return e - summation

def discretize(curr_data, num_bins):
    # Discretize all sets of feature values using <num_bins> equidistant bins
    for feature_list in curr_data.features.values():
        feature_interval = (max(feature_list) - min(feature_list)) // num_bins
        val_bounds = [min(feature_list) + ((i + 1) * feature_interval) for i in range(num_bins - 1)]
        for i in range(len(feature_list)):
            feature_set = False
            for j in range(len(val_bounds)):
                if feature_list[i] < val_bounds[j]:
                    feature_set = True
                    feature_list[i] = j
                    break
            if not feature_set:
                feature_list[i] = num_bins - 1

def determine_synthetic_num_bins(filename):
    if "1" in filename:
        return SYNTHETIC_1_NUM_BINS
    if "2" in filename:
        return SYNTHETIC_2_NUM_BINS
    if "3" in filename:
        return SYNTHETIC_3_NUM_BINS
    if "4" in filename:
        return SYNTHETIC_4_NUM_BINS
    else:
        print("Error: corrupted data directory")
        sys.exit()

def build_and_test_synthetic_data_classifier(data_dir):
    # dictionary to store tree for each synthetic data set
    decision_trees = {}
    # Load in training/test data
    data = load_synthetic_data(data_dir)
    # Iterate through all data sets and make decision trees
    for dataset in data.keys():
        curr_data = data[dataset]
        num_bins = determine_synthetic_num_bins(dataset) # Allow different number of bins per file
        discretize(curr_data, num_bins)
        decision_trees[dataset] = Tree()
        ID3(decision_trees[dataset], curr_data)

def load_synthetic_data(data_dir):
    synthetic_data = {}
    for root, dirs, files in os.walk(data_dir):
        for f in files: # Iterate through files in data_dir
            if f in SYNTHETIC_AVOID_FILES:
                continue # Skip pokemon files and README
            try:
                with open(os.path.join(root, f)) as csvfile:
                    filedata = SyntheticDataSet()
                    reader = csv.reader(csvfile)
                    filedata.features["f1"] = []
                    filedata.features["f2"] = []
                    for row in reader: # Read in each row and store in SyntheticDataSet object
                        filedata.features["f1"].append(ast.literal_eval(row[0]))
                        filedata.features["f2"].append(ast.literal_eval(row[1]))
                        filedata.classlist.append(ast.literal_eval(row[2]))
                    synthetic_data[f] = filedata # Store all file data in dictionary
            except IOError as err:
                print("Error: Unable to open file {}".format(f))
                sys.exit()
    return synthetic_data

def build_and_test_pokemon_classifier(data_dir):
    #TODO
    pass

if __name__ == "__main__":
    try:
        data_dir = sys.argv[1]
    except IndexError as err:
        print("Usage: python3 binaryClassifier.py <full path to data directory>")
        sys.exit()

    build_and_test_synthetic_data_classifier(data_dir)
    build_and_test_pokemon_classifier(data_dir)
