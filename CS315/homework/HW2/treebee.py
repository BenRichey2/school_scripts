"""
        This program implements an array based binary search tree and an array based heap. Each of
    these data structures can only store integers. The binary search tree supports searches, finding
    the max and min values, inserting into the tree, printing the in order, pre order, and post
    order traversals,  how much space is wasted, and the height of the tree. However, it does not
    support node deletion because that was not required for this assignment due to the difficulty of
    deleting elements from an array based BST. The heap supports insertion and converting the heap
    into a max heap. I also added test code to confirm things are working properly.

    by Ben Richey

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
import csv
import ast
import itertools
import math
import argparse

# Debug
import ipdb

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
        """
            Search for the first instance of a value in a tree. To search the entire tree,
            call this method with idx=0.
            @return: idx of first instance of value. -1 if not found
        """
        try:
            if self.bst[idx] == None: # Not found
                return -1
            elif self.bst[idx] == value:
                return idx
            elif self.bst[idx] < value:
                return self.search(2 * idx + 2, value)
            else:
                return self.search(2 * idx + 1, value)
        except IndexError: # Tree full and not found or tree is empty
            return -1

    def insert(self, idx, value):
        """
            Inserts value into a binary search tree. To insert an element, call this
            with idx = 0.
        """
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
        """
            Finds the minimum value in the tree. Call this with idx = 0
        """
        try:
            while self.bst[2 * idx + 1] != None:
                idx = 2 * idx + 1
            return self.bst[idx]
        except IndexError: # The tree is empty, so we never reach a None element
            return self.bst[idx]

    def max(self, idx):
        """
            Finds the maximum value in the tree. Call this with idx = 0
        """
        try:
            while self.bst[2 * idx + 2] != None:
                idx = 2 * idx + 2
            return self.bst[idx]
        except IndexError: # The tree is empty so we never reach a none element
            return self.bst[idx]

    def doubleSize(self):
        """
            Helper function to dynamically increase the size of the tree in the event
            that we attempt to insert a node into a non-existent space.
        """
        size = len(self.bst)
        if size == 0: # If this is an empty tree, start out with empty root
            self.bst = [None]
            return
        newBst = list(itertools.chain(self.bst, [None]*(size + 1)))
        self.bst = newBst

    def showInOrder(self, idx):
        """
            Prints the in order traversal of the bst. Call with idx = 0 to see full tree.
        """
        try:
            while self.bst[idx] is not None:
                self.showInOrder(2 * idx + 1)
                print(self.bst[idx], end=",")
                self.showInOrder(2 * idx + 2)
                return
        except IndexError: # We've reached a leaf so exit
            return

    def showPreOrder(self, idx):
        """
            Prints the pre order traversal of the bst. Call with idx = 0 to see full tree.
        """
        try:
            while self.bst[idx] is not None:
                print(self.bst[idx], end=",")
                self.showPreOrder(2 * idx + 1)
                self.showPreOrder(2 * idx + 2)
                return
        except IndexError: # We've reached a leaf so exit
            return

    def showPostOrder(self, idx):
        """
            Prints the post order traversal of the bst. Call with idx = 0 to see full tree.

        """
        try:
            while self.bst[idx] is not None:
                self.showPostOrder(2 * idx + 1)
                self.showPostOrder(2 * idx + 2)
                print(self.bst[idx], end=",")
                return
        except IndexError: # We've reached a leaf so exit
            return

    def calculateWastedSpace(self):
        """
            I noticed how wasteful in memory this implementation is, so I added this to
            tell the user how much memory is being wasted!
        """
        emptyNodes = 0
        for node in self.bst:
            if node is None:
                emptyNodes += 1
        emptyPercent = (emptyNodes / len(self.bst)) * 100
        wastedkB = math.ceil((sys.getsizeof(None) * emptyNodes) / 1000)
        print("There are {} empty nodes. {:.2f}% of the tree is ".format(emptyNodes, emptyPercent)
                +"empty. {} kilobytes were wasted.".format(wastedkB))

    def computeNodeDepth(self, node, heights):
        """
            Computes how many hops it takes to reach the root from the current node. A helper
            function that helps determine the height of the tree
        """
        # If we've already computed the height, just return it
        if heights[node] != 0:
            return heights[node]
        # Figure out if its the root node or a left/right child
        if node == 0:
            # Root node: height = 1
            heights[node] = 1
            return heights[node]
        elif (node - 1) % 2 == 0:
            # This is a left child
            parentIdx = int((node - 1) / 2)
        else:
            # This is a right child
            parentIdx = int((node - 2) / 2)
        # current node height = 1 + parentHeight
        if heights[parentIdx] == 0:
            # If parent height has not been set, then compute the parents height and then add 1
            heights[node] = 1 + self.computeNodeDepth(parentIdx, heights)
        else:
            # the parent's height has already been calculated so just add 1
            heights[node] = 1 + heights[parentIdx]
        return heights[node]

    def computeTreeHeight(self):
        """
            Returns the height of the tree (the largest number of steps required starting at the
            root to reach a node that actually contains data).
        """
        # array to keep track of the height of each node
        heights = [0 for i in range(len(self.bst))]
        # compute the height for each node in the bst that actually has data in it
        for node in range(len(self.bst)):
            if self.bst[node] is not None:
                self.computeNodeDepth(node, heights)
        # find the largest depth
        treeHeight = 0
        for height in heights:
            if height > treeHeight:
                treeHeight = height
        return treeHeight

class BinaryHeap:
    """
        An array implementation of a binary heap of integers. This heap has member functions
        that allow the user to transform it into a max heap.
    """

    def __init__(self):
        self.heap = []
        self.size = 0

    def insert(self, value):
        """
            Inserts data into the heap
        """
        assert type(value) == type(1), "Error: can only insert integers into heap"
        self.heap.append(value)
        self.size += 1

    def maxHeapify(self, idx):
        """
            Turns the binary heap starting at the current idx and below into a max-heap
        """
        leftIdx = 2 * idx + 1
        rightIdx = 2 * idx + 2
        if leftIdx <= (self.size - 1) and self.heap[leftIdx] > self.heap[idx]:
            largest = leftIdx
        else:
            largest = idx
        if rightIdx <= (self.size - 1) and self.heap[rightIdx] > self.heap[largest]:
            largest = rightIdx
        if largest != idx:
            tmp = self.heap[idx]
            self.heap[idx] = self.heap[largest]
            self.heap[largest] = tmp
            self.maxHeapify(largest)

    def buildMaxHeap(self):
        """
            Turns the entire heap into a max heap
        """
        self.size = len(self.heap)
        idx = math.floor((self.size - 2) / 2)
        # NOTE: might need to go down to -1
        for i in range(idx, -1, -1):
            self.maxHeapify(i)

    def confirmMaxHeap(self, idx):
        """
            Tests to make sure each child of the node at the current idx obeys the max heap
            property. Call w/ idx = 0 to confirm the entire heap is a max heap
        """
        leftIdx = 2 * idx + 1
        rightIdx = 2 * idx + 2
        if leftIdx <= (self.size - 1):
            if self.heap[leftIdx] > self.heap[idx]:
                # Error: max heap propery violation!!!!
                return False
            self.confirmMaxHeap(leftIdx)
        if rightIdx <= (self.size - 1):
            if self.heap[rightIdx] > self.heap[idx]:
                # Error: max heap propery violation!!!!
                return False
            self.confirmMaxHeap(rightIdx)
        if idx == 0:
            # Congratulations, we've iterated through the tree and it is a max heap!
            return True

if __name__ == "__main__":
    """
        Driver code that loads in the given data (supplied by Dr. Harrison), and...
            - creates binary search trees for each data set
            - finds the maximum and minimum for each tree
            - finds the height for each tree
            - finds how much space is wasted for each tree
            - prints out all of this info to stdout
            - prints out the inorder, preorder, and postorder traversals for each tree
            - creates a heap for each data set
            - turns each heap into a max heap
            - tests to make sure each heap is in fact a max heap
            - prints out these freshly made max heaps to stdout

        Arguments:
            - data_path = full path of directory containing data to test the code with
    """
    parser = argparse.ArgumentParser(description="Create and test array based implementations of" +
                                     " a binary search tree and a max heap")
    parser.add_argument("--data_path",
                        help="Full path to directory containing data to be used for testing. " +
                        "Assumes this directory contains nothing but the csv files " +
                        "containing the data to test with.",
                        required=True)
    args = parser.parse_args()
    data_path = args.data_path
    # Load in data from csv files
    data = {}
    try:
        for (root, dirs, files) in os.walk(data_path, topdown=True):
            for f in files:
                data[f] = []
                with open(os.path.join(root, f)) as csvfile:
                    csv_reader = csv.reader(csvfile)
                    for row in csv_reader:
                        data[f].append(ast.literal_eval(row[0]))
    except (IOError, ValueError) as err:
         print("Error: " + str(err))
         sys.exit()

    # Create binary search trees for each data set
    trees = {}
    for dataset in data.keys():
        trees[dataset] = BinarySearchTree()
        # Insert each element of data, starting at root node
        for node in data[dataset]:
            trees[dataset].insert(0, node)

    # Print Tree Info
    print("\n")
    for tree in trees.keys():
        print("{}:".format(tree))
        theMax = trees[tree].max(0)
        if theMax != 128:
            print("\tERROR: Reported max: {} but expected 128".format(theMax))
        theMin = trees[tree].min(0)
        if theMin != 0:
            print("\tERROR: Reported min: {} but expected 0".format(theMin))
        height = trees[tree].computeTreeHeight()
        print("\tMax: {} Min: {} Height: {}".format(theMax, theMin, height))
        print("\n\tInorder Traversal:")
        trees[tree].showInOrder(0)
        print("\n\tPreorder Traversal:")
        trees[tree].showPreOrder(0)
        print("\n\tPostorder Traversal:")
        trees[tree].showPostOrder(0)
        print("\n\tWasted memory:")
        trees[tree].calculateWastedSpace()
        print("\n")

    # Creat Heaps
    heaps = {}
    for filename in data.keys():
        # Create heap for each file
        heaps[filename] = BinaryHeap()
        for node in data[filename]:
            # Insert each node into heap
            heaps[filename].insert(node)

    # Make each heap a max heap and confirm it's correct
    for heap in heaps.values():
        heap.buildMaxHeap()
        heap.confirmMaxHeap(0)

    # Print Heap Info
    print("Heaps:\n")
    for heapName, heap in heaps.items():
        print("{}:".format(heapName))
        heapstring = ""
        for node in heap.heap:
            heapstring += "{}, ".format(node)
        print("\t{}\n".format(heapstring[:-2]))
