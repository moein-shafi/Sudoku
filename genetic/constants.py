#!/usr/bin/python3

sudoku_size = 9
population_size = 1000
elite_selection_rate = 0.05
elites_size = int(elite_selection_rate * population_size)
maximum_generation = 1000
mutation_rate = 0.06
crossover_rate = 1.0
selection_rate = 0.85

input_file = "input_sudoku.txt"