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
        player: players turn
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
    
    def play_random_agent(self, player):
        
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
        oppn_player = self.game_logics.get_opponent_player(player)
        
        # check if the normal move leads to a capture move
        if (len(self.game_logics.detected_capture_moves) > 0): # game in capture flow
            # generate valid capture moves
            self.get_valid_moves(player)
            # randomly select one capture move
            rand_indexes = np.random.choice(self.avilable_moves.shape[0])
            shifted_q, shifted_r = self.avilable_moves[rand_indexes]
            # get the eqivalent hex name
            clicked_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
            print(f"[DEBUG]-[main]- game in - Capture Mode")
            self.game_logics.capture_move_v2(
                clicked_hex_name, 
                oppn_player,
                )
            # empty the detected capture moves so that each turn it will check 
            self.game_logics.detected_capture_moves = []
            print(f"[DEBUG]-[main]- Exiting - Capture Mode")
            # click anywhere else in the board to not capture
        
    
        return game_over, oppn_player
#################################################################
# class AgentMiniMax(Agent):
#     def __init__(self, game_variables, game_logics,):
#         super().__init__(game_variables, game_logics)
    
#     def get_token_count_diff(self, player):
#         """
#         counts the differnece of number of players in the board
#         """
#         oppn_player = self.game_logics.get_opponent_player(player)
#         player_count = np.count_nonzero(self.variables.HEX_GRID_FLAT_MAP[0]
#                   == self.variables.PLAYERS[player]["symbol"])
#         oppn_player_count = np.count_nonzero(self.variables.HEX_GRID_FLAT_MAP[0]
#                   == self.variables.PLAYERS[oppn_player]["symbol"])
#         # count diff values are like - +1, +2, -1, -2 
#         # more the count_differnece better the value
#         count_diff =  int(player_count - oppn_player_count)
#         return count_diff

#     def static_eval(self, player):
#         """
#         Static evaluation function 
#         """
#         hex_name = None
#         token_count_diff = self.get_token_count_diff(player)
#         pos_value = self.variables.board_pos_values[hex_name]
    
#     def minimax_ab():
#         pass
    
#     # def play_agent():
#     # for all available moves
#         # make_move
#         # get score = minimax()
#         # find out the best score and moev
#     # return best move
#     def agent_make_move(self, select_hex_name, player):
#         """
#         Agent plays either in normal flow or in capture flow
#         """
#         # Normal Flow of Game (capture not detected)
#         if not(len(self.game_logics.detected_capture_moves) > 0): 
#             # make move on the flat_board
#             self.game_logics.make_move(select_hex_name, player)
#             # Check the board if game is over and get trap positions
#             game_over, detected_traps =  self.game_logics.check_board(player)
#             # check if current move can lead to a capture
#             self.game_logics.detect_capture_move(select_hex_name, player, detected_traps)
#             # in normal move, refresh any illegal move due to capture in prev turn
#             self.game_logics.reset_last_captured()
#         # check if the normal move leads to a capture move
#         if (len(self.game_logics.detected_capture_moves) > 0): # game in capture flow
#             self.game_logics.capture_move_v2(
#                 select_hex_name, 
#                 player,
#                 )
#             # empty the detected capture moves so that each turn it will check 
#             self.game_logics.detected_capture_moves = []
            
            

#     def play_agent(self, player):
#         """
#         parent function that makes agent make the final move
#         """
#         # agent player
#         game_over = False # default declaration
#         # generate valid moves before each move
#         self.get_valid_moves(player)
#         min_score = + np.inf

#         # iterate through all available moves
#         for move_index in range(self.avilable_moves.shape[0]):
#             shifted_q, shifted_r = self.avilable_moves[move_index]
#             # get the eqivalent hex name
#             select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
#             self.agent_make_move(self, select_hex_name, player)
            
#             score = self.minimax_ab(select_hex_name, player)
#             if score < min_score:
#                 min_score = score
#                 best_hex = select_hex_name
#         # make the final move
#         self.agent_make_move(self, best_hex, player)
#         return game_over, player

# def minimax(board: dict, depth: int, is_maximizing_player: bool):
#     # check for terminal states in the recursion function
#     game_over, winner = check_terminal(board)
#     if depth == 0 or game_over:
#         # print(f"\n[Debug]-depth- {depth}, finsihed")# max_player- score: {score}, max_score :{max_score}")
#         # print("\n[Debug]-depth- {depth}, min_player- score: {score}, min_score :{min_score}")
#         if winner == 'X':
#             return 10+ 10*(depth) 
#         elif winner == "O":
#             return -(10 + 10*(depth))
#         else:
#             # draw scenario
#             return 0
        
#     if is_maximizing_player:
#         max_score = -1000000 # -np.inf
        
#         # find empty spaces
#         for i in board.keys():
#             if board[i] == ' ':
#                 board[i] = 'X'
#                 score = minimax(board, depth-1, False)
#                 board[i] = ' '
                
#                 max_score = max(score, max_score)
#         return max_score
    
#     else:
#         min_score = +1000000 #+np.inf
#         # find empty spaces
#         for i in board.keys():
#             if board[i] == ' ':
#                 board[i] = 'O'
#                 score = minimax(board, depth-1, True)
#                 board[i] = ' '
#                 min_score = min(score, min_score)
                
#         return min_score
    



if __name__ == "__main__":
    board_variables = BoardVariables()
    board_geometry = BoardGeometry(board_variables)
    game_logics = GameLogics(board_variables, board_geometry)
    agent = Agent(board_variables, game_logics,)

