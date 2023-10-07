import pygame
import sys
import math
import numpy as np
from pprint import pprint
import time
from init import (WIDTH, HEIGHT, HEX_SIZE, BG_COLOR, 
                  HEX_COLOR, HEX_WIDTH, FONT_SIZE, LABEL_COLOR, 
                  boku_rule_cont_pos, PLAYERS, HEX_GRID_CORDS, 
                  HEX_GRID_FLAT_MAP, TRAP_PATTERN
)
from geometry import find_hex_center_near_mouse_click, flat_map_gird

def draw_hexagon(hex_points: list[float], label: str, cords_label: bool = False):
    """
    Input: hex_points=[q, r, x_center, y_center, v1, v2, v3, v4, v5, v6]
    takes the hex points and draws a hex on screen
    """
    if cords_label:
        # get the center co-ordinates
        q,r = hex_points[0], hex_points[1]
        s = -q -r 
        label_points = f": {(q,r,s)}"
        label = label + label_points

    x_center, y_center = hex_points[2], hex_points[3]
    vertices = hex_points[4:]
    assert len(vertices) ==6, "[Debug] hex points are incorrect"

    pygame.draw.polygon(screen, HEX_COLOR, vertices, HEX_WIDTH)
    # create a font object
    font = pygame.font.Font(None, FONT_SIZE)
    # create a text surface with anti aliased text
    text_surface = font.render(label, True, LABEL_COLOR)
    # get the rectangle of the text surface
    text_rect = text_surface.get_rect()
    text_rect.center = pygame.Vector2((x_center, y_center))#[0], center_cordinates[1])
    # blit, copy the text surface on to the screen
    screen.blit(text_surface, text_rect)
 
def draw_circle(circle_info):
    center_cords = circle_info[0]
    circle_player = circle_info[1]
    player_color = PLAYERS[circle_player]["color"]
    border_color = (128, 104, 73)
    border_width = 5
    radius = int(0.7 * HEX_SIZE) # 70 % of hex radius

    pygame.draw.circle(screen, player_color, center_cords, radius)
    pygame.draw.circle(screen, border_color, center_cords, radius, border_width)

def create_hist_box(hist_stat: list, pos : tuple[int,int], scrolling_offset, max_scroll):
    """
    draws history box in the right side of the window
    """
    # declare variables
    # Define colors
    text_color = (247, 229, 205)
    text_box_color = (0, 0, 0)
    scrollbar_color = (150, 150, 150)
    scrollbar_button_color = (100, 100, 100)
    text_line_space = 30
    box_height, box_width = 600, 350
    
    pos_x, pos_y = pos
    # Create a rectangle for the text box
    text_box_rect = pygame.Rect(pos_x, pos_y, box_width, box_height)
    # Create a surface for the text box
    text_box_surface = pygame.Surface((text_box_rect.width, text_box_rect.height))
    text_box_surface.fill(text_box_color)

    # Create a rectangle for the scrollbar
    scrollbar_rect = pygame.Rect(pos_x + box_width - 20, pos_y, 10, box_height)
    scrollbar_button_rect = pygame.Rect(pos_x + box_width - 20, pos_y, 10, 20)
    
    # Create a font for the text
    font = pygame.font.Font(None, 24)
    # Render and display text lines within the text box
    y = 0
    for line in hist_stat:
        text = font.render(line, True, text_color)
        if y - scrolling_offset > text_box_rect.height:
            break
        text_box_surface.blit(text, (20, y - scrolling_offset))
        y += text_line_space

    screen.blit(text_box_surface, text_box_rect.topleft)

    # Draw the scrollbar
    pygame.draw.rect(screen, scrollbar_color, scrollbar_rect)
    # Calculate the position of the scrollbar button based on scrolling offset and max_scroll
    if max_scroll != 0:
        scrollbar_button_rect.top = 10 + (scrolling_offset / max_scroll) * (text_box_rect.height - 50)
    pygame.draw.rect(screen, scrollbar_button_color, scrollbar_button_rect)


