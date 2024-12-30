#!/usr/bin/python3

from z3 import *
import argparse
import csv

def read_level(filename):
    # Open the file
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            data = []
            for row in reader:
                # int_row = [int(item) if item is not "" else -1 for item in row]  # Convert each item in the row to an integer
                int_row = [-1 if item.strip() == "" or item == " " or item == "\t" else int(item) for item in row]  # Convert each item in the row to an integer
                data.append(int_row)
            return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(-1)

def handle_args():
    parser = argparse.ArgumentParser(description="Solve a Sudoku puzzle using Z3 solver.")
    parser.add_argument("file", type=str, help="Path to the input file")

    # Parse command-line arguments
    return parser.parse_args()


def add_nonogram_line_single_constraint(solver: Solver, vars, constraint, var_string):
    or_list = []
    constraint_var = Int(var_string)
    for start_index in range(len(vars) - constraint + 1):
        and_list = []
        and_list.append(start_index == constraint_var)
        if start_index != 0:
            and_list.append(Not(vars[start_index - 1]))
        for i in range(constraint):
            and_list.append(vars[start_index + i])
        if (start_index + constraint) != len(vars):
            and_list.append(Not(vars[start_index + constraint]))
        or_list.append(And(and_list))
    solver.add(Or(or_list))
    return constraint_var

def add_kakurasu_line_constraint(solver: Solver, vars, number, size):
    sum_list = []
    for i in range(size):
        sum_list.append(If(vars[i], i + 1, 0))
    solver.add(Sum(sum_list) == number)



def solve_level(level):
    (rows, columns) = (level[0], level[1])
    solver = Solver()
    level_size = len(rows)
    vars = [[Bool(f"var_{i}_{o}") for i in range(level_size)] for o in range(level_size)]

    # add row constraints
    for row_index, number in enumerate(rows):
        add_kakurasu_line_constraint(solver, vars[row_index], number, level_size)

    # add column constraints
    for column_index, number in enumerate(columns):
        column_vars = [row[column_index] for row in vars]
        add_kakurasu_line_constraint(solver, column_vars, number, level_size)


    # Check satisfiability
    if solver.check() == sat:
        model = solver.model()
        return [[model[square] for square in row] for row in vars]  # Return the values of the variables
    else:
        print("No solution exists")
        exit(-1)

def main():
    args = handle_args()

    level = read_level(args.file)
    print("Detected level size: " + str(len(level[0])) + "x" + str(len(level[0])))
        
    row = level[0]
    column = level[1]
    print("\t", end="")
    for number in row:
        print(number, end="\t")
    print()
    for number in column:
        print(number)
    
    solution = solve_level(level)
    for row in solution:
        for square in row:
            print("X" if square else "O", end=" ")
        print()

if __name__ == "__main__":
    main()