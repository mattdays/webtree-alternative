from __future__ import print_function

import csv
import sys
import random
from student import Student

from ortools.linear_solver import pywraplp

FIELDS = ['ID', 'CLASS', 'CRN', 'TREE', 'BRANCH', 'COURSE_CEILING',
          'MAJOR', 'MAJOR2', 'SUBJ', 'NUMB', 'SEQ']

CLASS_MULTIPLIERS = {'SENI': 2.00, 'JUNI': 1.75,
                     'SOPH': 1.50, 'FRST': 1.25, 'OTHER': 1.0}


def read_file(filename):
	"""Returns formatted data read in from supplied WebTree data file.

    Parameters:
        filename - string containing the name of the CSV file.

    Returns:
        a) A dictionary mapping student IDs to records, where each record
           contains information about that student's WebTree requests.
        b) A dictionary mapping class years to student IDs, indicating
           which students are seniors, juniors, etc.
        c) A dictionary mapping course CRNs to enrollment capacities.
    """
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames=FIELDS)
		student_requests = {}
		students_by_class = {}
		courses = {}
		next(reader)
		
		for row in reader:
			id = int(row['ID'])
			class_year = row['CLASS']
			crn = int(row['CRN'])
			tree = int(row['TREE'])
			branch = int(row['BRANCH'])
			if id in student_requests:  # does this student already exist?
				temp_tup = (crn, tree, branch)
				student_requests.get(id).append(temp_tup)
			else:  # nope, create a new record
				student_requests[id] = []
				temp_tup = (crn, tree, branch)
				student_requests.get(id).append(temp_tup)
				students_by_class[id] = class_year
				
			courses[crn] = int(row['COURSE_CEILING'])
		return student_requests, students_by_class, courses


def class_preference(tree, branch):
    weight = 0
    diversions = 0

    if (branch < 4):
        weight = branch * tree
    else:
        weight = 21 + branch
    # conversions to diversions
    if ((weight == 25) or (weight == 24) or (weight == 22)):
        diversions += 7
    elif((weight == 23) or (weight == 21) or (weight == 20) or (weight == 18) or (weight == 17) or (weight == 15) or (weight == 4)):
        diversions += 6
    elif((weight == 19) or (weight == 16) or (weight == 14) or (weight == 13) or (weight == 11) or (weight == 10) or (weight == 8)):
        diversions += 5
    elif((weight == 12) or (weight == 9) or (weight == 7) or (weight == 6)):
        diversions += 4
    elif((weight == 5) or (weight == 3)):
        diversions += 3
    elif(weight == 2):
        diversions += 2
    elif(weight == 1):
        diversions += 1

    return diversions


def main():
    # Read in csv file data
    read_file_name = sys.argv[1]
    student_requests, students_by_class, courses = read_file(read_file_name)

    write_file_name = read_file_name.replace(".csv", "-output.csv")

    # Declare assignment & cost/point matrix
    class_assign = {}
    class_weight = [[0 for x in range(len(courses.keys()))]
                    for y in range(len(student_requests))]

    solver = pywraplp.Solver('SolveAssignmentProblemMIP',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    course_list = list(courses.keys())

    for i in range(len(student_requests)):
        sr_list = student_requests.get(i+1)
        class_year = students_by_class.get(i+1)

        for j in range(len(course_list)):
            for k in range(len(sr_list)):
                temp = class_preference(sr_list[k][1], sr_list[k][2])
                temp_class = CLASS_MULTIPLIERS[class_year]

                # class_weight[i][course_list.index(sr_list[k][0])] = temp
                class_weight[i][course_list.index(
                    sr_list[k][0])] = temp_class * temp
            class_assign[i, j] = solver.BoolVar('class_assign[%i,%i]' % (i, j))

    # Objective
    solver.Maximize(solver.Sum([class_weight[i][j] * class_assign[i, j] for i in range(len(student_requests))
                                for j in range(len(course_list))]))

    # Constraints

    # Each worker is assigned to at most 1 task.

    for i in range(len(student_requests)):
        solver.Add(solver.Sum([class_assign[i, j]
                               for j in range(len(course_list))]) <= 4)

    # Each task is assigned to exactly one worker.

    for j in range(len(course_list)):
        solver.Add(solver.Sum([class_assign[i, j] for i in range(
            len(student_requests))]) <= courses[course_list[j]])

    sol = solver.Solve()

    with open(write_file_name, 'w', newline='') as f:
        output = csv.writer(f)
        output.writerow(['Total score =', str(solver.Objective().Value())])

        output_nested_list = []

        for i in range(len(student_requests)):
            temp_output_list = []
            temp_output_list.append(str(i + 1))
            for j in range(len(course_list)):
                if class_assign[i, j].solution_value() > 0:
                    temp_output_list.append(str(course_list[j]))
            output_nested_list.append(temp_output_list)
            output.writerow(temp_output_list)
        output.writerow(["Time = ", solver.WallTime(), " milliseconds"])


if __name__ == '__main__':
    main()