# def check_contiguous_players(grid_flat_map, player, n):

#     rows, cols = len(grid_flat_map), len(grid_flat_map[0])
#     grid_flat_map = np.array(grid_flat_map)

#     # check for contiguos elements in rows
#     for row in grid_flat_map:
#         for i in range (cols - n + 1):
#             if all(row[i:i+n] == player):
#                 return True  

#     # check for contiguos elements in cols
#     for col in grid_flat_map.T:
#         for i in range (rows - n + 1):
#             if all(col[i:i+n] == player):
#                 return True 
#     # check for contiguos elements in anti-diagonals
    
#     for i in range (rows - n + 1):
#         for j in range(cols - n + 1):
#             anti_diagonal = np.fliplr(grid_flat_map[i:i+n, j:j+n]).diagonal()
#             if all(anti_diagonal == player): 
#                 return True 

# def test_check_contiguous_players(grid_flat_map, player, n):
#     # same function except instad of returning true or falls it return number of times such occurence happens
#     rows, cols = len(grid_flat_map), len(grid_flat_map[0])
#     grid_flat_map = np.array(grid_flat_map)

#     occurence = 0
#     # check for contiguos elements in rows
#     for row in grid_flat_map:
#         # print(f"[Debug]- row - {row}")
#         for i in range (cols - n + 1):
#             # print(f"[Debug]- row segments - {row[i:i+n]}, occurance- {occurence}")
#             if all(row[i:i+n] == player):
#                 occurence +=1 

#     # check for contiguos elements in cols
#     for col in grid_flat_map.T:
#         for i in range (rows - n + 1):
#             if all(col[i:i+n] == player):
#                 occurence +=1 
#     # check for contiguos elements in anti-diagonals
    
#     for i in range (rows - n + 1):
#         for j in range(cols - n + 1):
#             anti_diagonal = np.fliplr(grid_flat_map[i:i+n, j:j+n]).diagonal()
#             if all(anti_diagonal == player):
#                 occurence +=1 
    
#     return occurence

def check_board(grid_flat_map, player, n) -> tuple[bool, list]:
    """
    Check board for->
    1. 5 contigous tokens in same line
    2. trap condition
    """
    rows, cols = len(grid_flat_map), len(grid_flat_map[0])
    grid_flat_map = np.array(grid_flat_map)

    detect_traps = []
    # iterating over r
    # check for contiguos elements in rows
    for row_i, row in enumerate(grid_flat_map):
        for i in range (cols - n + 1):
            if all(row[i:i+n] == player):
                return True, detect_traps
            if list(row[i:i+4]) in TRAP_PATTERN:
                detect_trap = [[row_i,i] for i in range(i,i+4)]
                detect_traps.append(detect_trap)
        # since n=5 i will stop 1 before so add one more check for i+1: i+1+5
        if list(row[i+1:i+1+4]) in TRAP_PATTERN:
                detect_trap = [[row_i,i] for i in range(i+1,i+1+4)]
                detect_traps.append(detect_trap)
    
    # iterating over q
    # check for contiguos elements in cols
    for col_i, col in enumerate(grid_flat_map.T):
        for i in range (rows - n + 1):
            if all(col[i:i+n] == player):
                return True, detect_traps
            if list(col[i:i+4]) in TRAP_PATTERN:
                detect_trap = [[i, col_i] for i in range(i,i+4)]
                detect_traps.append(detect_trap)
        # since n=5 i will stop 1 before so add one more check for i+1: i+1+5
        if list(col[i+1:i+1+4]) in TRAP_PATTERN:
                detect_trap = [[i, col_i] for i in range(i+1,i+1+4)]
                detect_traps.append(detect_trap)

    # check for contiguos elements in anti-diagonals
    for i in range (rows - n + 1):
        for j in range(cols - n + 1):
            anti_diagonal = np.fliplr(grid_flat_map[i:i+n, j:j+n]).diagonal()
            if all(anti_diagonal == player):
                return True, detect_traps
            
            # check for trap pattern
            anti_diagonal = np.fliplr(grid_flat_map[i:i+4, j:j+4]).diagonal()
            if list(anti_diagonal) in TRAP_PATTERN:
                # Pattern matched; now find the original indices
                detect_trap = [[i + k, j + 4 - k - 1] for k in range(4)]
                detect_traps.append(detect_trap)
                
        # additional j+1 case because n=5 and trap_size=4
        anti_diagonal = np.fliplr(grid_flat_map[i:i+4, j+1:j+1+4]).diagonal()
        if list(anti_diagonal) in TRAP_PATTERN:
            # Pattern matched; now find the original indices
            detect_trap = [[i + k, j + 1 + 4 - k - 1] for k in range(4)]
            detect_traps.append(detect_trap)
            
    # consider one more case with i+1 and iterate over all j
    for j in range(cols - 4 + 1):
        anti_diagonal = np.fliplr(grid_flat_map[i+1:i+1+4, j:j+4]).diagonal()
        if list(anti_diagonal) in TRAP_PATTERN:
            # Pattern matched; now find the original indices
            detect_trap = [[i+1 + k, j + 4 - k - 1] for k in range(4)]
            detect_traps.append(detect_trap)

    return False, detect_traps
            
