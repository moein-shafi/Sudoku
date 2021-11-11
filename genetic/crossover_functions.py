import numpy
import random
from .candidate import Candidate
from genetic.constants import *
from past.builtins import range


def crossover(parent1, parent2):
    child1 = Candidate()
    child2 = Candidate()
    child1.values = numpy.copy(parent1.values)
    child2.values = numpy.copy(parent2.values)

    rand = random.uniform(0, 1.1)
    while (rand > 1):
        rand = random.uniform(0, 1.1)

    if (rand < crossover_rate):
        # Pick a crossover point. Crossover must have at least 1 row (and at most Nd-1) rows.
        crossover_point1 = random.randint(0, 8)
        crossover_point2 = crossover_point1
        while(crossover_point1 >= crossover_point2):
            crossover_point2 = random.randint(1, 9)
            
        for i in range(crossover_point1, crossover_point2):
            crossover_rows(child1, child2, i)

    return child1, child2


def crossover_rows(child1, child2, selected):
    child_row1 = numpy.zeros(Nd)
    child_row2 = numpy.zeros(Nd)

    remaining = range(1, Nd + 1)
    cycle = 0
    
    while ((0 in child_row1) and (0 in child_row2)):
        index = find_unused(child1.values[selected], remaining)
        start = child1.values[selected][index]
        remaining.remove(child1.values[selected][index])

        if(cycle % 2 == 0):
            child_row1[index] = child1.values[selected][index]
            child_row2[index] = child2.values[selected][index]
            next_cand = child2.values[selected][index]
            
            while(next_cand != start):
                index = find_value(child1.values[selected], next_cand)
                child_row1[index] = child1.values[selected][index]
                remaining.remove(child1.values[selected][index])
                child_row2[index] = child2.values[selected][index]
                next_cand = child2.values[selected][index]

            cycle += 1

        else:
            child_row1[index] = child2.values[selected][index]
            child_row2[index] = child1.values[selected][index]
            next_cand = child2.values[selected][index]
            
            while(next_cand != start):
                index = find_value(child1.values[selected], next_cand)
                child_row1[index] = child2.values[selected][index]
                remaining.remove(child1.values[selected][index])
                child_row2[index] = child1.values[selected][index]
                next_cand = child2.values[selected][index]
                
            cycle += 1
    
    child1.values[selected] = child_row1
    child2.values[selected] = child_row2


def find_unused(parent_row, remaining):
    for i in range(0, len(parent_row)):
        if(parent_row[i] in remaining):
            return i


def find_value(parent_row, value):
    for i in range(0, len(parent_row)):
        if(parent_row[i] == value):
            return i
