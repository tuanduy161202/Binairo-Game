from nonogram import Nonogram
from state import State
from node import Node
import copy, time

ROWS = [[2, 2], [4, 4], [9], [9], [7], [5], [3], [1], [1]]
COLUMNS = [[3], [5], [6], [6], [7], [6], [6], [5], [3]]

class Backtracking:
  def __init__(self, row, column):
    self.nonogram = Nonogram(row, column)
    self.rows = self.nonogram.row_constraint
    self.cols = self.nonogram.col_constraint
    self.row_len = len(self.rows)
    self.col_len = len(self.cols)
    # define state
    self.state = State(self.rows, self.cols)
    # col_permu and row_permu is two dictionaries of columns and rows 
    self.col_permu = self.hash_col_permutation()
    self.row_permu = self.hash_row_permutation() 
    # Number of node have traverse, and number of node created
    self.node_traversed = 0
    self.node_created = 0

    start_time = time.time()

    goal_state = self.backtracking_search(self.state)
    goal_state.state.print_board()

    stop_time = time.time()
    print('Time: %s seconds' %(stop_time - start_time)) 

  # ------------------ MAIN FUNCTION ----------------------#
  def backtracking_search(self, state):
    node = Node(state, None, 0)
    # print(self.col_permu)
    # Calling recursive function
    return self.recursive_btrack(node)

  def recursive_btrack(self, node):
    # Check if state met goal or not, create a deep copy of state each time we check - stopping condition
    if self.is_goal(copy.deepcopy(node.state.get_board())):
      print('Depth: ', node.depth)
      print('Number of node created: ', self.node_created)
      print('Number of node traversed: ', self.node_traversed)
      return node

    # get all possible permutation solution for all rows 
    rows = self.row_permu[node.state.filled]
    # print(node.state.filled)
    for row in rows:
      new_state = copy.deepcopy(node.state)
      new_state.add_row(list(row))
      self.node_created += 1

      # ckeck this newly row violate row contraints or not
      if self.check(new_state):
        self.node_traversed += 1

        new_node = Node(new_state, node, node.depth + 1)
        print(new_node.state.print_board())

        result = self.recursive_btrack(new_node)
        if result is not None:
          return result

        # Backtrack to previous state
        new_state.remove_row()
    return None

  # ------------------ HELPER FUNCTION ----------------------#
  # Check if there are constraint violation or not
  def check(self, state):
    if(state.filled == len(state.get_board())): 
      if not self.is_goal(copy.deepcopy(state.get_board())): 
        return False
    
    # List all the columns in the board and check for column constraint
    board = list(zip(*(state.get_board())))
    # print(board)
    for i in range(0, len(board)): 
      if not self.check_col(board[i], self.cols[i]):
        return False 
    return True

  # Check violation of column constraint (one column only)
  def check_col(self, col, constraints):
    filled = 0 # number of square got filled with "*"
    all_filled = 0 # number that have been filled (by both "*" or " ")

    # check if there are too many "*" in the column 
    for c in col: 
      if c == '*': 
        filled += 1
      if c != '?':
        all_filled += 1
    # If number of filled space larger than sum of constraint in one col -> false
    if filled > sum(constraints):
      return False

    counter = 0 # track size of '*' block
    curr_constraint = 0 # tracks the index of the constraint
    i = 0 # index of space in the column
    while i < all_filled: 
      # End of the constraints array
      if curr_constraint == len(constraints): 
        break 

      if col[i] == '*': 
        if constraints[curr_constraint] > (all_filled - i):
          return True
        counter = 1 
        for j in range(i + 1, all_filled): 
          if col[j] != '*':
              break 
          counter += 1 
            
        if counter != constraints[curr_constraint]: 
          return False 
        # Move to next constraint
        curr_constraint += 1
        i += counter 
      else: 
        i += 1 
    return True 

  # Check the state met the goal or not
  def is_goal(self, state):
    new_state = list(zip(*(state)))
    # print(new_state)
    # Check if each column in new_state available in column dictionary or not
    for i in range(len(self.col_permu)):
      if ''.join(new_state[i]) not in self.col_permu[i]: 
        return False
    return True 

  # Create col dictionary
  def hash_col_permutation(self):
    col = dict()
    for c in range(len(self.cols)):
      col[c] = self.nonogram.get_permutation(self.cols[c], self.row_len)
    return col

  # Create row dictionary
  def hash_row_permutation(self):
    row = dict()
    for r in range(len(self.rows)):
      row[r] = self.nonogram.get_permutation(self.rows[r], self.col_len)
    return row

Backtracking(ROWS, COLUMNS)