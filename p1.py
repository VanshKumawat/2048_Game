import random

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.board = [[0]*size for _ in range(size)]
        self.score = 0
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empty_cells = [(i, j) for i in range(self.size)
                              for j in range(self.size)
                              if self.board[i][j] == 0]
        if not empty_cells:
            return
        i, j = random.choice(empty_cells)
        self.board[i][j] = 4 if random.random() < 0.1 else 2

    def can_move(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return True
                if i < self.size - 1 and self.board[i][j] == self.board[i+1][j]:
                    return True
                if j < self.size - 1 and self.board[i][j] == self.board[i][j+1]:
                    return True
        return False

    def slide_and_combine_row(self, row):
        """ Slide non-zero tiles left, combine equal tiles, slide again """
        # Slide
        new_row = [num for num in row if num != 0]
        result_row = []
        skip = False
        for i in range(len(new_row)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_row) and new_row[i] == new_row[i+1]:
                result_row.append(new_row[i]*2)
                self.score += new_row[i]*2
                skip = True
            else:
                result_row.append(new_row[i])
        result_row += [0] * (self.size - len(result_row))
        return result_row

    def move_left(self):
        moved = False
        new_board = []
        for row in self.board:
            new_row = self.slide_and_combine_row(row)
            if new_row != row:
                moved = True
            new_board.append(new_row)
        if moved:
            self.board = new_board
            self.spawn_tile()
        return moved

    def move_right(self):
        moved = False
        new_board = []
        for row in self.board:
            reversed_row = list(reversed(row))
            new_row = self.slide_and_combine_row(reversed_row)
            new_row = list(reversed(new_row))
            if new_row != row:
                moved = True
            new_board.append(new_row)
        if moved:
            self.board = new_board
            self.spawn_tile()
        return moved

    def move_up(self):
        moved = False
        transposed = list(zip(*self.board))
        new_transposed = []
        for row in transposed:
            new_row = self.slide_and_combine_row(list(row))
            if list(row) != new_row:
                moved = True
            new_transposed.append(new_row)
        if moved:
            self.board = [list(row) for row in zip(*new_transposed)]
            self.spawn_tile()
        return moved

    def move_down(self):
        moved = False
        transposed = list(zip(*self.board))
        new_transposed = []
        for row in transposed:
            reversed_row = list(reversed(row))
            new_row = self.slide_and_combine_row(reversed_row)
            new_row = list(reversed(new_row))
            if list(row) != new_row:
                moved = True
            new_transposed.append(new_row)
        if moved:
            self.board = [list(row) for row in zip(*new_transposed)]
            self.spawn_tile()
        return moved

    def print_board(self):
        for row in self.board:
            print(row)
        print(f"Score: {self.score}")
        print()
        
        
        
# if __name__ == "__main__":
#     game = Game2048()
#     game.print_board()

#     # simulate a left move
#     game.move_left()
#     game.print_board()

#     # simulate a down move
#     game.move_down()
#     game.print_board()

#     while game.can_move():
#         game.move_left()
#         game.print_board()

# if __name__ == "__main__":
#     game = Game2048()
#     game.print_board()

#     # simulate some individual moves first
#     game.move_left()
#     game.print_board()

#     game.move_down()
#     game.print_board()

#     # now loop safely
#     while game.can_move():
#         moved = False
#         for move_fn in [game.move_left, game.move_right, game.move_up, game.move_down]:
#             if move_fn():
#                 moved = True
#                 game.print_board()
#                 break
#         if not moved:
#             break

#     print("Game over!")

if __name__ == "__main__":
    game = Game2048()
    game.print_board()

    while game.can_move():
        move = input("Enter move (w/a/s/d): ").lower()
        moved = False
        if move == 'w':
            moved = game.move_up()
        elif move == 's':
            moved = game.move_down()
        elif move == 'a':
            moved = game.move_left()
        elif move == 'd':
            moved = game.move_right()

        if moved:
            game.print_board()
        else:
            print("Move not possible!")

    print("Game over!")