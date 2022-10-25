
from random import shuffle
from tkinter import Canvas, Tk

BOARD_SIZE = 4
SQUARE_SIZE = 80
EMPTY_SQUARE = BOARD_SIZE ** 2

root = Tk()
root.title("make Fifteen")

c = Canvas(root, width=BOARD_SIZE * SQUARE_SIZE,
           height=BOARD_SIZE * SQUARE_SIZE, bg='#808080')
c.pack()


def get_inv_count():
    """ Function counting quantity of moves """
    inversions = 0
    inversion_board = board[:]
    inversion_board.remove(EMPTY_SQUARE)
    for i in range(len(inversion_board)):
        first_item = inversion_board[i]
        for j in range(i+1, len(inversion_board)):
            second_item = inversion_board[j]
            if first_item > second_item:
                inversions += 1
    return inversions


def is_solvable():
    """ function defines solution """
    num_inversions = get_inv_count()
    if BOARD_SIZE % 2 != 0:
        return num_inversions % 2 == 0
    else:
        empty_square_row = BOARD_SIZE - (board.index(EMPTY_SQUARE) // BOARD_SIZE)
        if empty_square_row % 2 == 0:
            return num_inversions % 2 != 0
        else:
            return num_inversions % 2 == 0


def get_empty_neighbor(index):
    # getting index from an empty box in a list
    empty_index = board.index(EMPTY_SQUARE)
    # defining distance from empty box to the box that you clicked
    abs_value = abs(empty_index - index)
    # If an empty cell is above or below the clicked cell
    # return the index of the empty cell
    if abs_value == BOARD_SIZE:
        return empty_index
    # If an empty cell is left or right
    elif abs_value == 1:
        # Checking that the blocks are in the same row
        max_index = max(index, empty_index)
        if max_index % BOARD_SIZE != 0:
            return empty_index
    # There was no empty field next to the block
    return index


def draw_board():
    # remove everything that is drawn on the canvas
    c.delete('all')
    # Our task is to group the tags from the list into a square
    #  BOARD_SIZE x BOARD_SIZE
    # i and j will be the coordinates for each individual tag
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # get the value that we will need to draw
            # on the square
            index = str(board[BOARD_SIZE * i + j])
            # if it's not a cell we want to leave empty
            if index != str(EMPTY_SQUARE):
                # draw a square at the given coordinates
                c.create_rectangle(j * SQUARE_SIZE, i * SQUARE_SIZE,
                                   j * SQUARE_SIZE + SQUARE_SIZE,
                                   i * SQUARE_SIZE + SQUARE_SIZE,
                                   fill='#43ABC9',
                                   outline='#FFFFFF')
                # write the number in the center of the square
                c.create_text(j * SQUARE_SIZE + SQUARE_SIZE / 2,
                              i * SQUARE_SIZE + SQUARE_SIZE / 2,
                              text=index,
                              font="Arial {} italic".format(int(SQUARE_SIZE / 4)),
                              fill='#FFFFFF')


def show_victory_plate():
    # Draw a black square in the center of the field
    c.create_rectangle(SQUARE_SIZE / 5,
                       SQUARE_SIZE * BOARD_SIZE / 2 - 10 * BOARD_SIZE,
                       BOARD_SIZE * SQUARE_SIZE - SQUARE_SIZE / 5,
                       SQUARE_SIZE * BOARD_SIZE / 2 + 10 * BOARD_SIZE,
                       fill='#000000',
                       outline='#FFFFFF')
    # We write in red the text Victory
    c.create_text(SQUARE_SIZE * BOARD_SIZE / 2, SQUARE_SIZE * BOARD_SIZE / 1.9,
                  text="ПОБЕДА!", font="Helvetica {} bold".format(int(10 * BOARD_SIZE)), fill='#DC143C')


def click(event):
    # Get click coordinates
    x, y = event.x, event.y
    # Converting coordinates from pixels to cells
    x = x // SQUARE_SIZE
    y = y // SQUARE_SIZE
    # Get the index in the list of the object we clicked on
    board_index = x + (y * BOARD_SIZE)
    # We get the index of an empty cell in the list. We will write this function later.
    empty_index = get_empty_neighbor(board_index)
    # Swap an empty cell and a clicked cell
    board[board_index], board[empty_index] = board[empty_index], board[board_index]
    # Redrawing the playing field
    draw_board()
    # If the current state of the board corresponds to the correct one, we draw a victory message
    if board == correct_board:
        # We will add this feature later.
        show_victory_plate()


c.bind('<Button-1>', click)
c.pack()


board = list(range(1, EMPTY_SQUARE + 1))
correct_board = board[:]
shuffle(board)

while not is_solvable():
    shuffle(board)

draw_board()
root.mainloop()