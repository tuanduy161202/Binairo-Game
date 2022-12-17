# Node in backtracking tree
class Node:
  def __init__(self, state, prev_node, depth):
    self.state = state
    self.parent_node = prev_node
    self.depth = depth