def make_move(pos: str, player: str, tokens: list):
    """
    Takes hex_name as player position and adds player symbol in the flat-map-grid
    """
    shifted_q, shifted_r = flat_map_gird(pos)
    HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r] = PLAYERS[player]['symbol']
    # print("[DEBUG]- [make_move]- HEX_GRID_FLAT_MAP[0]\n")
    # pprint(HEX_GRID_FLAT_MAP[0])
    # print("(hex_center_x, hex_center_y)", (HEX_GRID_CORDS[pos][1], HEX_GRID_CORDS[pos][2]))
    # (hex_center_x, hex_center_y) = HEX_GRID_CORDS[pos][2], HEX_GRID_CORDS[pos][3] 

def check_valid_move(
        clicked_hex_name: str, 
        player: str, 
        player_captured_last: dict[str: tuple[int, int]],
        ) -> bool:
    """
    For a player check if the particular position is valid or not
    If its an empty position check if the player was captured in the same position in the last turn
    """
    shifted_q, shifted_r = flat_map_gird(clicked_hex_name)
    pos_in_map = HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r]
    
    # player was captured from this position in the last turn
    player_captured_last[player]
    # print("[DEBUG]- [check_valid_move]- player_captured_last", player_captured_last)
    # check if the board is empty 
    # and check if the player was captured from that pos in the previous turn
    if ((pos_in_map == -1) and ([shifted_q, shifted_r] != player_captured_last[player])): 
        return True
    return False

def detect_capture_move(clicked_hex_name: str, detected_traps: list):
    """
    checks if a particular move leads to a capture situation
    """
    detected_capture_moves = []
    shifted_q, shifted_r = flat_map_gird(clicked_hex_name)
    
    # check if the current move is part of any of the two ends of a trap pattern
    for trap in detected_traps:
        if [shifted_q, shifted_r] in [trap[0],trap[3]]: 
            detected_capture_moves.append(trap[1:3])
    return detected_capture_moves

