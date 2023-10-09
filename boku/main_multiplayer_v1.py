import pygame
import pygame_menu
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

    restart_button_rect = pygame.Rect(900, 40, 150, 50)  # Define the restart button's position and size
    undo_button_rect = pygame.Rect(850, 100, 30, 30)
    redo_button_rect = pygame.Rect(1070, 100, 30, 30)
    
    graphics = Graphics(screen, board_variables)

    player = "p1" # start with player p1
    
    detected_traps = []
    # variables for history box
    text_line_space = 30
    # Calculate the maximum scrolling range
    max_scroll = 0
    scrolling_offset = 0
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
                    # print(f"[DEBUG]-[main]-mouse position- {mouse_x, mouse_y}, clicked_hex- {clicked_hex_name}")
                    # print(f"""flat_pos- {(board_variables.HEX_GRID_CORDS[clicked_hex_name][0]+5,
                    # board_variables.HEX_GRID_CORDS[clicked_hex_name][1]+4)}""")
                    
                    # restart
                    if graphics.is_point_inside_rect(mouse_x, mouse_y, restart_button_rect):
                        print("[DEBUG]-[main]-Restart button clicked")  # Perform restart action here
                        board_variables = BoardVariables()
                        board_geometry = BoardGeometry(board_variables)
                        game_logics = GameLogics(board_variables, board_geometry)
                        graphics = Graphics(screen, board_variables)
                        player = "p1" # always restart to player 1
                        
                    # Undo
                    elif graphics.is_point_inside_rect(mouse_x, mouse_y, undo_button_rect):
                        if len(game_logics.events) > 0:
                            player = game_logics.undo_events()
                        else:
                            print("[DEBUG]-[Undo_events]- No events to undo...")
                            game_logics.history_text.append(f"No events to undo.")
                    # Redo
                    elif graphics.is_point_inside_rect(mouse_x, mouse_y, redo_button_rect):
                        if len(game_logics.events_redo) > 0:
                            player = game_logics.redo_events()
                        else:
                            print("[DEBUG]-[Undo_events]- No events to redo...")
                            game_logics.history_text.append(f"No events to redo.")
                    else:
                        if clicked_hex_name: # if user actually clicks on a hex
                            if not(len(game_logics.detected_capture_moves) > 0): # game in normal flow
                            
                                print(f"[DEBUG]-[main]- game in - Normal Flow")
                                # check if the move is vald or not
                                if game_logics.check_valid_move(clicked_hex_name, player):
                                    # make move on the flat_board
                                    game_logics.make_move(clicked_hex_name, player)
                                    # Check the board if game is over and get trap positions
                                    game_over, detected_traps =  game_logics.check_board(player)
                                    # print(f"[DEBUG]-[main]-[normal_flow] detected_traps.")
                                    # print(f"total traps - {len(detected_traps)}\n")
                                    # pprint(detected_traps)
                                    
                                    # check if current move can lead to a capture
                                    # for inital few turns- detected_traps=[], detected_capture_moves=[]
                                    game_logics.detect_capture_move(clicked_hex_name, player, detected_traps)
                                    
                                    if (len(game_logics.detected_capture_moves) > 0):
                                        print(f"[DEBUG]-[main]- game_logics.detected_capture_moves are - ")
                                        pprint(game_logics.detected_capture_moves)
                                        print(f"[DEBUG]-[main]- Entering - Capture Mode")
                                        # history_text.append(f"Entering - Capture Mode")
                                    # refresh any illegal move due to capture in prev turn
                                    game_logics.reset_last_captured()
                                    if game_over:
                                        print(f"[DEBUG]-[play_game_multiuser]-game over winner- {player}")
                                        game_logics.history_text.append(f"Game Over !! Winner- {player}")
                                        # break
                                    # switch player
                                    if player == "p1":
                                        player = "p2"
                                    else:
                                        player = "p1"
                                else:
                                    print("[DEBUG]-[main]- [check_valid_move]- Invalid Move!")
                                    game_logics.history_text.append(f"Invalid Move!")
                            else: # game in capture flow
                                print(f"[DEBUG]-[main]- game in - Capture Mode")
                                game_logics.capture_move(
                                    clicked_hex_name, 
                                    player,
                                    )
                                # empty the detected capture moves so that each turn it will check 
                                game_logics.detected_capture_moves = []
                                print(f"[DEBUG]-[main]- Exiting - Capture Mode")
                                # click anywhere else in the board to not capture
                                

                            # Calculate the maximum scrolling range
                            max_scroll = max(0, len(game_logics.history_text) * text_line_space - 600)
                            scrolling_offset = max_scroll

                        else:
                            print("[DEBUG]-[main]-[clicked_hex_name]- Invalid Move!")
                            game_logics.history_text.append(f"Invalid Move!")
                if event.button == 4:  # Scroll up
                    scrolling_offset = max(0, scrolling_offset - 20)
                elif event.button == 5:  # Scroll down
                    scrolling_offset = min(max_scroll, scrolling_offset + 20)

        # display blank screen
        screen.fill(board_variables.BG_COLOR)
        # Draw the restart button
        graphics.draw_button(restart_button_rect.x, restart_button_rect.y, restart_button_rect.width, restart_button_rect.height, "Restart")
        # Draw the Undo button
        graphics.draw_button(undo_button_rect.x, undo_button_rect.y, undo_button_rect.width, undo_button_rect.height, "<")
        # Draw the Undo button
        graphics.draw_button(redo_button_rect.x, redo_button_rect.y, redo_button_rect.width, redo_button_rect.height, ">")

        # Draw board and player tokens
        # draw the hexagonal grid
        for hex_name, hex_points in board_variables.HEX_GRID_CORDS.items():
            graphics.draw_hexagon(hex_points,hex_name)
        
        # draw a player whenver player clicks on the board
        graphics.draw_player_tokens()
        
        # indicate player turn
        graphics.draw_circle([(800,70), player])
        if len(game_logics.detected_capture_moves) >0:
            graphics.highlight_capture_moves(game_logics.detected_capture_moves)
            # in capture mode retain existing player 
            # as player has been flipped , flip again
            graphics.draw_circle([(800,70), game_logics.get_opponent_player(player)])
        graphics.create_hist_box(game_logics.history_text, (800,160), scrolling_offset, max_scroll)
        pygame.display.flip()
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    play_game_multiuser()


# # Initialize Pygame Menu
# menu = pygame_menu.Menu("Menu Bar", WIDTH, 30, theme=pygame_menu.themes.THEME_DEFAULT)

# # Define menu buttons and their actions
# def rules_action():
#     print("Rules selected")

# def restart_action():
#     print("Restart selected")

# def undo_action():
#     print("Undo Last Move selected")

# menu.add_button("Rules", rules_action)
# menu.add_button("Restart", restart_action)
# menu.add_button("Undo Last Move", undo_action)

# # Main game loop
# running = True

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Clear the screen
#     screen.fill(BG_COLOR)

#     # Update and render the menu
#     menu.update(pygame.event.get())
#     menu.draw(screen)

#     pygame.display.flip()

# # Quit Pygame
# pygame.quit()
