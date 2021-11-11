import numpy
import random
import operator

from .candidate import Candidate
from genetic.constants import *

class Population(object):
    def __init__(self):
        self.candidates = list()
        return


    def sort(self):
        self.candidates.sort()


    def prepare_feasible_values_for_each_cell(self):
        self.feasible_values.values = [[[] for j in range(0, Nd)] for i in range(0, Nd)]
        for row in range(0, Nd):
            for column in range(0, Nd):
                for value in range(1, Nd + 1):
                    if (self.input_sudoku.values[row][column] == 0):
                        if (not self.input_sudoku.check_duplication(row, column, value)):
                            self.feasible_values.values[row][column].append(value)
                    else:
                        self.feasible_values.values[row][column].append(self.input_sudoku.values[row][column])
                        break


    def check_duplicate_in_row(self, row, row_index):
        while(len(list(set(row))) != Nd):
            for j in range(0, Nd):
                if(self.input_sudoku.values[row_index][j] == 0):
                    feasible_value_index = random.randint(0, len(self.feasible_values.values[row_index][j]) - 1)
                    row[j] = self.feasible_values.values[row_index][j][feasible_value_index]


    def fill_blanks(self, candidate):
        for i in range(0, Nd):
            row = numpy.zeros(Nd)
            for j in range(0, Nd):

                if(self.input_sudoku.values[i][j] == 0):
                    feasible_value_index = random.randint(0, len(self.feasible_values.values[i][j]) - 1)
                    row[j] = self.feasible_values.values[i][j][feasible_value_index]
                else:
                    row[j] = self.input_sudoku.values[i][j]

            self.check_duplicate_in_row(row, i)
            candidate.values[i] = row


    def update_fitness(self):
        for candidate in self.candidates:
            candidate.update_fitness()
        return


    def seed(self, input_sudoku):
        self.input_sudoku = input_sudoku
        self.feasible_values = Candidate()
        self.prepare_feasible_values_for_each_cell()

        for _ in range(0, Nc):
            candidate = Candidate()
            self.fill_blanks(candidate)
            self.candidates.append(candidate)

        self.update_fitness()
        print("Seeding complete.")
        return
