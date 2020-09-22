import time
import random

FIRST_HALF = 1
SECOND_HALF = 0
WITH_BOARD = 1
WITHOUT_BOARD = 0
POPULATION_SIZE = 100
SURVIVAL_THRESHOLD = 18
MUTATION_PROBABILITY = 0.30
FITNESS_OPTIMUM = 28
EVOLVE_ITERATIONS = 100
WRONG_STATE_WARNING = "The initial state is not valid."
"Please insert a correct state!"


class EightQueens:

    def __init__(self):
        self.population = []
        self.board = []
        self.solutions = []
        random.seed(time.time())
        self.init_population()

    def init_population(self):
        """ Generates a random initial population.
        """
        possible_values = ['1', '2', '3', '4', '5', '6', '7', '8']
        for i in range(POPULATION_SIZE):
            state_list = random.sample(possible_values, 8)
            state_string = ''.join(state_list)
            self.population.append(state_string)

    def fill_board(self, state):
        """ Draws chess board for a given state.
        """
        self.board = []
        row = []
        for i in range(8):
            for j in range(8):
                if(i+1 == int(state[j])):
                    row.append('Q')
                else:
                    row.append('E')
            self.board.append(row)
            row = []

    def print_board(self):
        for line in self.board:
            print(line)

    def get_attacking_queens_count(self, state):
        """ Calculates the number of directly or indirectly attacking queens
            for a given state.
        """
        self.fill_board(state)
        return self.get_queens_in_row() + self.get_queens_in_diagonal()

    def get_queens_in_row(self):
        """ Calculate the amount of attacking queens considering the rows.
        """
        attacking_queens = 0
        queens_in_line = 0
        for i in range(8):
            for j in range(8):
                if(self.board[i][j] == 'Q'):
                    queens_in_line += 1
                if(j == 7):
                    if(queens_in_line >= 2):
                        attacking_queens += queens_in_line
                    queens_in_line = 0
        return attacking_queens

    def get_queens_in_diagonal(self):
        """ Calculate the amount of attacking queens considering the diagonals.
        """
        attacking_queens = 0
        queens_in_line = 0
        # calc diagonals 1) top left bottom right for upper half.
        for i in range(8):
            for j in range(8-i):
                if(self.board[j][j+i] == 'Q'):
                    queens_in_line += 1
                if(j == 7-i):
                    if(queens_in_line >= 2):
                        attacking_queens += queens_in_line
                    queens_in_line = 0

        # calc diagonals 2) top left bottom right for lower half.
        for i in range(1, 8):
            for j in range(8-i):
                if(self.board[j+i][j] == 'Q'):
                    queens_in_line += 1
                if(j == 7-i):
                    if(queens_in_line >= 2):
                        attacking_queens += queens_in_line
                    queens_in_line = 0

        # calc diagonals 3) top right bottom left for upper half.
        for i in range(8):
            for j in range(8-i):
                if(self.board[j][7-(j+i)] == 'Q'):
                    queens_in_line += 1
                if(j == 7-i):
                    if(queens_in_line >= 2):
                        attacking_queens += queens_in_line
                    queens_in_line = 0

        # calc diagonals 4) top right bottom left for lower half.
        for i in range(1, 8):
            for j in range(8-i):
                if(self.board[j+i][7-(j)] == 'Q'):
                    queens_in_line += 1
                if(j == 7-i):
                    if(queens_in_line >= 2):
                        attacking_queens += queens_in_line
                    queens_in_line = 0
        return attacking_queens

    def get_fitness_value(self, state):
        """ Returns value of fitness function for given state.
        """
        return FITNESS_OPTIMUM - self.get_attacking_queens_count(state)

    def evolve(self):
        """ Main method of this code.
            Mimics the genetic evolutionary steps.
            Filters states with low fitness
            values and reproduces the ones that are left.
        """
        start_time = time.time()
        for i in range(EVOLVE_ITERATIONS):
            self.filter_states()
            self.reproduce()
            current_winning_state = self.get_winning_state()
            current_fitness = self.get_fitness_value(current_winning_state)
            if(current_fitness == FITNESS_OPTIMUM):
                print("Optimum found after %s iterations!" % (i+1))
                self.output_best_individuum(current_winning_state,
                                            current_fitness, WITH_BOARD, i+1)
                break
            self.output_best_individuum(current_winning_state,
                                        current_fitness, WITHOUT_BOARD, i+1)

        # print additional infos
        print("CONSTANTS \n\nPOPULATION_SIZE %s \n"
              "SURVIVAL_THRESHOLD % s \nMUTATION_PROBABILITY %s\n"
              "FITNESS_OPTIMUM %s" %
              (POPULATION_SIZE, SURVIVAL_THRESHOLD,
               MUTATION_PROBABILITY, FITNESS_OPTIMUM))
        duration = time.time() - start_time
        print("It took: %s seconds" % round(duration))

    def output_best_individuum(self, winning_state, fitness, mode, iteration):
        """ Prints fitness value and board for winning state.
        """
        if(mode == WITH_BOARD):
            self.fill_board(winning_state)
            self.print_board()
        print("Fitness value: %s state: %s current iteration: %s "
              % (fitness, winning_state, iteration))

    def filter_states(self):
        """ Filters states that are below our survival threshold value.
            And replaces them with a better state that will be
            chosen by probabilities that depend on their fitness value.
        """
        for state in self.population:
            if(self.get_fitness_value(state) <= SURVIVAL_THRESHOLD):
                self.population.remove(state)
                self.population.append(self.choose_replacement())

    def choose_replacement(self):
        """ Selects a state from our population that we will clone
            to keep the population size constant after filtering.
            Values with higher fitness value will have
            higher chances to be picked.
        """
        fitness_values = []
        for state in self.population:
            fitness_values.append(self.get_fitness_value(state))
        return random.choices(self.population, fitness_values)[0]

    def get_winning_state(self):
        """ Returns the current fittest state without
            any randomness.
        """
        fittest_state = ""
        fittest_value = 0
        current_fitness = 0
        for state in self.population:
            current_fitness = self.get_fitness_value(state)
            if(current_fitness > fittest_value):
                fittest_value = current_fitness
                fittest_state = state
        return fittest_state

    def grouped(self, iterable, n):
        """ Returns non overlapping n-sized pairs of given iterable.
        """
        return zip(*[iter(iterable)]*n)

    def reproduce(self):
        """ Reproduces the whole population.
            This contains the crossover and the mutation.
        """
        # iterate pair wise using python iterator
        iterator = iter(self.population)
        # go through pairs
        for index, pair in enumerate(self.grouped(iterator, 2)):
            resulting_states = list(self.crossover(pair[0], pair[1]))
            # chance to mutate state
            if(random.random() < MUTATION_PROBABILITY):
                resulting_states[0] = self.mutate(resulting_states[0])
            if(random.random() < MUTATION_PROBABILITY):
                resulting_states[1] = self.mutate(resulting_states[1])
            self.population[2*index] = resulting_states[0]
            self.population[2*index+1] = resulting_states[1]

    def mutate(self, state):
        """ Mutates a random position of the given state
            and returns it.
        """
        selected_bit = random.randint(0, 7)
        # make sure mutate does change the value.
        while (True):
            selected_value = random.randint(1, 8)
            if(state[selected_bit] != str(selected_value)):
                break
        if(selected_bit < 7):
            return (state[0:selected_bit]+str(selected_value) +
                    state[selected_bit+1:])
        else:
            return state[0:selected_bit]+str(selected_value)

    def crossover(self, first_state, second_state):
        """ Randomly recombinates two states.
            Returns them as a pair.
        """
        cut_pos = round(random.random()*5)+1
        if(random.random() > 0.5):
            return self.swap_halves(first_state, second_state,
                                    cut_pos, FIRST_HALF)
        else:
            return self.swap_halves(first_state, second_state,
                                    cut_pos, SECOND_HALF)

    def swap_halves(self, first_state, second_state, cut_pos, mode):
        """" Cuts both states at cut position and swaps
             the resulting parts with each other.

             Returns a pair of cut and swapped states.
        """
        if(mode == FIRST_HALF):
            resulting_first_state = (second_state[0:cut_pos:]
                                     + first_state[cut_pos:])
            resulting_second_state = (first_state[0:cut_pos:]
                                      + second_state[cut_pos:])
            return (resulting_first_state, resulting_second_state)
        elif(mode == SECOND_HALF):
            resulting_first_state = (first_state[0:cut_pos]
                                     + second_state[cut_pos:])
            resulting_second_state = (second_state[0:cut_pos]
                                      + first_state[cut_pos:])
            return (resulting_first_state, resulting_second_state)

    def backtracking(self, state="00000000", position=0):
        """ Solves the eight queens problem using backtracking.
            Puts one queen after another on the board until
            the first queen will have been at every place
            and backtracked completely. Backtrack as soon as we
            can't find a position for a queen where our
            get_attacking_queens does not return a zero.
        """
        if(position == 8 and self.get_attacking_queens_count(state) == 0):
            print("solution was found! it is state: %s " % state)
            self.solutions.append(state)
            return True
        # try out all eight possible fields
        for i in range(8):
            if(position < 7):
                resulting_state = state[0:position]+str(i+1)+state[position+1:]
            else:
                resulting_state = state[0:position]+str(i+1)
            # if we found a qualified position
            if(self.get_attacking_queens_count(resulting_state) == 0):
                # recursively check if it will lead us to succes
                if(self.backtracking(resulting_state, position+1)):
                    # continue until every combination has been tried.
                    continue


if __name__ == '__main__':
    eight_queens = EightQueens()
    # solution using the genetic algorithm
    # eight_queens.evolve()
    # soultion using backtracking
    eight_queens.backtracking()
