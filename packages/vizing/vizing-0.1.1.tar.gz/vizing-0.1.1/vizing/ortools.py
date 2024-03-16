from constraint_solver import pywrapcp

from vizing.utils import vtc_to_ctv

class _or_CP_model_:

    """ 
    Constraint model via Google or-tools.

    REFERENCES:

    [orto] http://code.google.com/p/or-tools/
    """

    def __init__(self, graph, list_assignment):

        """
        XXX doc XXX
        """

        self.graph = graph
        self.list_assignment = list_assignment
        self.solver = pywrapcp.Solver('xxxNAMExxx')
        self.var = {}
        self.solution = {}
        for node in self.graph.nodes():
            self.var[node] = self.solver.IntVar(self.list_assignment.get(node))
        for edge in self.graph.edges():
            self.solver.Add(self.solver.AllDifferent([self.var[node] for node in edge], False))

    def first_solution(self):

        """ 
        XXX doc XXX 
        """
    
        var_list = list(self.var.values())
        vars_phase = self.solver.Phase(var_list,
                                       self.solver.INT_VAR_SIMPLE, 
                                       self.solver.INT_VALUE_SIMPLE)
        solution = self.solver.Assignment()
        solution.Add(var_list)
        collector = self.solver.FirstSolutionCollector(solution)
        self.solver.Solve(vars_phase, [collector])
        current = collector.solution(0)
        if collector.solution_count() == 1:
            for var in self.var:  
                self.solution[var] = current.Value(self.var[var])
        return vtc_to_ctv(self.solution)
