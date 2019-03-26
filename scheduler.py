
import csv
import sys
import random
from student import Student

from __future__ import print_function
from ortools.linear_solver import pywraplp

FIELDS = ['ID', 'CLASS', 'CRN', 'TREE', 'BRANCH', 'COURSE_CEILING',
          'MAJOR', 'MAJOR2', 'SUBJ', 'NUMB', 'SEQ']


def read_file(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=FIELDS)
        student_requests = {}
        students_by_class = {'SENI': set([]), 'JUNI': set([]),
                             'SOPH': set([]), 'FRST': set([]),
                             'OTHER': set([])}
        courses = {}
        next(reader)
        # reader.next() # consume the first line, which is just column headers

        for row in reader:
            id = int(row['ID'])
            class_year = row['CLASS']
            crn = int(row['CRN'])
            tree = int(row['TREE'])
            branch = int(row['BRANCH'])
            if id in student_requests:  # does this student already exist?
                student_requests[id].add_request(crn, tree, branch)
            else:  # nope, create a new record
                s = Student(id, class_year)
                s.add_request(crn, tree, branch)
                student_requests[id] = s

            students_by_class[class_year].add(id)
            courses[crn] = int(row['COURSE_CEILING'])

    return student_requests, students_by_class, courses


def main():
    solver = pywraplp.Solver('SolveIntegerProblem',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # x and y are integer non-negative variables.
    x = solver.IntVar(0.0, solver.infinity(), 'x')
    y = solver.IntVar(0.0, solver.infinity(), 'y')
    num_vals = 500
    varList = []

    for i in range(num_vals):
        varName = "" + str(i)
        varList.append(solver.IntVar(0.0, 1.0, varName))

    print(varList[0])
#   solver.SetCoefficient()

    # x + 7 * y <= 17.5
    constraint1 = solver.Constraint(-solver.infinity(), 17.5)
    constraint1.SetCoefficient(x, 1)
    constraint1.SetCoefficient(y, 7)

    # x <= 3.5
    constraint2 = solver.Constraint(-solver.infinity(), 3.5)
    constraint2.SetCoefficient(x, 1)
    constraint2.SetCoefficient(y, 0)

    # Maximize x + 10 * y.
    objective = solver.Objective()
    objective.SetCoefficient(x, 1)
    objective.SetCoefficient(y, 10)
    for i in range(num_vals):
        name = "" + str(i)
        objective.SetCoefficient(name, 9)

    objective.SetMaximization()

    """Solve the problem and print the solution."""
    result_status = solver.Solve()
    # The problem has an optimal solution.
    assert result_status == pywraplp.Solver.OPTIMAL

    # The solution looks legit (when using solvers other than
    # GLOP_LINEAR_PROGRAMMING, verifying the solution is highly recommended!).
    assert solver.VerifySolution(1e-7, True)

    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())

    # The objective value of the solution.
    print('Optimal objective value = %d' % solver.Objective().Value())
    print()
    # The value of each variable in the solution.
    variable_list = [x, y]

    for variable in variable_list:
        print('%s = %d' % (variable.name(), variable.solution_value()))


if __name__ == '__main__':
    main()
