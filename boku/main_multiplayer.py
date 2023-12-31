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


def play_game_multiuser_v2():
    """
    Player have to capture after a capture move
    """

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
    game_over = False
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
                    
                    # Restart
                    if graphics.is_point_inside_rect(mouse_x, mouse_y, restart_button_rect):
                        print("[DEBUG]-[main]-Restart button clicked")  # Perform restart action here
                        board_variables = BoardVariables()
                        board_geometry = BoardGeometry(board_variables)
                        game_logics = GameLogics(board_variables, board_geometry)
                        graphics = Graphics(screen, board_variables)
                        player = "p1" # always restart to player 1
                        game_over = False
                        # Calculate the maximum scrolling range
                        max_scroll = max(0, len(game_logics.history_text) * text_line_space - 600)
                        scrolling_offset = max_scroll
                        
                    # Undo
                    elif graphics.is_point_inside_rect(mouse_x, mouse_y, undo_button_rect):
                        if len(game_logics.events) > 0:
                            player = game_logics.undo_events()
                        else:
                            print("[DEBUG]-[Undo_events]- No events to undo...")
                            game_logics.history_text.append(f"No events to undo.")
                            # Calculate the maximum scrolling range
                            max_scroll = max(0, len(game_logics.history_text) * text_line_space - 600)
                            scrolling_offset = max_scroll
                    # Redo
                    elif graphics.is_point_inside_rect(mouse_x, mouse_y, redo_button_rect):
                        if len(game_logics.events_redo) > 0:
                            player = game_logics.redo_events()
                        else:
                            print("[DEBUG]-[Undo_events]- No events to redo...")
                            game_logics.history_text.append(f"No events to redo.")
                            # Calculate the maximum scrolling range
                            max_scroll = max(0, len(game_logics.history_text) * text_line_space - 600)
                            scrolling_offset = max_scroll
                    
                    # Game Steps
                    else: 
                        if clicked_hex_name and not(game_over): # if user actually clicks on a hex
                            
                            game_over, player, _ = game_logics.play_user(clicked_hex_name, player)
                            print(f"[DEBUG]-[main]-[play_user]-HEX_GRID_FLAT_MAP[0]: ")
                            pprint(board_variables.HEX_GRID_FLAT_MAP[0])
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
        if not game_over:
                
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
            graphics.draw_circle((800,70), player)
            if len(game_logics.detected_capture_moves) >0:
                graphics.highlight_capture_moves(game_logics.detected_capture_moves)
                # in capture mode retain existing player 
                # as player has been flipped , flip again
                graphics.draw_circle((800,70), game_logics.get_opponent_player(player))
            graphics.create_hist_box(game_logics.history_text, (800,160), scrolling_offset, max_scroll)
        else: # game over
            # Create a font for text
            game_over_font = pygame.font.Font(None, 60)
            # as always a move leads to win and move changes player, to get the player reverse again
            oppn_player = game_logics.get_opponent_player(player)
            game_over_text = game_over_font.render(f"Game Over!!,\n {oppn_player} is winner.", True, (0,0,0))        
            screen.blit(game_over_text, (board_variables.WIDTH // 2 - 200, board_variables.HEIGHT // 2 - 100))
        pygame.display.flip()
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    play_game_multiuser_v2()