"""
    Sorting Algorithm Analyzer
      by Ben Richey

    The following program instantiates the Sortalyzer class which performs a run-time analysis
    on three sorting algorithms: insertion sort, quick sort, and merge sort. This run-time
    analysis is performed by counting the number of comparisons done by each algorithm. The run-time
    data is then printed to stdout, and the sorted lists are saved in a file called
    "sorted_pokemon.yaml" saved to the directory in which this script was invoked.

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
import math
import copy
import argparse
import ast
import csv
import yaml

# debug
import ipdb

class Pokemon:
    """
        A data structure to represent each pokemon being sorted.
    """

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return (self < other) or (self.score == other.score)

    def __eq__(self, other):
        return (self.score == other.score)

    def __gt__(self, other):
        return self.score > other.score

class Sortalyzer():
    """
        Sortalyzer class performs run-time analysis on insertion sort, quick sort, and merge sort
        algorithms by counting number of comparisons performed. Each of these algorithms will be
        tested against several different data sets in different sorted orders (sorted, reverse
        sorted, and random). Then, the runtime data is printed to stdout, and the sorted lists are
        saved in a file called "sorted_pokemon.yaml" saved to the directory in which this script
        was invoked.
    """

    def __init__(self):
        self.runtime_data = {}
        self.parse_arguments()
        # Load in data to sort
        self.load_data()
        # Run sorts on each data set
        self.insertion_sort_engine()
        self.merge_sort_engine()
        self.quick_sort_engine()
        # Confirm sorting is correct
        self.confirm_correct_output()
        # Graph run-time data
        self.dump_results()

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
        # NOTE: assumes the only files in the data directory are the pokemon .csv files to be sorted
        self.data_sets = {}
        self.data_sets["insertion"] = {}
        self.data_sets["merge"] = {}
        self.data_sets["quick"] = {}
        self.data_sets["correct"] = {} # Clean copy used to confirm lists are sorted correctly
        data = {}
        try: # Read the data from disk
            for (root, dirs, files) in os.walk(self.data_path, topdown=True):
                for f in files:
                    if f == "pokemonIndex.csv":
                        continue
                    else:
                        data[f] = []
                        with open(os.path.join(root, f)) as csvfile:
                            csv_reader = csv.reader(csvfile)
                            for row in csv_reader:
                                if row[0].startswith("Pokemon"):
                                    continue
                                else:
                                    pkmn = Pokemon(row[0], ast.literal_eval(row[1]))
                                    data[f].append(pkmn)
        except (OSError, IOError, ValueError) as err:
            print("Error: " + err)
            sys.exit()
        # Make copies of the data for each algorithm
        for algorithm in self.data_sets.keys():
            self.data_sets[algorithm] = copy.deepcopy(data)

    def insertion_sort_engine(self):
        data = {}
        for filename, pokemons in self.data_sets["insertion"].items():
            data[filename] = self.insertion_sort(pokemons)
        self.runtime_data["insertion"] = data

    def merge_sort_engine(self):
        data = {}
        for filename, pokemons in self.data_sets["merge"].items():
            self.merge_count = 0
            back = len(pokemons) - 1
            self.merge_sort(pokemons, 0, back)
            data[filename] = self.merge_count
        self.runtime_data["merge"] = data

    def quick_sort_engine(self):
        data = {}
        for filename, pokemons in self.data_sets["quick"].items():
            self.quick_count = 0
            self.quick_sort(pokemons, 0, len(pokemons) - 1)
            data[filename] = self.quick_count
        self.runtime_data["quick"] = data

    def insertion_sort(self, data):
        count = 0
        for j in range(1, len(data)):
            count += 1
            key = data[j]
            i = j - 1
            while (i >= 0) and (data[i] > key):
                count += 1
                data[i + 1] = data[i]
                i -= 1
            data[i + 1] = key
        return count

    def merge_sort(self, data, front, back):
        if front < back:
            middle = math.floor((front + back) / 2)
            self.merge_sort(data, front, middle)
            self.merge_sort(data, middle + 1, back)
            self.merge(data, front, middle, back)

    def merge(self, data, front, middle, back):
        left = []
        for idx in range(0, middle - front + 1):
            left.append(data[front + idx])
        left.append(Pokemon("End of List", math.inf))
        right = []
        for idx in range(0, (back - middle)):
            right.append(data[middle + idx + 1])
        right.append(Pokemon("End of List", math.inf))
        i = 0
        j = 0
        for k in range(front, back + 1):
            self.merge_count += 1
            if left[i] <= right[j]:
                data[k] = left[i]
                i += 1
            else:
                data[k] = right[j]
                j += 1

    def quick_sort(self, data, front, back):
        if front < back:
            middle = self.partition(data, front, back)
            self.quick_sort(data, front, middle - 1)
            self.quick_sort(data, middle + 1, back)

    def partition(self, data, front, back):
        pivot = data[front]
        i = front + 1
        for j in range(front + 1, back + 1):
            self.quick_count += 1
            if data[j] <= pivot:
                tmp = data[i]
                data[i] = data[j]
                data[j] = tmp
                i += 1
        tmp = data[i-1]
        data[i-1] = data[front]
        data[front] = tmp
        return i - 1

    def confirm_correct_output(self):
        # Sort the list of pokemon using pythons native method
        for filename, pokelist in self.data_sets["correct"].items():
            pokelist.sort()
        # Compare output from my sorting algorithms to python's
        for filename in self.data_sets["insertion"].keys():
            l1 = self.data_sets["insertion"][filename]
            l2 = self.data_sets["merge"][filename]
            l3 = self.data_sets["quick"][filename]
            l4 = self.data_sets["correct"][filename]
            self.compare_lists(l1, l2, l3, l4, filename)

    def compare_lists(self, l1, l2, l3, l4, filename):
        # Compare 4 lists
        if len(l1) != len(l2) or len(l2) != len(l3) or len(l3) != len(l4):
            print("ERROR: sorted lists for {} not equal. Unequal length.".format(filename))
            return False
        for idx in range(0, len(l1)):
            if (l1[idx] == l2[idx]) and (l2[idx] == l3[idx]) and (l3[idx] == l4[idx]):
                continue
            else:
                print("ERROR: sorted lists for {} not equal. Different ordering.".format(filename))
                return False
        return True

    def dump_results(self):
        self.data_sets.pop("correct")
        try:
            with open(os.path.join(os.getcwd(), "sorted_pokemon.yaml"), "w+") as output:
                yaml.dump(self.data_sets, output)

        except (IOError, OSError) as err:
            print("Error encountered when saving sorted data to disk: {}".format(err))
        print("\n---------------------------------------------------------------------")
        print("| Run-time Analysis for Insertion, Merge, and Quick Sort Algorithms |")
        print("---------------------------------------------------------------------\n")
        yaml.dump(self.runtime_data, sys.stdout)
        print("\n---------------------------------------------------------------------")
        print("Sorted Pokemon saved to \"./sorted_pokemon.yaml\"")
        print("---------------------------------------------------------------------\n")


if __name__ == "__main__":
    # instantiate object & perform analysis
    sort_analyzer = Sortalyzer()
