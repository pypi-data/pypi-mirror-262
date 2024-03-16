import constraint

from vizing.utils import vtc_to_ctv

class _CP_model_:

    """ 
    Constraint model via python-constraint.

    REFERENCES: 

    [pyco] http://labix.org/python-constraint
    """

    def __init__(self, graph, list_assignment):
    
        """ 
        XXX doc XXX 
        """

        self.graph = graph
        self.list_assignment = list_assignment
        self.problem = constraint.Problem()
        for node in self.graph.nodes():
            self.problem.addVariable(node, self.list_assignment.get(node)) 
        for edge in self.graph.edges():
            self.problem.addConstraint(constraint.AllDifferentConstraint(), edge)

    def first_solution(self):

        """ 
        XXX doc XXX 
        """

        return vtc_to_ctv(self.problem.getSolution())

