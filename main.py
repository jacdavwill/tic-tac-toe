from enum import IntEnum

SIDE_LEN = 3


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class Side(IntEnum):
    __order__ = 'UPPER_LEFT ABOVE UPPER_RIGHT LEFT RIGHT LOWER_LEFT BELOW LOWER_RIGHT'
    UPPER_LEFT = 1
    ABOVE = 2
    UPPER_RIGHT = 3
    LEFT = 4
    RIGHT = 5
    LOWER_LEFT = 6
    BELOW = 7
    LOWER_RIGHT = 8


PLAYER_1 = Player('Player 1', 'X')
PLAYER_2 = Player('Player 2', 'O')
print_board = []
play_board = []


def init_boards():
    global print_board
    global play_board
    print_board = []
    play_board = []
    for x in range(SIDE_LEN):
        row = []
        for y in range(SIDE_LEN):
            row.append(0)
        play_board.append(row)

    for x in range(SIDE_LEN * 12 - 1):
        row = []
        for y in range(SIDE_LEN * 4 - 1):
            row.append(' ')
        print_board.append(row)


def setup_board():
    global print_board
    for y in range(SIDE_LEN * 4 - 1):
        for x in range(SIDE_LEN * 12 - 1):
            if y % 4 == 3:
                print_board[x][y] = '-'
            elif x % 12 == 11:
                print_board[x][y] = '|'
            else:
                print_board[x][y] = ' '


def output_board():
    board = ""
    for y in range(SIDE_LEN * 4 - 1):
        row = ""
        for x in range(SIDE_LEN * 12 - 1):
            row += print_board[x][y]
        board += row + '\n'
    print(board)


def add_symbol(x, y, symbol):
    global play_board
    play_board[x][y] = symbol
    pivot = [12 * x, 4 * y]
    if symbol == 'X':
        print_board[pivot[0] + 4][pivot[1]] = '\\'
        print_board[pivot[0] + 6][pivot[1]] = '/'
        print_board[pivot[0] + 5][pivot[1] + 1] = 'X'
        print_board[pivot[0] + 4][pivot[1] + 2] = '/'
        print_board[pivot[0] + 6][pivot[1] + 2] = '\\'
    elif symbol == 'O':
        print_board[pivot[0] + 3][pivot[1]] = '/'
        print_board[pivot[0] + 4][pivot[1]] = '`'
        print_board[pivot[0] + 5][pivot[1]] = '`'
        print_board[pivot[0] + 6][pivot[1]] = '`'
        print_board[pivot[0] + 7][pivot[1]] = '\\'
        print_board[pivot[0] + 2][pivot[1] + 1] = '|'
        print_board[pivot[0] + 8][pivot[1] + 1] = '|'
        print_board[pivot[0] + 3][pivot[1] + 2] = '\\'
        print_board[pivot[0] + 4][pivot[1] + 2] = '_'
        print_board[pivot[0] + 5][pivot[1] + 2] = '_'
        print_board[pivot[0] + 6][pivot[1] + 2] = '_'
        print_board[pivot[0] + 7][pivot[1] + 2] = '/'


def get_side_coord(x, y, side):
    coord = x, y
    if side == Side.UPPER_LEFT:
        coord = x - 1, y - 1
    elif side == Side.ABOVE:
        coord = x, y - 1
    elif side == Side.UPPER_RIGHT:
        coord = x + 1, y - 1
    elif side == Side.LEFT:
        coord = x - 1, y
    elif side == Side.RIGHT:
        coord = x + 1, y
    elif side == Side.LOWER_LEFT:
        coord = x - 1, y + 1
    elif side == Side.BELOW:
        coord = x, y + 1
    elif side == Side.LOWER_RIGHT:
        coord = x + 1, y + 1

    if coord[0] < 0 or coord[0] >= SIDE_LEN or coord[1] < 0 or coord[1] >= SIDE_LEN:
        return None
    else:
        return coord


def check_for_winner():
    for x in range(SIDE_LEN):
        for y in range(SIDE_LEN):
            sym = play_board[x][y]
            if sym != 0:
                for side in Side:
                    loc = get_side_coord(x, y, side)
                    if loc is not None:
                        if play_board[loc[0]][loc[1]] == sym:
                            loc2 = get_side_coord(*loc, side)
                            if loc2 is not None:
                                if play_board[loc2[0]][loc2[1]] == sym:
                                    print("Congrats! You win!\n\n")
                                    return 1  # player has won
    for x in range(SIDE_LEN):
        for y in range(SIDE_LEN):
            if play_board[x][y] == 0:
                return 0  # no winner, continue playing
    return 2  # cat scratch


while True:
    print("Let's play Tic-Tac-Toe!")
    current_player = PLAYER_1
    init_boards()
    setup_board()
    output_board()
    while True:
        print(f"Ok, {current_player.name}, make your move!")
        input_row = int(input("Enter row #: "))
        input_col = int(input("Enter col #: "))

        if input_row < 1 or input_row > SIDE_LEN or input_col < 1 or input_col > SIDE_LEN:
            print("That space is not on the board, try again")
        elif play_board[input_col - 1][input_row - 1] != 0:
            print("That space is already taken, try again")
        else:
            add_symbol(input_col - 1, input_row - 1, current_player.symbol)
            if current_player == PLAYER_1:
                current_player = PLAYER_2
            else:
                current_player = PLAYER_1
            output_board()
            print("Good move!\n")

        result = check_for_winner()
        if result == 1:
            break
        elif result == 2:
            print("It is a tie!")
            break

    resp = input("Would you like to play again(Y/N): ")
    if 'y' in resp or 'Y' in resp:
        print("Great!")
    else:
        print("Ok, come back soon!")
        exit()
