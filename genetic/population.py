import numpy
import random
import operator

from .chromosome import Chromosome
from .constants import *

class Population(object):
    def __init__(self):
        self.candidates = list()
        return


    def sort(self):
        self.candidates.sort()


    def prepare_feasible_values_for_each_cell(self):
        self.feasible_values.values = [[[] for j in range(0, sudoku_size)] for i in range(0, sudoku_size)]
        for row in range(0, sudoku_size):
            for column in range(0, sudoku_size):
                for value in range(1, sudoku_size + 1):
                    if (self.input_sudoku.values[row][column] == 0):
                        if (not self.input_sudoku.check_duplication(row, column, value)):
                            self.feasible_values.values[row][column].append(value)
                    else:
                        self.feasible_values.values[row][column].append(self.input_sudoku.values[row][column])
                        break


    def check_duplication_in_row(self, row, row_index):
        while(len(list(set(row))) != sudoku_size):
            for j in range(0, sudoku_size):
                if(self.input_sudoku.values[row_index][j] == 0):
                    feasible_value_index = random.randint(0, len(self.feasible_values.values[row_index][j]) - 1)
                    row[j] = self.feasible_values.values[row_index][j][feasible_value_index]


    def fill_blanks(self, chromosome):
        for i in range(0, sudoku_size):
            row = numpy.zeros(sudoku_size)
            for j in range(0, sudoku_size):

                if(self.input_sudoku.values[i][j] == 0):
                    feasible_value_index = random.randint(0, len(self.feasible_values.values[i][j]) - 1)
                    row[j] = self.feasible_values.values[i][j][feasible_value_index]
                else:
                    row[j] = self.input_sudoku.values[i][j]

            self.check_duplication_in_row(row, i)
            chromosome.values[i] = row


    def update_fitness(self):
        for chromosome in self.candidates:
            chromosome.update_fitness()
        return


    def create_first_population(self, input_sudoku):
        self.input_sudoku = input_sudoku
        self.feasible_values = Chromosome()
        self.prepare_feasible_values_for_each_cell()

        for _ in range(0, population_size):
            chromosome = Chromosome()
            self.fill_blanks(chromosome)
            self.candidates.append(chromosome)

        self.update_fitness()
        return
