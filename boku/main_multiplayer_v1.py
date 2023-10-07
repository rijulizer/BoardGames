import pygame
import sys
import math
import numpy as np
from pprint import pprint
import time

from init import BoardVariables
from geometry import BoardGeometry
from game_logics import GameLogics
from graphics import Graphics
def play_game_multiuser():
    board_variables = BoardVariables()
    board_geometry = BoardGeometry(board_variables)
    game_logics = GameLogics(board_variables, board_geometry)

    # Initialize Pygame
    pygame.init()
    global screen
    # Create the Pygame window
    screen = pygame.display.set_mode((board_variables.WIDTH, board_variables.HEIGHT))
    pygame.display.set_caption("Boku")
    clock = pygame.time.Clock()

    graphics = Graphics(screen, board_variables)

    player = "p1" # start with player p1
    player_captured_last ={
        'p1': None,
        'p2': None,
    }
    detected_traps = []
    detected_capture_moves = []
    # variables for history box
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
                    clicked_hex_name = board_geometry.find_hex_center_near_mouse_click(mouse_x, mouse_y)
                    print("#"*30)
                    print(f"[DEBUG]-[main]-mouse position- {mouse_x, mouse_y}, clicked_hex- {clicked_hex_name}")
                    print(f"""flat_pos- {(board_variables.HEX_GRID_CORDS[clicked_hex_name][0]+5,
                                        board_variables.HEX_GRID_CORDS[clicked_hex_name][1]+4)}""")
                    if clicked_hex_name: # if user actually clicks on a hex
                        if not(len(detected_capture_moves) > 0): # game in normal flow
                        
                            print(f"[DEBUG]-[main]- game in - Normal Flow")
                            # check if the move is vald or not
                            if game_logics.check_valid_move(clicked_hex_name, player, player_captured_last):
                                # make move on the flat_board
                                game_logics.make_move(clicked_hex_name, player)
                                history_text.append(f"{player} moves to - {clicked_hex_name}") 
                                # Check the board if game is over and get trap positions
                                game_over, detected_traps =  game_logics.check_board(player)
                                print(f"[DEBUG]-[main]-[normal_flow] detected_traps.")
                                print(f"total traps - {len(detected_traps)}\n")
                                pprint(detected_traps)
                                
                                # check if current move can lead to a capture
                                # for inital few turns- detected_traps=[], detected_capture_moves=[]
                                detected_capture_moves = game_logics.detect_capture_move(clicked_hex_name, detected_traps)
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
                            game_logics.capture_move(
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
        screen.fill(board_variables.BG_COLOR)
        # Draw board and player tokens
        # draw the hexagonal grid
        for hex_name, hex_points in board_variables.HEX_GRID_CORDS.items():
            graphics.draw_hexagon(hex_points,hex_name)
        
        # draw a player whenver player clicks on the board
        graphics.draw_player_tokens()
        
        # indicate player turn
        graphics.draw_circle([(800,70), player])
        if len(detected_capture_moves) >0:
            graphics.highlight_capture_moves(detected_capture_moves)
        
        graphics.create_hist_box(history_text, (800,150), scrolling_offset, max_scroll)
        pygame.display.flip()
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    play_game_multiuser()