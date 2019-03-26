from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model


# You need to subclass the cp_model.CpSolverSolutionCallback class.
class VarArrayAndObjectiveSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        print('Solution %i' % self.__solution_count)
        print('  objective value = %i' % self.ObjectiveValue())
        for v in self.__variables:
            print('  %s = %i' % (v, self.Value(v)), end=' ')
        print()
        self.__solution_count += 1

    def solution_count(self):
        return self.__solution_count


def SolveAndPrintIntermediateSolutionsSampleSat():
    """Showcases printing intermediate solutions found during search."""
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
    num_vals = 500
    varList = []

    for i in range(num_vals):
        varName = "" + str(i)
        varList.append(model.NewIntVar(0, 1, varName))

    # print(varList)

    x = model.NewIntVar(0, num_vals - 1, 'x')
    varList.append(x)
    # print(varList))
    y = model.NewIntVar(0, num_vals - 1, 'y')
    z = model.NewIntVar(0, num_vals - 1, 'z')

    # Creates the constraints.
    model.Add(x != y)

    model.Maximize(x + 2 * y + 3 * z)

    # Creates a solver and solves.
    solver = cp_model.CpSolver()
    # solution_printer = VarArrayAndObjectiveSolutionPrinter([x, y, z])
    # status = solver.SolveWithSolutionCallback(model, solution_printer)

    # print('Status = %s' % solver.StatusName(status))
    # print('Number of solutions found: %i' % solution_printer.solution_count())


SolveAndPrintIntermediateSolutionsSampleSat()