import numpy
import random

from .constants import *

class Chromosome(object):
    def __init__(self, values=None):
        self.values = numpy.zeros((sudoku_size, sudoku_size), dtype=int) if not numpy.any(values) else values
        self.fitness = None
        return


    def __lt__(self, o: object):
        return (self.fitness < o.fitness)


    def check_duplication(self, row, column, value):
        if (self.check_column_duplication(column, value) or
            self.check_block_duplication(row, column, value) or
            self.check_row_duplication(row, value)):
            return True
        return False


    def check_row_duplication(self, row, value):
        for column in range(0, sudoku_size):
            if(self.values[row][column] == value):
               return True
        return False


    def check_column_duplication(self, column, value):
        for row in range(0, sudoku_size):
            if(self.values[row][column] == value):
               return True
        return False


    def check_block_duplication(self, row, column, value):
        i = 3 * (int(row / 3))
        j = 3 * (int(column / 3))

        if (  (self.values[i][j] == value)
           or (self.values[i + 1][j] == value)
           or (self.values[i + 2][j] == value)

           or (self.values[i][j + 1] == value)
           or (self.values[i + 1][j + 1] == value)
           or (self.values[i + 2][j + 1] == value)

           or (self.values[i][j + 2] == value)
           or (self.values[i + 1][j + 2] == value)
           or (self.values[i + 2][j + 2] == value)):

            return True

        else:
            return False


    def calculate_rows_fitness(self):
        rows_fitness = 0
        rows_count = numpy.zeros(sudoku_size)

        for i in range(0, sudoku_size):
            for j in range(0, sudoku_size):
                rows_count[self.values[i][j] - 1] += 1
            rows_fitness += (1.0 / len(set(rows_count))) / sudoku_size
            rows_count = numpy.zeros(sudoku_size)

        return rows_fitness


    def calculate_columns_fitness(self):
        columns_fitness = 0
        columns_count = numpy.zeros(sudoku_size)
        for i in range(0, sudoku_size):
            for j in range(0, sudoku_size):
                columns_count[self.values[j][i] - 1] += 1
            columns_fitness += (1.0 / len(set(columns_count))) / sudoku_size
            columns_count = numpy.zeros(sudoku_size)

        return columns_fitness


    def calculate_blocks_fitness(self):
        blocks_count = numpy.zeros(sudoku_size)
        blocks_fitness = 0
        for i in range(0, sudoku_size, 3):
            for j in range(0, sudoku_size, 3):
                blocks_count[self.values[i][j] - 1] += 1
                blocks_count[self.values[i+1][j] - 1] += 1
                blocks_count[self.values[i+2][j] - 1] += 1

                blocks_count[self.values[i][j+1] - 1] += 1
                blocks_count[self.values[i+1][j+1] - 1] += 1
                blocks_count[self.values[i+2][j+1] - 1] += 1

                blocks_count[self.values[i][j+2] - 1] += 1
                blocks_count[self.values[i+1][j+2] - 1] += 1
                blocks_count[self.values[i+2][j+2] - 1] += 1

                blocks_fitness += (1.0 / len(set(blocks_count))) / sudoku_size
                blocks_count = numpy.zeros(sudoku_size)

        return blocks_fitness


    def calculate_fitness(self):
        if (int(self.rows_fitness) == 1 and
                int(self.columns_fitness) == 1 and
                int(self.blocks_fitness) == 1):
            fitness = 1.0
        else:
            fitness = self.columns_fitness * self.blocks_fitness
        return fitness



    def update_fitness(self):
        self.rows_fitness = self.calculate_rows_fitness()
        self.columns_fitness = self.calculate_columns_fitness()
        self.blocks_fitness = self.calculate_blocks_fitness()
        self.fitness = self.calculate_fitness()


    def check_mutate_duplication(self, input_sudoku, dest_column, source_column, row):
        if (not input_sudoku.check_column_duplication(dest_column, self.values[row][source_column]) and
            not input_sudoku.check_column_duplication(source_column, self.values[row][dest_column]) and
            not input_sudoku.check_block_duplication(row, dest_column, self.values[row][source_column]) and
            not input_sudoku.check_block_duplication(row, source_column, self.values[row][dest_column])):
            return True
        return False


    def mutate(self, mutation_rate, input_sudoku):
        while(True):
            row = random.randint(0, sudoku_size - 1)
            source_column = random.randint(0, sudoku_size - 1)
            dest_column = random.randint(0, sudoku_size - 1)
            while(source_column == dest_column):
                source_column = random.randint(0, sudoku_size - 1)
                dest_column = random.randint(0, sudoku_size - 1)

            if (input_sudoku.values[row][source_column] == 0 and input_sudoku.values[row][dest_column] == 0):
                if (self.check_mutate_duplication(input_sudoku, dest_column, source_column, row)):
                    self.values[row][source_column], self.values[row][dest_column] = self.values[row][dest_column], self.values[row][source_column]
                    break

        return True
