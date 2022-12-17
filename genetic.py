from nonogram import Nonogram
import random, time, operator

ROWS = [[2, 2], [4, 4], [9], [9], [7], [5], [3], [1], [1]]
COLUMNS = [[3], [5], [6], [6], [7], [6], [6], [5], [3]]

# Solution class - store combination of state and fitness
class Solution:
  def __init__(self, state, fitness):
      self.state = state
      self.fitness = fitness

class Genetic:
  global mutation_rate, crossover_rate, population_limit, population, fitness
  population = []
  fitness = []
  mutation_rate = 30
  crossover_rate = 75
  population_limit = 300
  
  def __init__(self, row, column):
    self.nonogram = Nonogram(row, column)
    self.rows = self.nonogram.row_constraint
    self.cols = self.nonogram.col_constraint
    self.row_len = len(self.rows)
    self.col_len = len(self.cols)


    global population, fitness

    start = time.time()

    # ------------------ MAIN FUNCTION ----------------------#
    # Step 1: initial Population
    population = self.generate_population()

    flag = None
    count = 0
    while flag is None:
      count = count + 1
      print("Generate " + str(count) + " times \n")

      # Step 2: fitness function
      fitness = self.eval_fitness(population)

      # Each solution contains population and its fitness
      solution = self.combine(population, fitness)

      # Create new population
      population_arr = []
      # Step 3: Selection
      parents = self.select(solution)
      
      # Create children
      while(len(population_arr) <= population_limit):
        # Step 4: CrossOver
        cross = self.crossover(parents)

        # Step 5: Mutation 
        children = self.mutation(cross)

        population_arr.append(children)
      # ------------------------------------------
      population = population_arr

      # Check population met goal or not
      flag = self.check(population)
      
    stop = time.time()
    print('Time: ', stop - start)
    print ("Number of generations: %s" % count)
    print (self.nonogram.print_state(flag))
    

  # ------------------ HELPER FUNCTION ----------------------#
  # Generate 1st random population
  def generate_population(self):
    population_arr = []

    # Take random solution that met row constraint
    for i in range(0, population_limit):
      row_sol = []
      for row in self.rows:
        sol = self.nonogram.get_permutation(row, self.row_len)
        row_sol.append(random.choice(sol))
      population_arr.append(row_sol)
    return population_arr

  # Fitness function: return number of violation in all of column
  def eval_fitness(self, population):
    fit = []
    for solution in population:
      fit.append(self.nonogram.check_all_column(solution))
    return fit

  def combine(self, population, fitness):
    solutions = []
    for i in range(0, len(population)):
      # Structure of 1 solution: sol = [population, fitness]
      sol = Solution(population[i], fitness[i])
      solutions.append(sol)
    return solutions

  # Select function - select two parent and crossover to create new children 
  def select(self, solution):
    sorted_solution = sorted(solution, key = operator.attrgetter('fitness'))
    # Take 2 top fitness value solution
    solution1 = sorted_solution[0]
    solution2 = sorted_solution[1]

    # Print the parent and its fitness
    print ("Two chosen parents are \n")
    print (self.nonogram.print_state(solution1.state))
    print("fitness function value: " + str(solution1.fitness))
    print("\n\n")
    print (self.nonogram.print_state(solution2.state))
    print("fitness function value: " + str(solution2.fitness))
    print("\n\n")
    
    return [solution1.state, solution2.state]

  # Crossover function - form a new children set
  def crossover(self, parents):
    propability = random.randint(0, 100)
    if propability < crossover_rate:
      crossover_point = random.randint(0, self.row_len)
      
      children = []
      for i in range (0, crossover_point):
        children.append(parents[0][i])
      
      for j in range (crossover_point, self.row_len):
        children.append(parents[1][j])
    
    else:
      children = parents[0]
    
    return children

  # Mutation function - mutate all children in children set
  def mutation(self, children):
    new_children = []
    for i in range(0, self.row_len):
      propability = random.randint(0, 100)
      if propability < mutation_rate:
        rand = random.choice(self.nonogram.get_permutation(self.rows[i], self.row_len))
        new_children.append(rand)
      else:
        new_children.append(children[i])
    return new_children

  # Check for violation
  # Since starting state has met row constraint, only check for column constraint
  def check(self, population):
    for sol in population:
      if self.nonogram.check_all_column(sol) == 0:
        return sol
      return None
    
Genetic(ROWS, COLUMNS)
