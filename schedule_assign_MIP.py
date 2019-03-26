from __future__ import print_function

import csv
import sys
import random
from student import Student

# from __future__ import print_function
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
                # student_requests[id].add_request(crn, tree, branch)
                temp_tup = (crn, tree, branch)
                student_requests.get(id).append(temp_tup)
            else:  # nope, create a new record
                # s = Student(id, class_year)
                # s.add_request(crn, tree, branch)
                student_requests[id] = []
                temp_tup = (crn, tree, branch)
                student_requests.get(id).append(temp_tup)

            students_by_class[class_year].add(id)
            courses[crn] = int(row['COURSE_CEILING'])

    return student_requests, students_by_class, courses

# def populate_matrices(student_requests, courses):
#   class_assign = {}
#   class_weight = [[0 for x in range(len(courses.keys()))] for y in range(len(student_requests))] 
#   return 0

def class_preference(tree, branch):
  weight = 0
  if (branch < 4):
    weight = branch * tree
  else:
    weight = 21 + branch
  return 26 - weight

def main():
  # Read in csv file data
  student_requests, students_by_class, courses = read_file(sys.argv[1])

  # Declare assignment & cost/point matrix
  class_assign = {}
  class_weight = [[0 for x in range(len(courses.keys()))] for y in range(len(student_requests))] 

  # # Populate class weight matrix
  # for i in range(len(student_requests)):
  #   for j in 

  solver = pywraplp.Solver('SolveAssignmentProblemMIP',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

  # cost = [[90, 76, 75, 70],
  #         [35, 85, 55, 65],
  #         [125, 95, 90, 105],
  #         [45, 110, 95, 115],
  #         [60, 105, 80, 75],
  #         [45, 65, 110, 95]]

  # team1 = [0, 2, 4]
  # team2 = [1, 3, 5]
  # team_max = 2

  # num_workers = len(cost)
  # num_tasks = len(cost[1])
  # x = {}

  course_list = list(courses.keys())

  # print(student_requests)

  for i in range(len(student_requests)):
    sr_list = student_requests.get(i+1)

    for j in range(len(course_list)):
      for k in range(len(sr_list)):
        temp = class_preference(sr_list[k][1], sr_list[k][2])
        class_weight[i][course_list.index(sr_list[k][0])] = temp
        # print("Here")
      class_assign[i, j] = solver.BoolVar('class_assign[%i,%i]' % (i, j))

  # Objective
  solver.Minimize(solver.Sum([class_weight[i][j] * class_assign[i,j] for i in range(len(student_requests))
                                                  for j in range(len(course_list))]))

  # Constraints

  # Each worker is assigned to at most 1 task.

  for i in range(len(student_requests)):
    solver.Add(solver.Sum([class_assign[i, j] for j in range(len(course_list))]) == 4)

  # Each task is assigned to exactly one worker.

  for j in range(len(course_list)):
    solver.Add(solver.Sum([class_assign[i, j] for i in range(len(student_requests))]) == courses[course_list[i]])

  # Each team takes on two tasks.

  # solver.Add(solver.Sum([x[i, j] for i in team1 for j in range(num_tasks)]) <= team_max)
  # solver.Add(solver.Sum([x[i, j] for i in team2 for j in range(num_tasks)]) <= team_max)
  sol = solver.Solve()

  # print('Total cost = ', solver.Objective().Value())
  # print()
  # for i in range(len(student_requests)):
  #   for j in range(len(course_list)):
  #     if class_assign[i, j].solution_value() > 0:
  #       print('Student %d assigned to task %d.  Cost = %d' % (
  #             i,
  #             j,
  #             cost[i][j]))

  print()
  print("Time = ", solver.WallTime(), " milliseconds")
if __name__ == '__main__':
  main()