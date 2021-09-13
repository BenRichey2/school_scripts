"""
    Sorting Algorithm Analyzer
      by Ben Richey

    The following program instantiates the Sortalyzer class which performs a run-time analysis
    on three sorting algorithms: insertion sort, quick sort, and merge sort. This run-time
    analysis is performed by counting the number of comparisons done by each algorithm. The
    class also visualizes this run-time analysis via the matplotlib library.

    MIT License:

    Permission is hereby granted, free of charge, to any person obtaining a copy of this
    software and associated documentation files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or
    substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
    BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
# std libs
import os
import sys
import argparse
import ast
import csv

# 3rd party libs
import matplotlib # Tool to visualize run-time analysis

# debug
import ipdb

class Sortalyzer():
    """
        Sortalyzer class performs run-time analysis on insertion sort, quick sort, and merge sort
        algorithms by counting number of comparisons performed. Each of these algorithms will be
        tested against several different data sets in different sorted orders (sorted, reverse
        sorted, and random). Then, a graph will be generated which vizualizes the efficiency of 
        each algorithm for comparison.
    """

    def __init__(self):
        self.parse_arguments()
        # Load in data to sort
        self.load_data()
        # Run sorts on each data set
        self.insertion_sort()
        self.quick_sort()
        self.merge_sort()
        # Graph run-time data
        self.visualize_results()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="Perform run-time analysis on three " +
                                         "different sorting algorithms")
        parser.add_argument("--data_path",
                            help="Full path to directory containing data to be sorted. " +
                            "Assumes this directory contains nothing but the csv files " +
                            "containing the data to sort.",
                            required=True)
        args = parser.parse_args()
        self.data_path = args.data_path

    def load_data(self):
        self.data_sets = {}
        try:
            for (root, dirs, files) in os.walk(self.data_path, topdown=True):
                for f in files:
                    if f == "pokemonIndex.csv":
                        continue
                    else:
                        data_list = []
                        with open(os.path.join(root, f)) as csvfile:
                            csv_reader = csv.reader(csvfile)
                            for row in csv_reader:
                                if row[0].startswith("Pokemon"):
                                    continue
                                else:
                                    data_list.append(ast.literal_eval(row[1]))
                            self.data_sets[f] = data_list
        except (OSError, IOError, ValueError) as err:
            print("Error: " + err)
            sys.exit()

    def insertion_sort(self):
        self.insertion_sort_count = 1
        #TODO
        pass

    def quick_sort(self):
        self.quick_sort_count = 1
        #TODO
        pass

    def merge_sort(self):
        self.merge_sort_count = 1
        #TODO
        pass

if __name__ == "__main__":
    # instantiate object & perform analysis
    sort_analyzer = Sortalyzer()
