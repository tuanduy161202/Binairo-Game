# State class to present state in backtracking algo

class State:
  def __init__(self, row_constraint, col_constraint):
    self.row_constraint = row_constraint
    self.row_len = len(row_constraint)
    self.col_constraint = col_constraint
    self.col_len = len(col_constraint)
    self.board = [["?" for x in range(self.col_len)] for y in range(self.row_len)]
    # Rows index have been filled with solution ("*")
    self.filled = 0

  def get_board(self):
    return self.board

  def print_board(self):
    for r in self.board:
      print(' '.join(r))
  
  def add_row(self, row):
    self.board[self.filled] = row
    self.filled += 1

  # Remove row function - use to backtrack prev state
  def remove_row(self):
    if self.filled == 0:
      return "error: no row to remove"

    self.board[self.filled - 1] = ["?"] * (self.row_len)
    self.filled -= 1
