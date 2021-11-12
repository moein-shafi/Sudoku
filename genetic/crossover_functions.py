import numpy
import random

from past.builtins import range

from .candidate import Candidate
from .constants import *


def crossover(first_child, second_child):
    if (random.uniform(0, 1) < crossover_rate):
        crossover_point1 = random.randint(0, 8)
        crossover_point2 = crossover_point1
        while(crossover_point1 >= crossover_point2):
            crossover_point2 = random.randint(1, 9)

        for i in range(crossover_point1, crossover_point2):
            crossover_rows(first_child, second_child, i)


def find_unused(parent_row, remaining):
    for i in range(0, len(parent_row)):
        if(parent_row[i] in remaining):
            return i


def find_value(parent_row, value):
    for i in range(0, len(parent_row)):
        if(parent_row[i] == value):
            return i


def do_row_crossover(start, index, selected, first_child_row, second_child_row, first_child, second_child, remaining):
    first_child_row[index] = first_child.values[selected][index]
    second_child_row[index] = second_child.values[selected][index]
    next_cand = second_child.values[selected][index]

    while(next_cand != start):
        index = find_value(first_child.values[selected], next_cand)
        first_child_row[index] = first_child.values[selected][index]
        remaining.remove(first_child.values[selected][index])
        second_child_row[index] = second_child.values[selected][index]
        next_cand = second_child.values[selected][index]


def crossover_rows(first_child, second_child, selected):
    first_child_row = numpy.zeros(sudoku_size)
    second_child_row = numpy.zeros(sudoku_size)

    remaining = range(1, sudoku_size + 1)
    first_round = True
    index = 0

    while ((0 in first_child_row) and (0 in second_child_row)):
        index = find_unused(first_child.values[selected], remaining)
        start = first_child.values[selected][index]
        remaining.remove(first_child.values[selected][index])
        if(first_round):
            do_row_crossover(start, index, selected, first_child_row, second_child_row, first_child, second_child, remaining)
        else:
            do_row_crossover(start, index, selected, second_child_row, first_child_row, first_child, second_child, remaining)
        first_round = not first_round

    first_child.values[selected] = first_child_row
    second_child.values[selected] = second_child_row
