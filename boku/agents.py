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

class Agent():
    """
    Random agent as base calss, randomly places tokens on th board
    """
    def __init__(self, game_variables, game_logics,):
        self.game_logics = game_logics
        self.variables = game_variables
        self.avilable_moves = np.array([])
    
    def get_valid_moves(self, player):
        """
        generates all valid moves
        """
        self.avilable_moves= self.avilable_moves.tolist()
        # normal flow of game (capture not detected)
        if not(len(self.game_logics.detected_capture_moves) > 0):
            # get all the empty sapces
            row_indices, col_indices = np.where(
                np.array(self.variables.HEX_GRID_FLAT_MAP[0])
                  == self.variables.empty_space)  
            # remove last captured move from available positions
            [q,r] = self.game_logics.player_captured_last[player]
            # Create a list of lists with the indices
            for pair in zip(row_indices, col_indices):
                if list(pair) != [q,r]:
                    # append a list to array
                    self.avilable_moves.append(list(pair))
            self.avilable_moves = np.array(self.avilable_moves)
        else: # game in capture flow
            # all the capture moves are valid moves
            self.avilable_moves = self.game_logics.detected_capture_moves
            # flatten to list of indices -
            self.avilable_moves = np.array(self.avilable_moves).reshape(-1, len(self.avilable_moves[0][0]))
        # pprint(f"[DEBUG]-[Agent]- get_valid_moves - \n {self.avilable_moves}")
           
    def play_agent(self, player):
        # agent player
        game_over = False # default declaration
        # generate valid moves
        self.get_valid_moves(player)
        # randomly select a move
        rand_indexes = np.random.choice(self.avilable_moves.shape[0])
        shifted_q, shifted_r = self.avilable_moves[rand_indexes]
        # get the eqivalent hex name
        clicked_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
        # normal flow of game (capture not detected)
        print(f"[DEBUG]-[Agent]-[play_agent]- selected_hex_name- ", clicked_hex_name)
        # Normal Flow
        if not(len(self.game_logics.detected_capture_moves) > 0):
            print(f"[DEBUG]-[Agent]-[play_agent]- Normal Flow!!")
            # make move on the flat_board
            self.game_logics.make_move(clicked_hex_name, player)
            # Check the board if game is over and get trap positions
            game_over, detected_traps =  self.game_logics.check_board(player)
            # check if current move can lead to a capture
            # for inital few turns- detected_traps=[], detected_capture_moves=[]
            self.game_logics.detect_capture_move(clicked_hex_name, player, detected_traps)

            # in normal move, refresh any illegal move due to capture in prev turn
            self.game_logics.reset_last_captured()
            if game_over:
                print(f"[DEBUG]-[play_game_multiuser]-game over winner- {player}")
                self.game_logics.history_text.append(f"[Game Over] Winner is - {player} !!")
                # break
            
            # switch player
            player = self.game_logics.get_opponent_player(player)
        
        else: # game in capture flow
            print(f"[DEBUG]-[main]- game in - Capture Mode")
            self.game_logics.capture_move_v2(
                clicked_hex_name, 
                player,
                )
            # empty the detected capture moves so that each turn it will check 
            self.game_logics.detected_capture_moves = []
            print(f"[DEBUG]-[main]- Exiting - Capture Mode")
            # click anywhere else in the board to not capture
        
        return game_over, player
    

if __name__ == "__main__":
    board_variables = BoardVariables()
    board_geometry = BoardGeometry(board_variables)
    game_logics = GameLogics(board_variables, board_geometry)
    agent = Agent(board_variables, game_logics,)

