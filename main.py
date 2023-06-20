from typing import Tuple, List
from pygame import time

import board
import cell
import pygame
from sweeper_enums import SweeperColors, SweeperFonts

pygame.init()
pygame.font.init()

# ================
# region Settings

CELL_SIZE = 40
'''the length of the side of a cell. area = CELL_SIZE ** 2'''

BOARD_SIZE_EASY = 8
BOARD_SIZE_MED = 15
BOARD_SIZE_HARD = 20

BOMBS_EASY = int((BOARD_SIZE_EASY ** 2) * 0.1)
BOMBS_MED = int((BOARD_SIZE_MED ** 2) * 0.2)
BOMBS_HARD = int((BOARD_SIZE_HARD ** 2) * 0.2)

# don't change these
EASY = 0
MED = 1
HARD = 2
CLOCK = pygame.time.Clock()

# endregion
# ================


def get_difficulty():
    """
    Instantiates a small window asking the user which difficulty the user would like to play on.

     :returns: the difficulty chosen by the user, easy, med or hard.

     - 0 = easy
     - 1 = med
     - 2 = hard
    """

    difficulty = -1
    chosen = False
    nova_font = SweeperFonts.NOVA_22.value
    bg_color = SweeperColors.POPUP_BG.value

    # not the main display, just an options window.
    popup = pygame.display.set_mode((400, 250))

    # button Rects
    choices = render_difficulty_buttons(popup)

    # loop for popup window
    while not chosen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event == pygame.K_ESCAPE:
                chosen = True
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                # handle all mouse clicks
                difficulty = difficulty_clicked(pygame.mouse.get_pos(), choices)

                # difficulty is -1 when starting the loop.
                if difficulty > -1:
                    chosen = True

        # refreshing screen
        popup.fill(SweeperColors.POPUP_BG.value)

        rendered_text = nova_font.render("Choose your difficulty", False, bg_color)
        render_difficulty_buttons(popup)
        popup.blit(rendered_text, (200 - (rendered_text.get_width() // 2), 10, 200, 100))
        pygame.display.flip()
        CLOCK.tick(60)
    return difficulty


def render_difficulty_buttons(window: pygame.Surface):
    """
    draw the radio style buttons for difficulty choices

    :param window: the popup window to draw the buttons on
    :returns: the :class:`pygame.rect.Rect` containing the button images.
    """

    # partitioning the difficulty popup into thirds for easier placement of items.
    width_thirds = window.get_width() // 3
    height_thirds = window.get_height() // 3
    font_color = SweeperColors.CELL_TEXT.value
    nova_font = SweeperFonts.NOVA_18.value

    # offset amount for aligning buttons. Before using the offset, width_thirds corresponds
    # to the right edge of a partition, the offset adjusts the location to the center of the partition
    offset_increment = width_thirds // 2

    # difficulty radio buttons
    choice_easy = pygame.draw.circle(window,
                                     font_color,
                                     (width_thirds - offset_increment, height_thirds * 2),
                                     10, 2)

    choice_med = pygame.draw.circle(window,
                                    font_color,
                                    ((width_thirds * 2) - offset_increment, height_thirds * 2),
                                    10, 2)

    choice_hard = pygame.draw.circle(window,
                                     font_color,
                                     (window.get_width() - offset_increment, height_thirds * 2),
                                     10, 2)

    # difficulty labels
    easy_text = nova_font.render("easy", True, font_color)
    medium_text = nova_font.render("medium", True, font_color)
    hard_text = nova_font.render("hard", True, font_color)

    window.blit(easy_text,
                (choice_easy.x - easy_text.get_width() // 4, choice_easy.y - 30,
                 easy_text.get_width(), easy_text.get_height()))
    window.blit(medium_text,
                (choice_med.x - easy_text.get_width() // 4, choice_med.y - 30,
                 easy_text.get_width(), easy_text.get_height()))
    window.blit(hard_text,
                (choice_hard.x - hard_text.get_width() // 4, choice_hard.y - 30,
                 hard_text.get_width(), hard_text.get_height()))

    return choice_easy, choice_med, choice_hard


def difficulty_clicked(mouse_location: Tuple[int, int], choices: Tuple[pygame.Rect, pygame.Rect, pygame.Rect]):
    """
    Called to handle clicks in the difficulty selection window.

    :param mouse_location: the x and y position of the cursor when clicked.
    :param choices: the collection of difficulty button rects.
    :return: an int indicating the chosen difficulty level

    - -1 -> no button clicked
    - \a 0 -> easy
    - \a 1 -> med
    - \a 2 -> hard
    """
    easy, med, hard = choices
    if easy.y - 10 < mouse_location[1] < easy.y + 10:
        if easy.left < mouse_location[0] < easy.right:
            return EASY
        elif med.left < mouse_location[0] < med.right:
            return MED
        elif hard.left < mouse_location[0] < hard.right:
            return HARD
    return -1


def cell_clicks(event: pygame.event.Event, mine_field: board.GameBoard, window: pygame.Surface):
    """
    handle a click event inside a :class:`board.Cell`.

    :param window: the main game board
    :param event: the click event that triggered this method.
    :param mine_field: the current game board
    :return: None
    """

    cell_index_x = event.pos[0] // CELL_SIZE
    cell_index_y = event.pos[1] // CELL_SIZE
    current_cell = mine_field.cell_matrix[cell_index_x][cell_index_y]
    if current_cell.is_flagged:
        return True
    current_cell.update(event)
    if current_cell.value > 0:
        # draw_cell_number(current_cell, window, current_cell.value)
        current_cell.render_revealed_cell()
        pygame.display.flip()
        return True
    elif current_cell.value == 0:
        mine_field.zero_clicked(current_cell)
        return True
    else:
        return False


def draw_cell_number(clicked, screen: pygame.Surface, number: int):
    """
    draw the number of adjacent mines on a cell when it is clicked

    :type clicked: cell.Cell
    :param clicked: the cell that was clicked
    :param screen: the main game display
    :param number: the number of adjacent mines to print on the cell
    :return: a new copy of the cell containing the number blitted to its Rect.
    """

    nova = SweeperFonts.NOVA_18.value
    font_color = SweeperColors.CELL_TEXT.value
    text = nova.render(f"{number}", True, font_color)
    clicked.cell_surface.blit(text, ((clicked.size // 2) - (text.get_width() // 2),
                                     clicked.size // 4))

    to_update = screen.blit(clicked.cell_surface, clicked.location)
    pygame.display.update(to_update)


def play_again():
    """
    Ask the player if they would like to play again in a popup.

    :rtype: Tuple[bool, bool]
    :return: (play again?, button clicked?)
    """

    # region -------- settings --------

    # pygame font for text rendering
    nova_font = SweeperFonts.NOVA_20.value
    text_color = SweeperColors.POPUP_TEXT.value
    bg_color = SweeperColors.POPUP_BG.value

    # not the main game window, should be released before finishing the method.
    popup = pygame.display.set_mode((500, 350))

    # for holding all the words
    rendered_text = []

    # partitioning up the screen for easier placement
    part_size_x = int(popup.get_width() // 6)
    part_size_y = int(popup.get_height() // 6)

    button_clicked = False
    again = False

    half_popup = popup.get_width() // 2
    play_again_text = nova_font.render("Would you like to play again?",
                                       False, text_color)

    half_text = play_again_text.get_width() // 2

    # endregion

    def _draw_circles():
        """
        internal method that draws the buttons on the screen

        :return: the rects for the yes and no button respectively
        """

        _yes = pygame.draw.circle(popup, text_color, (part_size_x * 2, part_size_y * 2), 10, 2)
        _no = pygame.draw.circle(popup, text_color, (part_size_x * 4, part_size_y * 2), 10, 2)
        return _yes, _no

    rendered_text.append((play_again_text, (half_popup - half_text, part_size_y * 3)))

    # region ------------ play again screen loop ------------

    while not button_clicked:
        popup.fill(bg_color)
        yes, no = _draw_circles()
        rendered_text.append((nova_font.render("yes", True, text_color),
                              (yes.x, yes.y - 40)))

        rendered_text.append((nova_font.render("no", True, text_color),
                              (no.x, no.y - 40)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_butts = pygame.mouse.get_pressed(3)
                if mouse_butts[0]:
                    again, button_clicked = again_clicked(pygame.mouse.get_pos(), [yes, no])
                    print(again, button_clicked)
        popup.blits(rendered_text)
        pygame.display.flip()

    # endregion

    # dispose of popup
    pygame.display.quit()
    return again


def again_clicked(click_position: Tuple[int, int], button_rects: List[pygame.rect.Rect]):
    """
    determine if a button was clicked on the play again screen.
    if the mouse was clicked but was not inside a button, button_clicked will be false and
    the containing loop is not yet terminated.

    :param click_position: the x, y position of the mouse cursor when it was clicked
    :param button_rects: a list of the buttons on screen
    :return: (play_again?, button_clicked?)
    """

    # button areas setup
    yes_top = button_rects[0].top
    yes_bottom = button_rects[0].bottom
    yes_right = button_rects[0].right
    yes_left = button_rects[0].left
    no_left = button_rects[-1].left
    no_right = button_rects[-1].right
    in_range_yes = yes_left < click_position[0] < yes_right
    in_range_no = no_left < click_position[0] < no_right

    # check y range then the x range on each button
    if yes_bottom > click_position[1] > yes_top:
        if in_range_yes:

            # play_again, button_clicked
            #       |      |
            return True, True

        elif in_range_no:
            return False, True
    return False, False


def flag_cell(clicked_coords: Tuple[int, int], gboard: board.GameBoard):
    x_index = int(clicked_coords[0] // CELL_SIZE)
    y_index = int(clicked_coords[1] // CELL_SIZE)

    current_cell = gboard.cell_matrix[x_index][y_index]
    current_cell.flagged()


def main():

    difficulty = get_difficulty()
    num_mines: int
    board_x: int
    board_y: int

    # determines:
    # - size of the board
    # - number of total cells
    # - number of mines on the board
    match difficulty:
        case 0:
            num_mines = BOMBS_EASY
            board_x = board_y = BOARD_SIZE_EASY
        case 1:
            num_mines = BOMBS_MED
            board_x = board_y = BOARD_SIZE_MED
        case 2:
            num_mines = BOMBS_HARD
            board_x = board_y = BOARD_SIZE_HARD
        case _:
            num_mines = int((40 ** 2) * .35)
            board_x = board_y = 40

    screen_size = (board_x * CELL_SIZE, board_y * CELL_SIZE)
    game_board = board.GameBoard(board_x, board_y, num_mines, CELL_SIZE)
    screen = pygame.display.set_mode(screen_size, 0, 32)

    running = True

    # holds the pygame custom event type associated with the cell
    cell_list = []

    # populating the custom event list
    for row in range(game_board.num_cells_y):
        for col in range(game_board.num_cells_x):
            cell_list.append(game_board.cell_matrix[row][col])

    # =====================
    #     main game loop
    # =====================

    while running:
        game_board.draw_board(screen)
        events = pygame.event.get()
        mouse_butts = pygame.mouse.get_pressed(3)
        clicked_coords = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return running
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_butts[0]:
                    running = cell_clicks(event, game_board, screen)
                elif mouse_butts[2]:
                    flag_cell(clicked_coords, game_board)

        pygame.display.flip()
        screen.fill("#aaaaaa")
        CLOCK.tick(60)

    game_board.reveal_mines(screen)
    pygame.display.flip()
    time.wait(5000)
    pygame.display.quit()
    if play_again():
        return main()
    else:
        pygame.quit()


if __name__ == "__main__":
    main()
