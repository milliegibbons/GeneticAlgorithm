import random
import sys

recursion_limit = 6000
sys.setrecursionlimit(recursion_limit)


# function that creates a random list to represent the queens on the board of specified size.
# the list index is the column on the board and the interger value is the row on the board.
def create_state(board_size):
    board = []
    for i in range(0, board_size):
        board.append(random.randint(0, (board_size) - 1))
    return board


# function that creates a population of specified size.
# a list of states created by the create_state function.
def create_population(size):
    population = []
    for i in range(0, size):
        new_state = create_state(board_size)
        population.append(new_state)
    return population


# function that calculates the number of collisions in a state
# using number collisions calculates the fitness of that state.
# Fitness is defined as how many pieces are attacking each other and therefore inhibiting the solution.
def collisions(state):
    collisions = 0
    for i in range(0, board_size):
        x = [i, state[i]]
        for j in range(0, len(state)):
            y = [j, state[j]]
            if (x[1] == y[1] or abs(x[0] - x[1]) == abs(y[0] - y[1])) and x != y:
                collisions += 1

    fitness = (56 - collisions) / 2
    return fitness


# To select the mating pool, a probability distribution of fitness values is created.
# this is to enable a higher chance of selecting the best solutions to be used for mating.
# fitness proportional selection
def fitness_calculation(population):
    fitness_sum = 0
    highest_score = 0
    prob_dist = []
    fitness_percentage = 0

    # For each state a cummulative sum is calculated
    for state in population:
        fitness_score = collisions(state)

        if fitness_score > highest_score:
            highest_score = fitness_score
            highest_state = state[0:board_size]

        state.append(fitness_score)
        fitness_sum += fitness_score

    # Creation of probability distribution
    for state in population:
        fitness_score = (state[-1])
        state.remove(fitness_score)
        fitness_percentage += fitness_score / fitness_sum
        state.append(fitness_percentage)
        prob_dist.append(fitness_percentage)
    return highest_score, highest_state, prob_dist


# Parents are selected at random. By using a probably distribtuion, it is likely that better solutions will be chosen as parents
# This method of selection is called roulette wheel/ fitness proportial selection
def parent_selection(prob_dist):
    parent_number = 2
    parents = []
    for j in range(0, parent_number):
        parent_select = random.random()
        if parent_select < prob_dist[0]:
            parent = population[0][0:board_size]
            parents.append(parent)
        for i in range(1, len(prob_dist)):
            if prob_dist[i - 1] <= parent_select and parent_select <= prob_dist[i]:
                parent = population[i][0:board_size]
                parents.append(parent)
    return parents


# Using the parents and the decided crossover point, two child states are created.
# By splitting and swapping the parent states at the crossover point
def crossover(crossing_point, parents):
    child1 = parents[0][0:crossing_point] + parents[1][crossing_point:]
    child2 = parents[1][0:crossing_point] + parents[0][crossing_point:]
    return child1, child2


# A randomly selected value in each child is swapped for another randomly selected value.
# This type of mutation is called flip.
def mutation(child1, child2):
    mutate = random.randint(0, (board_size - 1))
    child1[mutate] = random.randint(0, (board_size - 1))
    mutate = random.randint(0, (board_size - 1))
    child2[mutate] = random.randint(0, (board_size - 1))
    return child1, child2


# A function to create a generation of evolution.
# Calculating the fitness for each state in the population.
# Selecting parents from the mating pool.
# Creating child states using crossover and mutation.
# Returning the new population
def generation(population, count=0):
    count += 1
    new_population = []
    score = 0
    highest_score, highest_state, fitness_proportional = fitness_calculation(population)
    while len(new_population) < len(population):
        parents = parent_selection(fitness_proportional)
        child1, child2 = crossover(crossing_point, parents)
        child1, child2 = mutation(child1, child2)
        new_population.append(child1)
        new_population.append(child2)
        if highest_score > score:
            score = highest_score
            state = highest_state
    return score, state, new_population, count


# A recursive function, that calls the generation function until a solution is reached.
# The recursion runs to a maximum of 4000, if it runs to 4000 with no solution, the best state and score is generated.
def iteration(population, count=0):
    score, state, new_population, count = generation(population, count)
    if score == 28:
        print('Solution:', state)
        print('Number of iterations:', count)
        print("")
    else:
        if count == (5000):
            print('Maximum iterations reached')
            print('Best solution:', state)
            print('Best score:', score)
            print("")
        else:
            iteration(new_population, count)


# Parameter selection
# Ignition of solution
for i in range(0, 10):
    random.seed(i)
    board_size = 8
    crossing_point = 3
    population = create_population(150)
    generate_solution = iteration(population)

board_size = 5
crossing_point = 3
population_size = 50
population = create_population(population_size)
generate_solution = iteration(population)

board_size = 9
crossing_point = 5
population = create_population(150)
generate_solution = iteration(population)

# Optimisation 1
# Tournament selection is a different way of selecting the parent states.
# By selecting the strongest out of the number k.
k = 2


def tournament_selection(k):
    selected_parents = []
    parent_number = 2
    parents = []

    for j in range(0, parent_number):
        for i in range(0, k):

            parent_select = random.randint(0, (population_size - 1))
            parents.append(population[parent_select][0:board_size])

            winning_fitness = 0
            for parent in parents:
                fitness = collisions(parent)
                if fitness > winning_fitness:
                    winner = parent
                    winning_fitness = fitness

        selected_parents.append(winner)
    return selected_parents


# Optimisation 2
# Only mutating randomly if the integer is less than 5%. A method used to make it more realistic.
def optimisation_mutation(child1, child2):
    mutate1 = random.randint(0, 1)
    mutate2 = random.randint(0, 1)
    if mutate1 < 0.05:
        child1[mutate1] = random.randint(0, (board_size - 1))
    if mutate2 < 0.05:
        mutate = random.randint(0, (board_size - 1))
        child2[mutate2] = random.randint(0, (board_size - 1))
    else:
        child1 = child1
        child2 = child2

    return child1, child2


# An updated generation function to use the two new optimising functions.
def generation(population, count=0):
    count += 1
    new_population = []
    score = 0
    highest_score, highest_state, fitness_proportional = fitness_calculation(population)
    while len(new_population) < len(population):
        parents = tournament_selection(k)
        child1, child2 = crossover(crossing_point, parents)
        child1, child2 = optimisation_mutation(child1, child2)
        new_population.append(child1)
        new_population.append(child2)
        if highest_score > score:
            score = highest_score
            state = highest_state
    return score, state, new_population, count


# Parameter selection
# Ignition of solution
board_size = 5
crossing_point = 3
population = create_population(150)
generate_solution = iteration(population)
