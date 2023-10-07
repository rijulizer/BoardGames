import pygame
import sys
import math
import numpy as np
from pprint import pprint

from init import BoardVariables
from geometry import BoardGeometry

class GameLogics():
    def __init__(self, game_variables, game_geometry):
        print("[DEBUG]- Initiating Game Logics...")
        self.variables = game_variables
        self.geometry = game_geometry

    def check_valid_move(
            self,
            clicked_hex_name: str, 
            player: str, 
            player_captured_last: dict[str: tuple[int, int]],
        ) -> bool:
        """
        For a player check if the particular position is valid or not
        If its an empty position check if the player was captured in the same position in the last turn
        """
        shifted_q, shifted_r = self.geometry.flat_map_gird(clicked_hex_name)
        pos_in_map = self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r]
        
        # player was captured from this position in the last turn
        player_captured_last[player]
        # print("[DEBUG]- [check_valid_move]- player_captured_last", player_captured_last)
        # check if the board is empty 
        # and check if the player was captured from that pos in the previous turn
        if ((pos_in_map == -1) and ([shifted_q, shifted_r] != player_captured_last[player])): 
            return True
        return False
    
    def make_move(self, pos: str, player: str,):
        """
        Takes hex_name as player position and adds player symbol in the flat-map-grid
        """
        shifted_q, shifted_r = self.geometry.flat_map_gird(pos)
        self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r] = self.variables.PLAYERS[player]['symbol']

    def check_board(self, player: str) -> tuple[bool, list]:
        """
        Check board for->
        1. 5 contigous tokens in same line
        2. trap condition
        """
        grid_flat_map = np.array(self.variables.HEX_GRID_FLAT_MAP[0])
        player_symbol = self.variables.PLAYERS[player]['symbol']
        n = self.variables.boku_rule_cont_pos
        
        rows, cols = len(grid_flat_map), len(grid_flat_map[0])

        detect_traps = []
        # iterating over r
        # check for contiguos elements in rows
        for row_i, row in enumerate(grid_flat_map):
            for i in range (cols - n + 1):
                if all(row[i:i+n] == player_symbol):
                    return True, detect_traps
                if list(row[i:i+4]) in self.variables.TRAP_PATTERN:
                    detect_trap = [[row_i,i] for i in range(i,i+4)]
                    detect_traps.append(detect_trap)
            # since n=5 i will stop 1 before so add one more check for i+1: i+1+5
            if list(row[i+1:i+1+4]) in self.variables.TRAP_PATTERN:
                    detect_trap = [[row_i,i] for i in range(i+1,i+1+4)]
                    detect_traps.append(detect_trap)
        
        # iterating over q
        # check for contiguos elements in cols
        for col_i, col in enumerate(grid_flat_map.T):
            for i in range (rows - n + 1):
                if all(col[i:i+n] == player_symbol):
                    return True, detect_traps
                if list(col[i:i+4]) in self.variables.TRAP_PATTERN:
                    detect_trap = [[i, col_i] for i in range(i,i+4)]
                    detect_traps.append(detect_trap)
            # since n=5 i will stop 1 before so add one more check for i+1: i+1+5
            if list(col[i+1:i+1+4]) in self.variables.TRAP_PATTERN:
                    detect_trap = [[i, col_i] for i in range(i+1,i+1+4)]
                    detect_traps.append(detect_trap)

        # check for contiguos elements in anti-diagonals
        for i in range (rows - n + 1):
            for j in range(cols - n + 1):
                anti_diagonal = np.fliplr(grid_flat_map[i:i+n, j:j+n]).diagonal()
                if all(anti_diagonal == player_symbol):
                    return True, detect_traps
                
                # check for trap pattern
                anti_diagonal = np.fliplr(grid_flat_map[i:i+4, j:j+4]).diagonal()
                if list(anti_diagonal) in self.variables.TRAP_PATTERN:
                    # Pattern matched; now find the original indices
                    detect_trap = [[i + k, j + 4 - k - 1] for k in range(4)]
                    detect_traps.append(detect_trap)
                    
            # additional j+1 case because n=5 and trap_size=4
            anti_diagonal = np.fliplr(grid_flat_map[i:i+4, j+1:j+1+4]).diagonal()
            if list(anti_diagonal) in self.variables.TRAP_PATTERN:
                # Pattern matched; now find the original indices
                detect_trap = [[i + k, j + 1 + 4 - k - 1] for k in range(4)]
                detect_traps.append(detect_trap)
                
        # consider one more case with i+1 and iterate over all j
        for j in range(cols - 4 + 1):
            anti_diagonal = np.fliplr(grid_flat_map[i+1:i+1+4, j:j+4]).diagonal()
            if list(anti_diagonal) in self.variables.TRAP_PATTERN:
                # Pattern matched; now find the original indices
                detect_trap = [[i+1 + k, j + 4 - k - 1] for k in range(4)]
                detect_traps.append(detect_trap)

        return False, detect_traps            

    def detect_capture_move(self, clicked_hex_name: str, detected_traps: list):
        """
        checks if a particular move leads to a capture situation
        """
        detected_capture_moves = []
        shifted_q, shifted_r = self.geometry.flat_map_gird(clicked_hex_name)
        
        # check if the current move is part of any of the two ends of a trap pattern
        for trap in detected_traps:
            if [shifted_q, shifted_r] in [trap[0],trap[3]]: 
                detected_capture_moves.append(trap[1:3])
        return detected_capture_moves

    def capture_move(
            self,
            clicked_hex_name: str, 
            player: str, 
            detected_capture_moves: list, 
            player_captured_last: dict[str: tuple[int, int]],
            history_text: list[str],
            ):
        
        shifted_q, shifted_r = self.geometry.flat_map_gird(clicked_hex_name)
        # pos_in_flatmap = HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r]
        oppn_player = list(set(self.variables.PLAYERS.keys()) - set([player]))[0]
        # Since the player has already been switched so player holds the opponent player 
        # TODO: check if cheking of opponent trapped in between is needed or not
        # opponent_trap_windows = [trap_window[1:3] for trap_window in detected_capture_moves if trap_window[0] != PLAYERS[player]['symbol']]
        for trap_window in detected_capture_moves:
            if [shifted_q, shifted_r] in trap_window:
                self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r] = -1 # empty captured position
                # add captured move to illegal psotions for the next move
                player_captured_last[player] = [shifted_q,shifted_r] # make the position

                history_text.append(f"Player - {oppn_player} captures - {clicked_hex_name}")
        # print("[DEBUG]- [capture_move]- HEX_GRID_FLAT_MAP[0]\n")
        # pprint(HEX_GRID_FLAT_MAP[0])
        print("[DEBUG]- [capture_move]- player_captured_last", player_captured_last)

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
if __name__ == "__main__":
    board_variables = BoardVariables()
    # print("[DEBUG]-[geometry]- board_variable.HEX_GRID_FLAT_MAP after BoardVariables() \n")
    # pprint(board_variables.HEX_GRID_FLAT_MAP)
    board_geometry = BoardGeometry(board_variables)
    # print("[DEBUG]-[geometry]- board_variable.HEX_GRID_FLAT_MAP after BoardGeometry() \n")
    # pprint(board_variables.HEX_GRID_FLAT_MAP)
    game_logics = GameLogics(board_variables, board_geometry)