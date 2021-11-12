#!/usr/bin/python3

import numpy
import random

from genetic.population import Population
from genetic.chromosome import Chromosome
from genetic.crossover_functions import *
from genetic.constants import *


def read_input():
    with open(input_file, "r") as f:
        input_sudoku = numpy.loadtxt(f).reshape((sudoku_size, sudoku_size)).astype(int)
        return input_sudoku


def select_parent(chromosomes):
    chromosome1 = chromosomes[random.randint(0, len(chromosomes) - 1)]
    chromosome2 = chromosome1
    while (chromosome1 == chromosome2):
        chromosome2 = chromosomes[random.randint(0, len(chromosomes) - 1)]

    rand = random.uniform(0, 1)
    fittest = chromosome1 if chromosome1.fitness > chromosome2.fitness else chromosome2
    weakest = chromosome2 if chromosome1.fitness < chromosome2.fitness else chromosome1
    return fittest if rand < selection_rate else weakest


def check_ultimate_state(population):
    for chromosome in population.chromosomes:
        if(chromosome.fitness == 1):
            print(chromosome.values)
            return True

    return False


def mutate_child(input_sudoku, mutation_rate, child):
    if (random.uniform(0, 1) < mutation_rate):
        child.mutate(mutation_rate, input_sudoku)
    child.update_fitness()


def add_elites(population, new_population):
    for i in range(0, elites_size):
        elite = Chromosome()
        elite.values = numpy.copy(population.chromosomes[i].values)
        new_population.append(elite)


def create_childs_from_parents(first_parent, second_parent):
    first_child = Chromosome()
    second_child = Chromosome()
    first_child.values = numpy.copy(first_parent.values)
    second_child.values = numpy.copy(second_parent.values)
    return first_child, second_child


def create_new_population(input_sudoku, population):
    new_population = []
    population.sort()

    for _ in range(0, int(population_size / 2)):
        first_parent = select_parent(population.chromosomes)
        second_parent = first_parent
        while (first_parent == second_parent):
            second_parent = select_parent(population.chromosomes)

        first_child, second_child = create_childs_from_parents(first_parent, second_parent)
        crossover(first_child, second_child)
        mutate_child(input_sudoku, mutation_rate, first_child)
        new_population.append(first_child)
        mutate_child(input_sudoku, mutation_rate, second_child)
        new_population.append(second_child)

    add_elites(population, new_population)
    return new_population


def solve(input_sudoku):
    random.seed()
    population = Population()
    population.create_first_population(input_sudoku)
    print("> Populdation created.")
    for generation in range(0, maximum_generation):
        print("> Generation number:", generation)
        if check_ultimate_state(population):
            return True
        population.chromosomes = create_new_population(input_sudoku, population)
        population.update_fitness()

    print("Oops! Can't find the solution :(")
    return False


def main():
    input_sudoku_array  = read_input()
    input_sudoku = Chromosome(input_sudoku_array)
    solve(input_sudoku)


if __name__ == '__main__':
    main()
