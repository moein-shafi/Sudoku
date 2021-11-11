import numpy
import random
from genetic.constants import *

class Candidate(object):
    def __init__(self, values=None):
        self.values = numpy.zeros((Nd, Nd), dtype=int) if not numpy.any(values) else values
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
        for column in range(0, Nd):
            if(self.values[row][column] == value):
               return True
        return False


    def check_column_duplication(self, column, value):
        for row in range(0, Nd):
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
        rows_count = numpy.zeros(Nd)

        for i in range(0, Nd):
            for j in range(0, Nd):
                rows_count[self.values[i][j]-1] += 1
            rows_fitness += (1.0 / len(set(rows_count))) / Nd
            rows_count = numpy.zeros(Nd)

        return rows_fitness


    def calculate_columns_fitness(self):
        columns_fitness = 0
        columns_count = numpy.zeros(Nd)
        for i in range(0, Nd):
            for j in range(0, Nd):
                columns_count[self.values[j][i]-1] += 1
            columns_fitness += (1.0 / len(set(columns_count))) / Nd
            columns_count = numpy.zeros(Nd)

        return columns_fitness


    def calculate_blocks_fitness(self):
        blocks_count = numpy.zeros(Nd)
        blocks_fitness = 0
        for i in range(0, Nd, 3):
            for j in range(0, Nd, 3):
                blocks_count[self.values[i][j]-1] += 1
                blocks_count[self.values[i+1][j]-1] += 1
                blocks_count[self.values[i+2][j]-1] += 1

                blocks_count[self.values[i][j+1]-1] += 1
                blocks_count[self.values[i+1][j+1]-1] += 1
                blocks_count[self.values[i+2][j+1]-1] += 1

                blocks_count[self.values[i][j+2]-1] += 1
                blocks_count[self.values[i+1][j+2]-1] += 1
                blocks_count[self.values[i+2][j+2]-1] += 1

                blocks_fitness += (1.0 / len(set(blocks_count))) / Nd
                blocks_count = numpy.zeros(Nd)

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
 

    def mutate(self, mutation_rate, given):
        rand = random.uniform(0, 1.1)
        while (rand > 1):
            rand = random.uniform(0, 1.1)
    
        if (rand < mutation_rate):
            while(True):
                row1 = random.randint(0, Nd - 1)
                row2 = row1
                
                from_column = random.randint(0, Nd - 1)
                to_column = random.randint(0, Nd - 1)
                while(from_column == to_column):
                    from_column = random.randint(0, Nd - 1)
                    to_column = random.randint(0, Nd - 1)   

                if (given.values[row1][from_column] == 0 and given.values[row1][to_column] == 0):
                    # ...and that we are not causing a duplicate in the rows' columns.
                    if (not given.check_column_duplication(to_column, self.values[row1][from_column])
                       and not given.check_column_duplication(from_column, self.values[row2][to_column])
                       and not given.check_block_duplication(row2, to_column, self.values[row1][from_column])
                       and not given.check_block_duplication(row1, from_column, self.values[row2][to_column])):
                    
                        # Swap values.
                        temp = self.values[row2][to_column]
                        self.values[row2][to_column] = self.values[row1][from_column]
                        self.values[row1][from_column] = temp
                        break
    
        return True
