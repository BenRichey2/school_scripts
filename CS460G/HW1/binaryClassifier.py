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
import ipdb

SYNTHETIC_AVOID_FILES = ["pokemonLegendary.csv", "pokemonStats.csv", "README.txt"]
POKEMON_AVOID_FILES = ["synthetic-1.csv", "synthetic-2.csv", "synthetic-3.csv",
                       "synthetic-4.csv", "README.txt"]
SYNTHETIC_1_NUM_BINS = 2
SYNTHETIC_2_NUM_BINS = 2
SYNTHETIC_3_NUM_BINS = 2
SYNTHETIC_4_NUM_BINS = 2

class SyntheticDataSet:

    def __init__(self):
        self.features = {}
        self.classlist = [] 

    def __str__(self): # For debugging
        return "f1={}\nf2={}\nclass={}".format(self.feature1list, self.feature2list,
                                               self.classlist)

def discretize(curr_data, num_bins):
    # Discretize all sets of feature values using <num_bins> equidistant bins
    for feature_list in curr_data.features.values():
        feature_interval = (max(feature_list) - min(feature_list)) // num_bins
        val_bounds = [(i + 1) * feature_interval for i in range(num_bins - 1)]
        for i in range(len(feature_list)):
            feature_set = False
            for j in range(len(val_bounds)):
                if feature_list[i] < val_bounds[j]:
                    feature_set = True
                    feature_list[i] = j
                    break
            if not feature_set:
                feature_list[i] = num_bins - 1

def build_and_test_synthetic_data_classifier(data_dir):
    decision_trees = {}
    # Load in training/test data
    data = load_synthetic_data(data_dir)
    ipdb.set_trace()
    # Iterate through all data sets and make decision trees
    for dataset in data.keys():
        curr_data = data[dataset]
        if "1" in dataset: # Allow for different number of bins per data set
            discretize(curr_data, SYNTHETIC_1_NUM_BINS)
        if "2" in dataset: # Allow for different number of bins per data set
            discretize(curr_data, SYNTHETIC_2_NUM_BINS)
        if "3" in dataset: # Allow for different number of bins per data set
            discretize(curr_data, SYNTHETIC_3_NUM_BINS)
        if "4" in dataset: # Allow for different number of bins per data set
            discretize(curr_data, SYNTHETIC_4_NUM_BINS)

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
                        filedata.classlist.append(row[2])
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
