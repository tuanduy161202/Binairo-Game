ROWS = [[2, 2], [4, 4], [9], [9], [7], [5], [3], [1], [1]]
COLUMNS = [[3], [5], [6], [6], [7], [6], [6], [5], [3]]


# Nonogram board

class Nonogram:
    def __init__(self, rows, columns):
        self.row_constraint = rows
        self.row_len = len(self.row_constraint)
        self.col_constraint = columns
        self.col_len = len(self.col_constraint)
        self.board = [["*" for x in range(self.col_len)] for y in range(self.row_len)]

    # Print Board
    def print_board(self):
        for r in self.board:
            print(' '.join(r))

    # Print State
    def print_state(self, state):
        string = ""
        for row in state:
            string += str(row)
            string += "\n"
        return string

    # ------------------ HELPER FUNCTION ----------------------#
    # get all permutation of '*' in 1 row
    def get_permutation(self, constraints, row_len):
        # create a block of 1st constraint in constraint array
        blocks = "*" * constraints[0]

        # There is only 1 constraint in row
        if len(constraints) == 1:
            res = []
            for i in range(row_len - constraints[0] + 1):
                # space before 1st blcok
                prev = " " * i
                # space after 1st block
                after = " " * (row_len - i - constraints[0])
                res.append(prev + blocks + after)
            return res

        # There are many constrains in 1 row - We iterate through it
        res = []
        for i in range(constraints[0], row_len):
            for p in self.get_permutation(constraints[1:], row_len - i - 1):
                prev = " " * (i - constraints[0])
                res.append(prev + blocks + " " + p)
        return res

    # return number of violation in 1 column - use to evaluate fitness
    def check_constraint(self, constraints_list, index, current):
        violate = 0
        for constraint in constraints_list[index]:
            # flag to determine if the constraint is met
            flag = False
            for i in range(0, len(current)):
                if current[i] == "*":
                    counter = 1
                    for j in range(i + 1, len(current)):
                        counter += 1
                        if current[j] != "*":
                            counter -= 1
                            break
                    if counter == constraint:
                        # backtrack and remove that out of consideration
                        for a in range(0, constraint):
                            current[i + a] = " "
                        flag = True
                        break
                    else:
                        for a in range(0, counter):
                            current[i + a] = " "
                        break
            if flag is False:
                violate += 1
        # check for any addition fill blank
        for square in current:
            if square == "*":
                violate += 1
        return violate

    # Check constraint for one column
    def check_one_column(self, state, column):
        current_col = []
        for i in range(0, self.row_len):
            current_col.append(state[i][column])
        return self.check_constraint(self.col_constraint, column, current_col)

    # Check for all column
    def check_all_column(self, solution):
        violation = 0
        for i in range(0, self.col_len):
            violation += self.check_one_column(solution, i)
        return violation

# stuff = Nonogram(ROWS, COLUMNS)
# print("*" * stuff.row_constraint[0][1])
