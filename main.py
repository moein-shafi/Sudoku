#!/usr/bin/python3

import numpy
import random

from genetic.population import Population
from genetic.candidate import Candidate
from genetic.crossover_functions import *
from genetic.constants import *


def read_input():
    with open("input_sudoku.txt", "r") as f:
        values = numpy.loadtxt(f).reshape((Nd, Nd)).astype(int)
        return values


def select_parent(candidates):
    candidate1_index = random.randint(0, len(candidates) - 1)
    candidate2_index = candidate1_index
    while (candidate2_index == candidate1_index):
        candidate2_index = random.randint(0, len(candidates) - 1)

    candidate1 = candidates[candidate1_index]
    candidate2 = candidates[candidate2_index]

    rand = random.uniform(0, 1.1)
    while (rand > 1):  # Outside [0, 1] boundary. Choose another.
        rand = random.uniform(0, 1.1)

    fittest = candidate1 if candidate1.fitness > candidate2.fitness else candidate2
    weakest = candidate2 if candidate1.fitness > candidate2.fitness else candidate1

    return fittest if rand < selection_rate else weakest


def check_ultimate_state(population):
    for c in range(0, Nc):
        fitness = population.candidates[c].fitness
        if(fitness == 1):
            print(population.candidates[c].values)
            return True

    return False


def mutate_child(given, mutation_rate, child):
    child.mutate(mutation_rate, given)
    child.update_fitness()


def add_elites(population, next_population):
    for e in range(0, Ne):
        elite = Candidate()
        elite.values = numpy.copy(population.candidates[e].values)
        next_population.append(elite)


def create_new_population(given, population):
    next_population = []
    population.sort()

    for count in range(Ne, Nc, 2):
        parent1 = select_parent(population.candidates)
        parent2 = select_parent(population.candidates)
        child1, child2 = crossover(parent1, parent2)
        mutate_child(given, mutation_rate, child1)
        mutate_child(given, mutation_rate, child2)
        
        next_population.append(child1)
        next_population.append(child2)

    add_elites(population, next_population)
    return next_population


def solve(given):
    random.seed()
    population = Population()
    population.seed(given)
    for generation in range(0, Ng):
        print("Generation number: ", generation)
        if check_ultimate_state(population):
            return True
        population.candidates = create_new_population(given, population)
        population.update_fitness()
        
    print("No solution found.")
    return False


def main():
    values = read_input()
    given = Candidate(values)
    solve(given)


if __name__ == '__main__':
    main()

### TODO list:
#   change names
#   change prints
#   change functions' names
