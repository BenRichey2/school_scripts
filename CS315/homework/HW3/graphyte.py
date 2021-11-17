"""
    Graphyte
    by Ben Richey

    This script contains implementations of a(n) (un)weighted graph using an adjacency list.
    It implements other data structures necessary for this graph representation (such as
    graph edges), graph-related algorithms such as breadth-first search and Dijkstra's.

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

import sys
import os
import csv
import argparse

import ipdb

class UndirectedEdge:

    def __init__(self, weight, vertex1, vertex2):
        self.weight = weight 
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def __eq__(self, other):
        weights = self.weight == other.weight
        v1 = self.vertex1 == other.vertex1
        v2 = self.vertex2 == other.vertex2
        return weights and v1 and v2

class Vertex:

    def __init__(self, name, distance, predecessor, color):
        self.name = name
        self.distance = distance
        self.predecessor = predecessor
        self.color = color

class Graphyte:

    def __init__(self, vertices=[], edges=[]):
        self.graph = {}
        for vertex in vertices:
            assert type(vertex) == type(Vertex(None, None, None, None)), "Error: vertex must be type Vertex"
            assert vertex.name not in self.graph.keys(), "Error: no two vertices may have the same name"
            self.graph[vertex.name] = (vertex, [])
        for edge in edges:
            assert type(edge) == type(UndirectedEdge(None, None, None)), "Error: edge must be type UndirectedEdge"
            assert edge.vertex1 in self.graph.keys(), "Error: edge vertex 1 does not exist"
            assert edge.vertex2 in self.graph.keys(), "Error: edge vertex 2 does not exist"
            assert edge not in self.graph[edge.vertex1][1], "Error: cannot add edge twice"
            assert edge not in self.graph[edge.vertex2][1], "Error: cannot add edge twice"
            self.graph[edge.vertex1][1].append(edge)
            self.graph[edge.vertex2][1].append(edge)

    """
    def insertVertex(self, vertex):
        assert vertex.name not in self.graph.keys(), "Error: cannot add already existing vertex to graph"
        assert type(vertex) == type(Vertex(None, None, None, None)), "Error: Must insert vertices of type Vertex"
        self.graph[vertex.name] =  (vertex, [])

    def insertEdge(self, edge):
        assert type(edge) == type(UndirectedEdge(None, None, None)), "Error: Must insert edges of type UndirectedEdge"
        assert edge.vertex1 in self.graph.keys(), "Error: edge vertex 1 does not exist"
        assert edge.vertex2 in self.graph.keys(), "Error: edge vertex 2 does not exist"
        assert edge not in self.graph[edge.vertex1], "Error: cannot insert an already existing edge"
        assert edge not in self.graph[edge.vertex2], "Error: cannot insert an already existing edge"
        self.graph[edge.vertex1].append(edge)
        self.graph[edge.vertex2].append(edge)
        """

    def __str__(self):
        graph_string = ""
        for vertex in self.graph.keys():
            edgeString = ""
            for edge in self.graph[vertex][1]:
                edgeString += "(" + edge.vertex1 + ", " + edge.vertex2 + ", " + str(edge.weight) + ")" + ", "
            edgeString = edgeString[:len(edgeString) - 2]
            graph_string += vertex + " -> " + edgeString + "\n"
        return graph_string

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=("Graphyte is an adjacency list based "
                                    + "implementation of a graph with undirected edges."
                                    + "It reads in test data (designed for the cities in Romania)"
                                    + ", and prints out the graph to stdout"))
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
                        data[f].append(row)
    except (IOError, ValueError) as err:
         print("Error: " + str(err))
         sys.exit()

    edges = []
    vertices = []
    for f in data.keys():
        if f == "RomaniaEdges.txt":
            for edge in data[f]:
                new_edge = UndirectedEdge(int(edge[2]), edge[1], edge[0])
                edges.append(new_edge)
        elif f == "RomaniaVertices.txt":
            for vertex in data[f]:
                new_vertex = Vertex(vertex[0], None, None, None)
                vertices.append(new_vertex)
        else:
            print("Error: unexpected file found in data path: {}".format(f))
            sys.exit()
    graph = Graphyte(vertices, edges)
    print(graph)
