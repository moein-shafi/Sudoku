#!/usr/bin/python3

Nd = 9  # Number of digits (in the case of standard Sudoku puzzles, this is 9).
Nc = 1000  # Number of candidates (i.e. population size).
Ne = int(0.05*Nc)  # Number of elites.
Ng = 1000  # Number of generations.
mutation_rate = 0.06
crossover_rate = 1.0
selection_rate = 0.85
