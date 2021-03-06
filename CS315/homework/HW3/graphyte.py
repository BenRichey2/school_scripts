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
import math
import heapq

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

    def __lt__(self, other):
        return self.distance < other.distance

class Graphyte:

    def __init__(self, vertices=[], edges=[]):
        self.graph = {}
        vertexType = type(Vertex(None, None, None, None))
        edgeType = type(UndirectedEdge(None, None, None))
        for vertex in vertices:
            assert type(vertex) == vertexType, "Error: vertex must be type Vertex"
            assert vertex.name not in self.graph.keys(), "Error: no two vertices may have the same name"
            self.graph[vertex.name] = (vertex, [])
        for edge in edges:
            assert type(edge) == edgeType, "Error: edge must be type UndirectedEdge"
            assert edge.vertex1 in self.graph.keys(), "Error: edge vertex 1 does not exist"
            assert edge.vertex2 in self.graph.keys(), "Error: edge vertex 2 does not exist"
            assert edge not in self.graph[edge.vertex1][1], "Error: cannot add edge twice"
            assert edge not in self.graph[edge.vertex2][1], "Error: cannot add edge twice"
            self.graph[edge.vertex1][1].append(edge)
            self.graph[edge.vertex2][1].append(edge)

    def __str__(self):
        graph_string = ""
        for vertex in self.graph.keys():
            edgeString = ""
            for edge in self.graph[vertex][1]:
                if vertex == edge.vertex1:
                    edgeString += "(" + edge.vertex2 + ", " + str(edge.weight) + ")" + ", "
                else:
                    edgeString += "(" + edge.vertex1 + ", " + str(edge.weight) + ")" + ", "
            edgeString = edgeString[:len(edgeString) - 2]
            graph_string += vertex + " -> " + edgeString + "\n"
        return graph_string

    def breadthFirstSearch(self, source_vertex):
        for vertex in self.graph.keys():
            self.graph[vertex][0].color = "WHITE"
            self.graph[vertex][0].distance = math.inf
            self.graph[vertex][0].predecessor = None
        source_vertex.color = "GRAY"
        source_vertex.distance = 0
        source_vertex.predecessor = None
        queue = []
        queue.append(source_vertex)
        while len(queue) > 0:
            current = queue.pop(0)
            for edge in self.graph[current.name][1]:
                adj_vertex = edge.vertex1
                if edge.vertex1 == current.name:
                    adj_vertex = edge.vertex2
                if self.graph[adj_vertex][0].color == "WHITE":
                    self.graph[adj_vertex][0].color = "GRAY"
                    self.graph[adj_vertex][0].distance = current.distance + 1
                    self.graph[adj_vertex][0].predecessor = current
                    queue.append(self.graph[adj_vertex][0])
            current.color = "BLACK"

    def printPath(self, source_vertex, dest_vertex):
        if dest_vertex.name == source_vertex.name:
            print(source_vertex.name)
        elif dest_vertex.predecessor == None:
            print("No path from {} to {}".format(source_vertex.name, dest_vertex.name))
        else:
            self.printPath(source_vertex, dest_vertex.predecessor)
            print(dest_vertex.name)

    def dijkstra(self, source_vertex):
        self.initSingleSource(source_vertex)
        priorityQ = []
        for vertex in self.graph.keys(): priorityQ.append(self.graph[vertex][0])
        heapq.heapify(priorityQ)
        while len(priorityQ) != 0:
            current = heapq.heappop(priorityQ)
            for edge in self.graph[current.name][1]:
                adj_vertex = self.graph[edge.vertex1][0]
                if edge.vertex1 == current.name:
                    adj_vertex = self.graph[edge.vertex2][0]
                self.relax(current, adj_vertex, edge.weight)
                heapq.heapify(priorityQ)

    def relax(self, current, adj_vertex, distance):
        if adj_vertex.distance > (current.distance + distance):
            adj_vertex.distance = current.distance + distance
            adj_vertex.predecessor = current

    def initSingleSource(self, source_vertex):
        for vertex in self.graph.keys():
            self.graph[vertex][0].distance = math.inf
            self.graph[vertex][0].predecessor = None
        source_vertex.distance = 0

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

    # Convert file data to UndirectedEdge and Vertex data types
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
    # Create and print graph
    graph = Graphyte(vertices, edges)
    print(graph)
    # Show weighted and unweighted shortest paths for various cities
    print("Finding shortest unweighted path from Arad to Sibiu")
    graph.breadthFirstSearch(graph.graph["Arad"][0])
    graph.printPath(graph.graph["Arad"][0], graph.graph["Sibiu"][0])
    print("Finding shortest unweighted path from Arad to Craiova")
    graph.printPath(graph.graph["Arad"][0], graph.graph["Craiova"][0])
    print("Finding shortest unweighted path from Arad to Bucharest")
    graph.printPath(graph.graph["Arad"][0], graph.graph["Bucharest"][0])
    print("Finding shortest weighted path from Arad to Bucharest")
    graph.dijkstra(graph.graph["Arad"][0])
    graph.printPath(graph.graph["Arad"][0], graph.graph["Bucharest"][0])
