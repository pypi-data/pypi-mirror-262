import random

from vizing.pythonconstraint import _CP_model_
#from vizing.ortools import _or_CP_model_

def list_colouring(graph, list_assignment, model = 'CP'):

    r"""
    This function returns a list-colouring of a list-colourable graph.

    INPUT:

    - ``graph`` -- A ``networkx`` graph.
    - ``list_assignment`` -- A mapping from nodes of ``graph`` to lists of colours.
    - ``model`` -- Choices are 'CP' for constraint programming via 
      ``python-constraint`` or ``or`` for constraint programming via Google 
      ``or-tools``.

    OUTPUT:

    ``dictionary`` -- the list colouring

    EXAMPLES:

    >>> import networkx
    >>> G = networkx.complete_graph(10)
    >>> L = dict([(node, range(10)) for node in G.nodes()])
    >>> from vizing.models import list_colouring
    >>> list_colouring(G, L, model = 'CP')
    {0: [9], 1: [8], 2: [7], 3: [6], 4: [5], 5: [4], 6: [3], 7: [2], 8: [1], 9: [0]}
    """

    if model == 'CP':
        return _CP_model_(graph, list_assignment).first_solution()
    else:
        raise Exception('No such model')

####################################################################
# Vertex coloring algorithms
####################################################################

def neighboring_colors(graph, node):
    """Returns list of colors used on neighbors of 'node' in 'graph'."""
    return [_f for _f in [graph.node[neighbor].get('color') for neighbor in graph.neighbors(node)] if _f]

def n_colors(graph):
    """The number of distinct colors used on vertices of 'graph'."""
    return len(set([graph.node[i]['color'] for i in graph.nodes()]))

def least_missing(colors):
    """The smallest integer not in 'colors'."""
    colors.sort()
    for color in colors:
        if color + 1 not in colors:
            return color + 1

def first_available_color(graph, node):
    """The first color not used on neighbors of 'node' in 'graph'."""
    used_colors = neighboring_colors(graph, node)
    if len(used_colors) == 0:
        return 1
    else:
        return least_missing(used_colors)

def random_available_color(graph, node):
    """A random colour from the list of a node."""
    list = graph.node[node]['list'][:]
    for color in neighboring_colors(graph, node):
        if color in list:
            list.remove(color)
    return random.choice(list)

def saturation_degree(graph, node):
    """Saturation degree of 'node' in 'graph'."""
    return len(set(neighboring_colors(graph, node)))

class FirstAvailableColor():
    """First available color choice visitor."""

    def __call__(self, graph, node):
        return first_available_color(graph, node)

class RandomAvailableColor():
    """Random color choice visitor."""

    def __call__(self, graph, node):
        return random_available_color(graph, node)

class InOrder():
    """Natural vertex ordering strategy."""

    def __init__(self, graph):
        self.graph = graph

    def __iter__(self):
        return self.graph.nodes_iter()

class RandomOrder():
    """Random vertex ordering strategy."""

    def __init__(self, graph):
        self.graph = graph
        self.nodes = self.graph.nodes()

    def __iter__(self):
        random.shuffle(self.nodes)
        return iter(self.nodes)

class DSATOrder():
    """Saturation degree vertex ordering strategy."""

    def __init__(self, graph):
        self.graph = graph
        self.nodes = self.graph.nodes()
        self.value = 0

    def dsatur(self, node):
        return saturation_degree(self.graph, node)

    def __next__(self):
        self.value += 1
        if self.value > self.graph.order(): raise StopIteration
        self.nodes.sort(key = self.dsatur)
        return self.nodes.pop()

    def __iter__(self):
        return self

def vertex_coloring(graph, nodes = InOrder, choose_color = FirstAvailableColor):
    """Generic vertex coloring algorithm. Node ordering specified by 'nodes'
    iterator. Color choice strategy specified by 'choose_color'."""
    nodes = nodes(graph)
    for node in nodes:
        if not graph.node[node].get('color'):
            graph.node[node]['color'] = choose_color()(graph, node)
    return graph

