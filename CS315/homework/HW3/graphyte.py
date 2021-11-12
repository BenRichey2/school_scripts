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

class UndirectedEdge:

    def __init__(self, weight=None, vertex1=None, vertex2=None):
        self.weight = weight 
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def __str__(self):
        return str(self.weight) + self.vertex1 + self.vertex2

class Vertex:

    def __init__(self, name=None, distance=None, predecessor=None, color=None):
        self.name = name
        self.distance = distance
        self.predecessor = predecessor
        self.color = color

    def __str__(self):
        return self.name

class Graphyte:

    def __init__(self, vertices=[], edges=[]):
        self.graph = {}
        for vertex in vertices:
            assert type(vertex) == type(Vertex()), "Error: vertex must be type Vertex"
            self.graph[vertex] 
        for edge in edges:
            assert type(edge) == type(UndirectedEdge()), "Error: edge must be type UndirectedEdge"
            assert edge.vertex1 in self.graph.keys(), "Error: edge vertex 1 does not exist"
            assert edge.vertex2 in self.graph.keys(), "Error: edge vertex 2 does not exist"
            assert edge not in self.graph[edge.vertex1], "Error: cannot insert an already existing edge"
            assert edge not in self.graph[edge.vertex2], "Error: cannot insert an already existing edge"
            self.graph[edge.vertex1].append(edge)
            self.graph[edge.vertex2].append(edge)

    def insertVertex(self, vertex=None):
        assert vertex not in self.graph, "Error: cannot add already existing vertex to graph"
        assert type(vertex) = type(Vertex()), "Error: Must insert vertices of type Vertex"
        self.graph[vertex] = []

    def insertEdge(self, edge=None):
        assert type(edge) == type(UndirectedEdge()), "Error: Must insert edges of type UndirectedEdge"
        assert edge.vertex1 in self.graph.keys(), "Error: edge vertex 1 does not exist"
        assert edge.vertex2 in self.graph.keys(), "Error: edge vertex 2 does not exist"
        assert edge not in self.graph[edge.vertex1], "Error: cannot insert an already existing edge"
        assert edge not in self.graph[edge.vertex2], "Error: cannot insert an already existing edge"
        self.graph[edge.vertex1].append(edge)
        self.graph[edge.vertex2].append(edge)

    def __str__(self):
        graph_string = ""
        for vertex in self.graph.keys():
            edgeString = ""
            for edge in self.graph[vertex]:
                edgeString += edge + ", "
            edgeString = edgeString[:len(edgeString - 1)]
            graph_string += vertex + " -> " + edgeString + "\n"
        return graph_string

