import random
from typing import Tuple, List
import pygame
from cell import Cell


class GameBoard:
    pygame.font.init()
    font_path = pygame.font.match_font("ArialRounded")
    arial = pygame.font.Font(font_path, 18)

    def __init__(self, cells_x: int, cells_y: int, bombs: int, cell_size: int):
        """ This class represents a minesweeper game board.
        As a public property, Gameboard provides `board` a 2-d matrix containing all the cells on the board.
        each :class:`Cell`

        :param cells_x: the number of columns on the board
        :param cells_y: the number of rows on the board
        :param bombs: the number of bombs on the board
        :param cell_size: the size of each side of a cell
        :returns: GameBoard
        """

        self.cell_size = cell_size
        '''the size of each cell as shown on screen'''

        self.num_cells_x: int = cells_x
        '''the number of cells in the x-axis of the game board'''

        self.num_cells_y: int = cells_y
        '''the number of cells in the y-axis of the game board'''

        self.num_mines: int = bombs
        '''the total number of mines on the board'''

        # 2-d list of Cells. Each cell has a unique event, clicked_event
        self.cell_matrix: List[List[Cell | None]] = [[None for _ in range(self.num_cells_x)]
                                                     for _ in range(self.num_cells_y)]
        '''a 2-d list containing all the cells in on the board'''

        self._seed_mines()
        for row in self.cell_matrix:
            for cell in row:
                _ = cell.get_adjacency(self.cell_matrix)

    def _seed_mines(self):
        rand = random.Random()

        # track how many mines have been seeded
        left_to_seed = self.num_mines

        # populate game board with Cells.
        for row in range(self.num_cells_y):
            for col in range(self.num_cells_x):

                # cell creation
                click_event = pygame.event.custom_type()
                location: Tuple[int, int] = (row * self.cell_size, col * self.cell_size)
                self.cell_matrix[row][col] = Cell(location, click_event, 0, "#777777", self.cell_size)

        # populate mines based on required number of mines
        while left_to_seed > 0:
            x = rand.randint(0, self.num_cells_x - 1)
            y = rand.randint(0, self.num_cells_y - 1)
            self.cell_matrix[y][x].value = -1
            left_to_seed -= 1

    def reveal_mines(self, screen: pygame.Surface):
        """Show all the mines on the board

        :param screen: the main game display
        """

        font_path = pygame.font.match_font("ArialRounded")
        arial = pygame.font.Font(font_path, 18)

        # traverse the 2-d list of cells checking for bombs.
        # -1 == bomb, 0 == no bomb
        for row in range(self.num_cells_x):
            for col in range(self.num_cells_y):
                current_cell = self.cell_matrix[row][col]

                if current_cell.value == -1:
                    pygame.draw.rect(screen, "red", (
                        current_cell.location[0], current_cell.location[-1], self.cell_size,
                        self.cell_size))
                else:
                    pygame.draw.rect(screen, "grey", (current_cell.location[0],
                                                      current_cell.location[-1],
                                                      self.cell_size,
                                                      self.cell_size))

                pygame.draw.rect(screen, "black", (current_cell.location[0],
                                                   current_cell.location[-1],
                                                   self.cell_size,
                                                   self.cell_size), 2)

                screen.blit(arial.render(f"{current_cell.value}", False, "#876af4"),
                            (current_cell.location[0] + int(self.cell_size // 2),
                             current_cell.location[1] + int(self.cell_size // 2)))

    def draw_board(self, screen: pygame.Surface):
        blitzs = []
        for row in range(self.num_cells_y):
            for col in range(self.num_cells_x):
                current_cell = self.cell_matrix[row][col]
                blitzs.append((current_cell.cell_surface, current_cell.location))

        screen.blits(blitzs)

    # stopped here.
    def zero_clicked(self, current_cell: Cell):

        # get_adjacency populates this cells adjacency list and determines value.
        current_cell.get_adjacency(self.cell_matrix)

        # start recursion with copy of adjacency list
        neighbors = current_cell.adjacent_list.copy()
        self._search_for_zeros(neighbors)

    def _search_for_zeros(self, neighbors: List[Cell]):
        if len(neighbors) > 0:
            current = neighbors.pop(0)
            if current.value == 0 and not current.visited:
                current.visited = True
                current.get_adjacency(self.cell_matrix)
                neighbors.extend(current.adjacent_list)
                _render_zero_cell(current)
                for cell in current.adjacent_list:
                    _render_zero_cell(cell)
            return self._search_for_zeros(neighbors)
        return


def _render_zero_cell(current: Cell):
    current.cell_surface.fill("#444444")
    rendered_text = GameBoard.arial.render(f"{current.value}", False, "#876af4")
    current.cell_surface.blit(rendered_text,
                              (rendered_text.get_width() // 4,
                               rendered_text.get_height() // 3))