def capture_move(
        clicked_hex_name: str, 
        player: str, 
        detected_capture_moves: list, 
        player_captured_last: dict[str: tuple[int, int]],
        history_text: list[str],
        ):
    
    shifted_q, shifted_r = flat_map_gird(clicked_hex_name)
    # pos_in_flatmap = HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r]
    oppn_player = list(set(PLAYERS.keys()) - set([player]))[0]
    # Since the player has already been switched so player holds the opponent player 
    # TODO: check if cheking of opponent trapped in between is needed or not
    # opponent_trap_windows = [trap_window[1:3] for trap_window in detected_capture_moves if trap_window[0] != PLAYERS[player]['symbol']]
    for trap_window in detected_capture_moves:
        if [shifted_q, shifted_r] in trap_window:
            HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r] = -1 # empty captured position
            # add captured move to illegal psotions for the next move
            player_captured_last[player] = [shifted_q,shifted_r] # make the position

            history_text.append(f"Player - {oppn_player} captures - {clicked_hex_name}")
    # print("[DEBUG]- [capture_move]- HEX_GRID_FLAT_MAP[0]\n")
    # pprint(HEX_GRID_FLAT_MAP[0])
    print("[DEBUG]- [capture_move]- player_captured_last", player_captured_last)
    
def draw_player_tokens():
    """
    draws circles for tokens in flatmap grid
    """
    tokens = []
    n_rows, n_cols = len(HEX_GRID_FLAT_MAP[0]), len(HEX_GRID_FLAT_MAP[0][0])
    for r in range(n_rows):
        for c in range(n_cols):
            if HEX_GRID_FLAT_MAP[0][r][c] in [0,1]: # check if the board has a token 
                if HEX_GRID_FLAT_MAP[1][r][c]: # not None invalid positions
                    # get the center of the hexagon 
                    (hex_center_x, hex_center_y) = HEX_GRID_FLAT_MAP[1][r][c][2], HEX_GRID_FLAT_MAP[1][r][c][3] 
                    if HEX_GRID_FLAT_MAP[0][r][c]==1:
                        player="p1"
                    else:
                        player="p2"
                    draw_circle([(hex_center_x, hex_center_y), player])

def draw_player_turn(center_cords, player):
    
    c1_player = player
    # c1_color = PLAYERS[c1_player]["color"]
    c1_color = (247, 229, 205, 100) #(10, 21, 23)
    c1_border_color = (128, 104, 73, 100)
    border_width = 5
    radius = int(0.7 * HEX_SIZE) # 70 % of hex radius
    c1_x, c1_y = center_cords[0] + radius, center_cords[1] + radius
    # Create a surface for the circle
    circle_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, c1_color, center_cords, radius)
    pygame.draw.circle(circle_surface, c1_border_color, center_cords, radius, border_width)
    screen.blit(circle_surface, (center_cords[0],center_cords[1]))

def highlight_capture_moves(detected_capture_moves):
    
    highlight_color = 247, 62, 102
    highlight_hex_width = HEX_WIDTH + 6
    # detected_capture_moves = [[[5, 4], [5, 5]], [[4, 6], [4, 5]]]
    # flat_capture_moves = [[5, 4], [5, 5], [4, 6], [4, 5]]
    detected_capture_moves_np = np.array(detected_capture_moves)
    flat_capture_moves = detected_capture_moves_np.reshape(-1, detected_capture_moves_np.shape[-1])
    # get all the poins of interest from the
    detected_hex_points = [HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][2:] for [shifted_q, shifted_r] in flat_capture_moves]
    for hex_points in detected_hex_points:
        # x_center, y_center = hex_points[1], hex_points[1]
        vertices = hex_points[2:]
        assert len(vertices) ==6, "[Debug] hex points are incorrect"
        pygame.draw.polygon(screen, highlight_color, vertices, highlight_hex_width)
            

