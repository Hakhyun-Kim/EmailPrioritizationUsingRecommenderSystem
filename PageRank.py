# Copyright (c) 2010 Pedro Matiello <pmatiello@gmail.com>
#                    Juarez Bochi <jbochi@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


"""
PageRank algoritm

@sort: pagerank
"""

# for graph init
#!/usr/bin/env python

# Copyright (c) 2007-2008 Pedro Matiello <pmatiello@gmail.com>
# License: MIT (see COPYING file)

# Import graphviz
import sys
sys.path.append('..')
sys.path.append('/usr/lib/graphviz/python/')
sys.path.append('/usr/lib64/graphviz/python/')

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

# Graph creation
gr = graph()

# Add nodes and edges
gr.add_nodes(["Portugal","Spain","France","Germany","Belgium","Netherlands","Italy"])
gr.add_nodes(["Switzerland","Austria","Denmark","Poland","Czech Republic","Slovakia","Hungary"])
gr.add_nodes(["England","Ireland","Scotland","Wales"])

gr.add_edge(("Portugal", "Spain"))
gr.add_edge(("Spain","France"))
gr.add_edge(("France","Belgium"))
gr.add_edge(("France","Germany"))
gr.add_edge(("France","Italy"))
gr.add_edge(("Belgium","Netherlands"))
gr.add_edge(("Germany","Belgium"))
gr.add_edge(("Germany","Netherlands"))
gr.add_edge(("England","Wales"))
gr.add_edge(("England","Scotland"))
gr.add_edge(("Scotland","Wales"))
gr.add_edge(("Switzerland","Austria"))
gr.add_edge(("Switzerland","Germany"))
gr.add_edge(("Switzerland","France"))
gr.add_edge(("Switzerland","Italy"))
gr.add_edge(("Austria","Germany"))
gr.add_edge(("Austria","Italy"))
gr.add_edge(("Austria","Czech Republic"))
gr.add_edge(("Austria","Slovakia"))
gr.add_edge(("Austria","Hungary"))
gr.add_edge(("Denmark","Germany"))
gr.add_edge(("Poland","Czech Republic"))
gr.add_edge(("Poland","Slovakia"))
gr.add_edge(("Poland","Germany"))
gr.add_edge(("Czech Republic","Slovakia"))
gr.add_edge(("Czech Republic","Germany"))
gr.add_edge(("Slovakia","Hungary"))

def pagerank(graph, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
    """
    Compute and return the PageRank in an directed graph.    
    
    @type  graph: digraph
    @param graph: Digraph.
    
    @type  damping_factor: number
    @param damping_factor: PageRank dumping factor.
    
    @type  max_iterations: number 
    @param max_iterations: Maximum number of iterations.
    
    @type  min_delta: number
    @param min_delta: Smallest variation required to have a new iteration.
    
    @rtype:  Dict
    @return: Dict containing all the nodes PageRank.
    """
    
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        graph = gr
        nodes = graph.nodes()
        graph_size = len(nodes)
        # return {}
    min_value = (1.0-damping_factor)/graph_size #value for nodes without inbound links
    
    # itialize the page rank dict with 1/N for all nodes
    pagerank = dict.fromkeys(nodes, 1.0/graph_size)
        
    for i in range(max_iterations):
        diff = 0 #total difference compared to last iteraction
        # computes each node PageRank based on inbound links
        for node in nodes:
            rank = min_value
            for referring_page in graph.incidents(node):
                rank += damping_factor * pagerank[referring_page] / len(graph.neighbors(referring_page))
                
            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank
        
        #stop if PageRank has converged
        if diff < min_delta:
            break
    
    return pagerank