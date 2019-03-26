
import csv
import sys
import random
from student import Student

FIELDS = ['ID','CLASS','CRN','TREE','BRANCH','COURSE_CEILING',
          'MAJOR','MAJOR2','SUBJ','NUMB','SEQ']

def read_file(filename):
    """Returns data read in from supplied WebTree data file.

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
            if id in student_requests: # does this student already exist?
                student_requests[id].add_request(crn, tree, branch)
            else: # nope, create a new record
                s = Student(id, class_year)
                s.add_request(crn, tree, branch)
                student_requests[id] = s

            students_by_class[class_year].add(id)
            courses[crn] = int(row['COURSE_CEILING'])
            
    return student_requests, students_by_class, courses

def countUniqueCourses(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=FIELDS)
        student_requests = {}
        students_by_class = {'SENI': set([]), 'JUNI': set([]),
                             'SOPH': set([]), 'FRST': set([]),
                             'OTHER': set([])}
        courses = {}
        next(reader)
        # reader.next() # consume the first line, which is just column headers

        counterSet = set()
        count = 0
        for row in reader:
            counterSet.add(int(row['ID']))
            # id = int(row['ID'])
            # class_year = row['CLASS']
            # crn = int(row['CRN'])
            # tree = int(row['TREE'])
            # branch = int(row['BRANCH'])
            # if id in student_requests: # does this student already exist?
            #     student_requests[id].add_request(crn, tree, branch)
            # else: # nope, create a new record
            #     s = Student(id, class_year)
            #     s.add_request(crn, tree, branch)
            #     student_requests[id] = s

            # students_by_class[class_year].add(id)
            # courses[crn] = int(row['COURSE_CEILING'])
            
    return len(counterSet)
    # student_requests, students_by_class, courses

def main():
    # if (len(sys.argv) != 2):
    #     print()
    #     print("***********************************************************")
    #     print("You need to supply a .csv file containing the WebTree data")
    #     print("as a command-line argument.")
    #     print()
    #     print("Example:")
    #     print("    python baseline_webtree.py spring-2015.csv")
    #     print("***********************************************************")
    #     print()
    #     return
    
    # Read in data
    # student_requests, students_by_class, courses = read_file(sys.argv[1])

    # Assign random numbers
    # random_ordering = assign_random_numbers(students_by_class)

    # Run webtree
    # assignments = run_webtree(student_requests, students_by_class,
                            #   courses, random_ordering)

    # Print results to stdout
    # for id in assignments:
    #     print(id),
    #     for course in assignments[id]:
    #         print(course),
    #     print()
    num = countUniqueCourses("spring-2015.csv")
    print(num)

        
if __name__ == "__main__":
    main()