def play_game_multiuser():
    # Initialize Pygame
    pygame.init()
    global screen
    # Create the Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boku")
    clock = pygame.time.Clock()

    tokens = []   
    # start with player p1
    player = "p1"

    player_captured_last ={
        'p1': None,
        'p2': None,
    }
    detected_traps = []
    detected_capture_moves = []
    text_line_space = 30
    # Calculate the maximum scrolling range
    max_scroll = 0
    scrolling_offset = 0
    history_text = [f"Game Starts!! Starting Player Turn- {player}"]
    running = True
    while running:
        # check for quit by user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button ==1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # find the hex that was clicked
                    clicked_hex_name = find_hex_center_near_mouse_click(mouse_x, mouse_y)
                    print("#"*30)
                    print(f"[DEBUG]-[main]-mouse position- {mouse_x, mouse_y}, clicked_hex- {clicked_hex_name}")
                    print(f"flat_pos- {(HEX_GRID_CORDS[clicked_hex_name][0]+5, HEX_GRID_CORDS[clicked_hex_name][1]+4)}")
                    if clicked_hex_name: # if user actually clicks on a hex
                        if not(len(detected_capture_moves) > 0): # game in normal flow
                        
                            print(f"[DEBUG]-[main]- game in - Normal Flow")
                            # check if the move is vald or not
                            if check_valid_move(clicked_hex_name, player, player_captured_last):
                                # make move on the flat_board
                                make_move(clicked_hex_name, player, tokens)
                                history_text.append(f"{player} moves to - {clicked_hex_name}") 
                                # Check the board if game is over and get trap positions
                                game_over, detected_traps =  check_board(
                                    HEX_GRID_FLAT_MAP[0], 
                                    PLAYERS[player]['symbol'], 
                                    boku_rule_cont_pos
                                    )
                                print(f"[DEBUG]-[main]-[normal_flow] detected_traps.")
                                print(f"total traps - {len(detected_traps)}\n")
                                pprint(detected_traps)
                                
                                # check if current move can lead to a capture
                                # for inital few turns- detected_traps=[], detected_capture_moves=[]
                                detected_capture_moves = detect_capture_move(clicked_hex_name, detected_traps)
                                if (len(detected_capture_moves) > 0):
                                    print(f"[DEBUG]-[main]- detected_capture_moves are - ")
                                    pprint(detected_capture_moves)
                                    print(f"[DEBUG]-[main]- Entering - Capture Mode")
                                    # history_text.append(f"Entering - Capture Mode")
                                # refresh any illegal move due to capture in prev turn
                                player_captured_last ={
                                    'p1': None,
                                    'p2': None,
                                }
                                if game_over:
                                    print(f"[DEBUG]-[play_game_multiuser]-game over winner- {player}")
                                    history_text.append(f"Game Over !! Winner- {player}")
                                    # break
                                # switch player
                                if player == "p1":
                                    player = "p2"
                                else:
                                    player = "p1"
                            else:
                                print("[DEBUG]-[main]- [check_valid_move]- Invalid Move!")
                                history_text.append(f"Invalid Move!")
                        else: # game in capture flow
                            print(f"[DEBUG]-[main]- game in - Capture Mode")
                            capture_move(
                                clicked_hex_name, 
                                player, 
                                detected_capture_moves, 
                                player_captured_last,
                                history_text,
                                )
                            # empty the detected capture moves so that each turn it will check 
                            detected_capture_moves = []
                            print(f"[DEBUG]-[main]- Exiting - Capture Mode")
                            # click anywhere else in the board to not capture
                            

                        # Calculate the maximum scrolling range
                        max_scroll = max(0, len(history_text) * text_line_space - 600)
                        scrolling_offset = max_scroll

                    else:
                        print("[DEBUG]-[main]-[clicked_hex_name]- Invalid Move!")
                        history_text.append(f"Invalid Move!")
                if event.button == 4:  # Scroll up
                    scrolling_offset = max(0, scrolling_offset - 20)
                elif event.button == 5:  # Scroll down
                    scrolling_offset = min(max_scroll, scrolling_offset + 20)

        # display blank screen
        screen.fill(BG_COLOR)
        # Draw board and player tokens
        # draw the hexagonal grid
        for hex_name, hex_points in HEX_GRID_CORDS.items():
            draw_hexagon(hex_points,hex_name)
        
        draw_player_tokens()
        # indicate player turn
        draw_circle([(800,70), player])
        if len(detected_capture_moves) >0:
            highlight_capture_moves(detected_capture_moves)
        
        create_hist_box(history_text, (800,150), scrolling_offset, max_scroll)
        pygame.display.flip()
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    play_game_multiuser()