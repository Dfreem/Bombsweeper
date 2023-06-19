from typing import Tuple, List
import pygame

MINE = -1


class Cell:

    def __init__(self, location: Tuple[int, int], click_event: int, value: int = 0, color: str = "#777777",
                 size: int = 10):
        """
        A cell on the game-board.

        """

        self.value: int = value
        '''indicates either MINE (-1) or number of adjacent mines.'''

        self.size = size
        '''the length of the side of a cell. A cell is a square.'''

        self.location: Tuple[int, int] = location
        '''x and y position of this cell within the board matrix'''

        self.is_flagged: bool = False
        '''True if the player has set a flag on this cell'''

        self.visited = False
        '''used while traversing the graph-like structored gameboard for zeros'''

        self.click_event = click_event
        '''Custom :class:`pygame.event.Event` triggered when this cell is clicked.'''

        self.color: str = color
        '''the current color of the cell'''

        self.cell_surface = pygame.Surface((size, size))
        '''the surface of the cell in which the cell image is printed'''

        self.adjacent_list: List[Cell] = []

        self.cell_surface.fill(self.color)
        pygame.draw.rect(self.cell_surface, "black", self.cell_surface.get_rect(), 1)

    def clicked(self, event):
        """Check if the click event occurred in the position of this cell. If it did, post a new pygame event.

        :param event: the click event to compare this cells position to.
        :returns: a boolean value indicating whether the event was successfully posted.
        """

        # compensate for the size of the cell, creates a click window rather than a small point.
        cell_offset = (self.size // 2)

        # x and y range for click window == cell_offset
        if self.location[-1] - cell_offset < event.pos[1] < self.location[1] + cell_offset:
            if self.location[0] - cell_offset < event.pos[0] < self.location[0] + cell_offset:

                # custom event contains exact x and y on screen as well as row and column index within the board.
                event_dict = {
                    "x": self.location[0],
                    "y": self.location[1],
                    "row": self.location[0] // self.size,
                    "col": self.location[1] // self.size
                }
                cell_event = pygame.event.Event(self.click_event, event_dict)

                # return true if successful else false
                return pygame.event.post(cell_event)

    def get_adjacency(self, board_matrix):
        """find all the surrounding cells to this cell and add them to this cells adjacency list.
        Set this cells value to the number of adjacent mines.

        :type board_matrix: List[List[Cell]]
        :param board_matrix: the 2d-list of Cell objects representing the game board.
        :return: None
        """

        if self.value == MINE:
            return

        # a cells location is an x, y value but we want the row and column.
        this_y = (self.location[1] // self.size)
        this_x = (self.location[0] // self.size)
        adjacent_mines = 0

        # adjacent rows are last row, this row, and next row, ditto for column.
        rows = [this_y - 1, this_y, this_y + 1]
        cols = [this_x - 1, this_x, this_x + 1]

        # only check existing rows and columns
        if rows[0] < 0:
            rows = rows[1:]
        elif rows[-1] >= len(board_matrix):
            rows = rows[:-1]
        if cols[0] < 0:
            cols = cols[1:]
        elif cols[-1] >= len(board_matrix[0]):
            cols = cols[:-1]
        for row in rows:
            for col in cols:
                current = board_matrix[col][row]
                self.adjacent_list.append(current)
        for cell in self.adjacent_list:
            if cell.value == MINE:
                adjacent_mines += 1
        self.value = adjacent_mines

