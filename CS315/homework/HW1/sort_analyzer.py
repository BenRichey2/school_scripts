"""
    Sorting Algorithm Analyzer
      by Ben Richey

    The following program instantiates the Sortalyzer class which performs a run-time analysis
    on three sorting algorithms: insertion sort, quick sort, and merge sort. This run-time
    analysis is performed by counting the number of comparisons done by each algorithm. The
    class also visualizes this run-time analysis via the matplotlib library.
"""
# std libs
import csv

# 3rd party libs
import matplotlib # Tool to visualize run-time analysis

class Sortalyzer:
    """
        Sortalyzer class performs run-time analysis on insertion sort, quick sort, and merge sort
        algorithms by counting number of comparisons performed. Each of these algorithms will be
        tested against several different data sets in different sorted orders (sorted, reverse
        sorted, and random). Then, a graph will be generated which vizualizes the efficiency of 
        each algorithm for comparison.

        by Ben Richey
    """

    def __init__(self):
        #TODO
        pass

if __name__ == "__main__":
    # instantiate object & perform analysis
    sort_analyzer = Sortalyzer()
