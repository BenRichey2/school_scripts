"""
    This program implements a binary search tree and most of the common member functions with
    BST's.
"""

import os
import sys
import csv
import ast
import itertools
import math

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
                idx = 2 * idx + 1
            return self.bst[idx]
        except IndexError: # The tree is empty, so we never reach a None element
            return self.bst[idx]

    def max(self, idx):
        try:
            while self.bst[2 * idx + 2] != None:
                idx = 2 * idx + 2
            return self.bst[idx]
        except IndexError: # The tree is empty so we never reach a none element
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

    def showPreOrder(self, idx):
        try:
            while self.bst[idx] is not None:
                print(self.bst[idx], end=",")
                self.showPreOrder(2 * idx + 1)
                self.showPreOrder(2 * idx + 2)
                return
        except IndexError: # We've reached a leaf so exit
            return

    def showPostOrder(self, idx):
        try:
            while self.bst[idx] is not None:
                self.showPostOrder(2 * idx + 1)
                self.showPostOrder(2 * idx + 2)
                print(self.bst[idx], end=",")
                return
        except IndexError: # We've reached a leaf so exit
            return

    def calculateWastedSpace(self):
        emptyNodes = 0
        for node in self.bst:
            if node is None:
                emptyNodes += 1
        emptyPercent = (emptyNodes / len(self.bst)) * 100
        wastedkB = math.ceil((sys.getsizeof(None) * emptyNodes) / 1000)
        print("There are {} empty nodes. {:.2f}% of the tree is ".format(emptyNodes, emptyPercent)
                +"empty. {} kilobytes were wasted.".format(wastedkB))

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
    print("\n")
    for tree in trees.keys():
        print("{}:".format(tree))
        theMax = trees[tree].max(0)
        if theMax != 128:
            print("\tERROR: Reported max: {} but expected 128".format(theMax))
        theMin = trees[tree].min(0)
        if theMin != 0:
            print("\tERROR: Reported min: {} but expected 0".format(theMin))
        print("\tMax: {} Min: {}".format(theMax, theMin))
        print("\n\tInorder Traversal:")
        trees[tree].showInOrder(0)
        print("\n\tPreorder Traversal:")
        trees[tree].showPreOrder(0)
        print("\n\tPostorder Traversal:")
        trees[tree].showPostOrder(0)
        print("\n\tWasted memory:")
        trees[tree].calculateWastedSpace()
        print("\n")
