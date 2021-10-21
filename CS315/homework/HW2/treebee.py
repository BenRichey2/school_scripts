"""
    This program implements a binary search tree and most of the common member functions with
    BST's.
"""

import os
import sys
import csv
import ast
import itertools

# Debug
import ipdb

# full path of directory contain data files
DATA_PATH = "/home/brich/src/school_scripts/CS315/homework/HW2/data"

class BinarySearchTree:
    """
        This is an array (or since we're in python land, list) based binary search tree.
        It will dynamically increase its size as needed as nodes are added to the tree.
        Supported methods include search, insert, min, and max. I am not implementing delete
        because it is not required for the coding project this was written for.
    """

    def __init__(self):
        self.bst = []

    def search(self, idx, value):
        try:
            if self.bst[idx] == None: # Not found
                return -1
            elif self.bst[idx] == value:
                return idx
            elif self.bst[idx] < value:
                self.search(2 * idx + 1, value)
            else:
                self.search(2 * idx + 2, value)
        except IndexError: # Tree full and not found
            return -1

    def insert(self, idx, value):
        assert type(value) == type(1), "invalid attempt to insert non-integer"
        try:
            if self.bst[idx] == None:
                self.bst[idx] = value
            elif value < self.bst[idx]:
                self.insert(2 * idx + 1, value)
            else:
                self.insert(2 * idx + 2, value)
        except IndexError: # The tree is empty or full so we're going to double the size
            self.doubleSize()
            self.insert(idx, value)

    def min(self, idx):
        try:
            while self.bst[2 * idx + 1] != None:
                self.min(2 * idx + 1)
            return self.bst[idx]
        except IndexError: # The tree is empty or full, so we never reach a None element
            return self.bst[idx]

    def max(self, idx):
        try:
            while self.bst[2 * idx + 2] != None:
                self.max(2 * idx + 2)
            return self.bst[idx]
        except IndexError: # The tree is empty or full, so we never reach a None element
            return self.bst[idx]

    def doubleSize(self):
        size = len(self.bst)
        if size == 0: # If this is an empty tree, start out with empty root
            self.bst = [None]
            return
        newBst = list(itertools.chain(self.bst, [None]*(size + 1)))
        self.bst = newBst

    def showInOrder(self, idx):
        try:
            while self.bst[idx] is not None:
                self.showInOrder(2 * idx + 1)
                print(self.bst[idx], end=",")
                self.showInOrder(2 * idx + 2)
                return
        except IndexError: # We've reached a leaf so exit
            return

if __name__ == "__main__":
    # Load in data from csv files
    data = {}
    try:
        for (root, dirs, files) in os.walk(DATA_PATH, topdown=True):
            for f in files:
                data[f] = []
                with open(os.path.join(root, f)) as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for row in csv_reader:
                        data[f].append(ast.literal_eval(row[0]))
    except (IOError, ValueError) as err:
         print("Error: " + str(err))
         sys.exit()

    # Test tree implementation
    trees = {}
    for filename in data.keys():
        # Create a binary search tree for each file
        trees[filename] = BinarySearchTree()
        for node in data[filename]:
            # Insert each node starting at the root
            trees[filename].insert(0, node)

    # Print traversals
    print("\nInorder Traversal: \n")
    for tree in trees.keys():
        print("{}:".format(tree))
        trees[tree].showInOrder(0)
        print("\n")
