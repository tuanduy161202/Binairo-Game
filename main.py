class Board:
    class __Cell:
        def __init__(self, value, fixed = False):
            self.fixed = fixed
            if value not in (0,1,'x'):
                raise "giá trị cô cờ không đúng"
            self.value = value

        def __eq__(self, other):
            return self.value == other.value

        def print(self):
            print("{}{:<2}".format(self.value, "*" if self.fixed else ""), end='')

    def __init__(self, size):
        if size % 2 != 0:
            raise "Kích thước bàn cờ không hợp lệ"
        self.size = size
        self.state = [[Board.__Cell('x') for i in range(size)] for j in range(size)]
        self.__positions = tuple((x, y) for x in range(size) for y in range(size))

    def printState(self):
        for i in range(self.size):
            for j in range(self.size):
                self.state[i][j].print()
                print(" ",end='')
            print()

    def input(self):
        fInput = open("input.txt", "r")
        for row in range(self.size):
            list = fInput.readline().split()
            for col in range(self.size):
                if list[col] == 'x':
                    self.state[row][col] = self.__Cell('x', False)
                else:
                    self.state[row][col] = self.__Cell(int(list[col]),True)

    # return tọa độ của ô thứ index
    # tính từ trái qua phải, trên xuống dưới, bắt đầu với index = 0
    def getXY(self, index):
        if index < 0 or index >= self.size**2:
            raise "index vượt bàn cờ rồi kìa"
        return self.__positions[index]

    def setCell(self, x, y, value):
        self.state[x][y].value = value

    # kiểm tra tính valid của bàn cờ tại ô (x,y)
    def isValidAtXY(self, x, y):
        # 6 dòng if check có 3 ô cùng loại liên tiếp không
        if y >= 2 \
                and self.state[x][y] == self.state[x][y - 1] \
                and self.state[x][y] == self.state[x][y - 2]:
            return False

        if y < self.size - 2 \
                and self.state[x][y] == self.state[x][y + 1] \
                and self.state[x][y] == self.state[x][y + 2]:
            return False

        if y > 0 and y < self.size - 1 \
                and self.state[x][y] == self.state[x][y - 1] \
                and self.state[x][y] == self.state[x][y + 1]:
            return False

        if x >= 2 and self.state[x][y] == self.state[x - 1][y] \
                and self.state[x][y] == self.state[x - 2][y]:
            return False

        if x < self.size - 2 \
                and self.state[x][y] == self.state[x + 1][y] \
                and self.state[x][y] == self.state[x + 2][y]:
            return False

        if x > 0 and x < self.size - 1 \
                and self.state[x][y] == self.state[x - 1][y] \
                and self.state[x][y] == self.state[x + 1][y]:
            return False

        # check số ô trắng và đen tại hàng x
        count0, count1 = 0, 0
        for i in range(self.size):
            if self.state[x][i].value == 0:
                count0 += 1
            elif self.state[x][i].value == 1:
                count1 += 1
        if count0 > self.size // 2 or count1 > self.size // 2:
            return False

        # check số trắng tại cột y
        count0, count1 = 0, 0
        for i in range(self.size):
            if self.state[i][y].value == 0:
                count0 += 1
            elif self.state[i][y].value == 1:
                count1 += 1
        if count0 > self.size // 2 or count1 > self.size // 2:
            return False
        return True

    # kiểm tra tính valid của bàn cờ
    def isValid(self):
        pass

    # check hàng row có là duy nhất từ hàng 0 đến row
    def checkRow(self, row):
        for i in range(row):
            same = True
            for j in range(self.size):
                if self.state[row][j] != self.state[i][j]:
                    same = False
                    break
            if same:
                return False
        return True

    # chek cột col có là duy nhất từ cột 0 đến col
    def checkCol(self, col):
        for i in range(col):
            same = True
            for j in range(self.size):
                if self.state[j][col] != self.state[j][i]:
                    same = False
                    break
            if same:
                return False
        return True


class DFS:
    @staticmethod
    def dfs(board, index = 0):
        # đã điền hết bàn cờ
        if index == board.size**2:
            return True

        x, y = board.getXY(index)
        for value in (0,1):
            # gán giá trị cho ô trống
            if not board.state[x][y].fixed:
                board.state[x][y].value = value
            if not board.isValidAtXY(x, y):
                continue
            # kiểm tra cột có là duy nhất nếu điền xong cột y
            if x == board.size - 1 and not board.checkCol(y):
                continue
            # kiểm tra hàng có duy nhất nếu điền xong hàng x
            if y == board.size - 1 and not board.checkRow(x):
                continue
            if DFS.dfs(board, index+1):
                return True
        # trả lại giá trị trống cho ô
        if not board.state[x][y].fixed:
            board.state[x][y].value = 'x'
        return False

b=Board(6)
b.input()
solve = DFS()
DFS.dfs(b)
b.printState()