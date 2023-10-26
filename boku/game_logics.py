import pygame
import sys
import math
import numpy as np
from pprint import pprint
import time

from init import BoardVariables
from geometry import BoardGeometry

class GameLogics():
    def __init__(self, game_variables: object, game_geometry: object, flag_track: bool = True):
        print("[DEBUG]- Initiating Game Logics...")
        self.variables = game_variables
        self.geometry = game_geometry
        self.events = []
        self.events_redo = []
        # the text that is displayed on the right side of the screen in the history board
        self.history_text = [f"Game starts!! Player-1 starts -"] # refresh history
        self.player_captured_last ={
        'p1': [None,None],
        'p2': [None,None],
        }
        self.detected_capture_moves = []
        self.flag_track = flag_track
                        
    def get_opponent_player(self, player):
        # oppn_player = list(set(self.variables.PLAYERS.keys()) - set([player]))[0]
        # This is faster
        if player == "p1":
            return "p2"
        elif player == "p2":
            return "p1"
        else:
            raise ValueError("player should be in - ['p1','p2']")

    def check_valid_move(
            self,
            clicked_hex_name: str, 
            player: str, 
        ) -> bool:
        """
        For a player check if the particular position is valid or not in normal flow.
        If its an empty position check if the player was captured in the same position in the last turn
        """
        shifted_q, shifted_r = self.geometry.get_flat_map_gird(clicked_hex_name)
        pos_in_map = self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r]
        
        # player was captured from this position in the last turn
        # print("[DEBUG]- [check_valid_move]- player_captured_last", player_captured_last)
        
        # check if the board is empty 
        # and check if the player was captured from that pos in the previous turn
        if ((pos_in_map == self.variables.empty_space) and ([shifted_q, shifted_r] != self.player_captured_last[player])): 
            return True
        return False
    
    def make_move(self, pos: str, player: str, flag_redo: bool = False, redo_detected_capture_moves=[]):
        """
        Takes hex_name as player position (clicked_hex_name) and adds player symbol in the flat-map-grid
        """
        shifted_q, shifted_r = self.geometry.get_flat_map_gird(pos)
        self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r] = self.variables.PLAYERS[player]['symbol']
        if flag_redo: # redo flow
            detected_capture_moves = redo_detected_capture_moves
            if self.flag_track:
                self.history_text.append(f"[Redo] - {player} - moves to - {pos}")

        else: # normal flow make_move
            self.events_redo = [] # refresh the redo list as a new move have been made after undo
            detected_capture_moves = []
            if self.flag_track:
                self.history_text.append(f"{player} - moves to - {pos}")
        
        if self.flag_track:
            # add an event type="move"
            self.events.append({
                "move":{
                    "player_turn": player,
                    "hex_name": pos,
                    # "hex_points": self.variables.HEX_GRID_CORDS[pos],
                    "detected_capture_moves": detected_capture_moves, # gets updated by detect_capture_move()
                    "flag_redo_ind": flag_redo} # indicates whether the event is normal or redo 
                })
            # pprint("[DEBUG] - [EVENTS] - [make_move]- last 5 events added - \n")
            # pprint(self.events[-5:])
        
    def undo_move(self, pos: str, player: str):
        """
        Takes hex_name as player position (clicked_hex_name) and un-does opponent player symbol in the flat-map-grid
        """
        shifted_q, shifted_r = self.geometry.get_flat_map_gird(pos)
        # empty position
        self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r] = self.variables.empty_space
        # if the mode had lead to detect captured moves then empty that
        if len(self.detected_capture_moves) > 0:
            self.detected_capture_moves = []
        if self.flag_track:
            self.history_text.append(f"[Undo] - {player} - moves to - {pos}")

    def check_board(self, player: str):
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
        detected_traps: list of list of pisitons where trap pattern has been detected
        """
        self.detected_capture_moves = []
        shifted_q, shifted_r = self.geometry.get_flat_map_gird(clicked_hex_name)
        
        # check if the current move is part of any of the two ends of a trap pattern
        for trap in detected_traps:
            if [shifted_q, shifted_r] in [trap[0],trap[3]]: 
                self.detected_capture_moves.append(trap[1:3]) # append the trapped opponent's flat cords
        
        if (len(self.detected_capture_moves) > 0) and self.flag_track:
            # check if last event is a move event
            event_type = list(self.events[-1].keys())[0]
            if event_type == "move":
                # add detected captured moves with the "move" event
                self.events[-1][event_type]["detected_capture_moves"] = self.detected_capture_moves
            # pprint("[DEBUG] - [EVENTS] - [detect_capture_move]- event added - \n")
            # pprint(self.events[-5:])

    def check_click_capture_hex(
            self,
            clicked_hex_name: str, 
            ):
        """
        Rule: if a move leads to capture move then the player must capture the opponent.
        Checks if one of the capture hex is clicked during capturing move or not.
        """
        shifted_q, shifted_r = self.geometry.get_flat_map_gird(clicked_hex_name)
        for trap_window in self.detected_capture_moves:
            if [shifted_q, shifted_r] in trap_window:
                return True
        return False
    
    def capture_move_v2(
            self,
            clicked_hex_name: str, 
            oppn_player: str,
            ):
        """
        oppn_player: takes the opponent player # logic is compatible with 2 player version 
        only valid capture move is passed: 
        """
        
        shifted_q, shifted_r = self.geometry.get_flat_map_gird(clicked_hex_name)
        # get the player whos turn it was.
        player = self.get_opponent_player(oppn_player)
        removed_symbol =  self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r]
        self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r] = self.variables.empty_space # empty captured position
        # add captured move to illegal positions for the next move of the opponent
        self.player_captured_last[oppn_player] = [shifted_q, shifted_r]
        
        if self.flag_track:
            self.history_text.append(f"{player} - captures - {clicked_hex_name}")
            # add capture event
            self.events.append({
            "capture":{
                "captured_hex": clicked_hex_name,
                "player_turn": player,
                "detected_capture_moves": self.detected_capture_moves,
                "captured_hex_flat_cords": [shifted_q, shifted_r],
                "removed_symbol":  removed_symbol,
                "redo_flag_ind": True
                }
            })
            pprint("[DEBUG]-[game_logics]-[capture_move]- last 3 events- \n")
            pprint(self.events[-3:])
    
    # def capture_move(
    #         self,
    #         clicked_hex_name: str, 
    #         player: str,
    #         ):
    #     """
    #     May or may not capture logic
    #     """
        
    #     shifted_q, shifted_r = self.geometry.flat_map_gird(clicked_hex_name)
    #     # pos_in_flatmap = HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r]
    #     oppn_player = list(set(self.variables.PLAYERS.keys()) - set([player]))[0]
    #     # Since the player has already been switched so player holds the opponent player 
    #     for trap_window in self.detected_capture_moves:
    #         if [shifted_q, shifted_r] in trap_window:
    #             removed_symbol =  self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r]
    #             self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r] = self.variables.empty_space # empty captured position
    #             # add captured move to illegal psotions for the next move
    #             self.player_captured_last[player] = [shifted_q,shifted_r]

    #             self.history_text.append(f"{oppn_player} - captures - {clicked_hex_name}")
    #             # add capture event
    #             self.events.append({
    #             "capture":{
    #                 "captured_hex": clicked_hex_name,
    #                 "player_turn": oppn_player,
    #                 "detected_capture_moves": self.detected_capture_moves,
    #                 "captured_hex_flat_cords": [shifted_q, shifted_r],
    #                 "removed_symbol":  removed_symbol,
    #                 "redo_flag_ind": True
    #                 }
    #             })
    #             # pprint("[DEBUG] - [EVENTS] - [capture_move]- event added - \n")
    #             # pprint(self.events[-5:])
            
    #     # print("[DEBUG]- [capture_move]- HEX_GRID_FLAT_MAP[0]\n")
    #     # pprint(HEX_GRID_FLAT_MAP[0])
    #     # print("[DEBUG]- [capture_move]- player_captured_last", self.player_captured_last)

    def reset_last_captured(self):
        self.player_captured_last ={
        'p1': [None,None],
        'p2': [None,None],
        }
    
    def undo_events(self):
        """
        Input the latest event from events list
        """
        # get the last event
        event = self.events.pop()
        self.events_redo.append(event)
        # get the type of event a string
        event_type = list(event.keys())[0]

        if event_type == "move":
            player = event[event_type]["player_turn"]
            hex_name = event[event_type]["hex_name"]
            # detected_capture_moves = event[event_type]["detected_capture_moves"]
            self.undo_move(hex_name, player)
            # pprint("[DEBUG] - [EVENTS] - [undo_make_move]- events added - \n")
            # pprint(self.events[-5:])
            return player
        
        elif event_type == "capture":
            # get the event data
            captured_hex = event[event_type]["captured_hex"]
            player = event[event_type]["player_turn"]
            detected_capture_moves = event[event_type]["detected_capture_moves"]
            oppn_player = self.get_opponent_player(player)
            [shifted_q, shifted_r] = event[event_type]["captured_hex_flat_cords"]
            removed_symbol = event[event_type]["removed_symbol"]
            
            # put the token back on the grid
            self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r] = removed_symbol
            # get back the detected capture moves too
            self.detected_capture_moves = detected_capture_moves
            # undo illegal psotions for the next move
            self.player_captured_last[player] = [None,None]

            # pprint("[DEBUG] - [EVENTS] - [undo_capture_move]- events - \n")
            # pprint(self.events[-5:])
            if self.flag_track:
                self.history_text.append(f"[Undo] - {player} - captures - {captured_hex}")
            return oppn_player

    def redo_events(self):
        """
        Input the latest event from events list
        """
        print("[DEBUG]-[Redo_events]")  # Perform restart action here
        # get the last event
        event = self.events_redo.pop()
        event_type = list(event.keys())[0]
        
        if event_type == "move":
            player = event[event_type]["player_turn"]
            oppn_player = self.get_opponent_player(player)
            hex_name = event[event_type]["hex_name"]
            redo_detected_capture_moves = event[event_type]["detected_capture_moves"]
            self.make_move(hex_name, player, True, redo_detected_capture_moves)
            # if that move detected captures then return the detected captures in the main game
            self.detected_capture_moves = redo_detected_capture_moves
            return oppn_player
        
        elif event_type == "capture":
            captured_hex = event[event_type]["captured_hex"]
            player = event[event_type]["player_turn"]
            oppn_player = self.get_opponent_player(player)
            detected_capture_moves = event[event_type]["detected_capture_moves"]
            [shifted_q, shifted_r] = event[event_type]["captured_hex_flat_cords"]
            removed_symbol = event[event_type]["removed_symbol"]
            
            # put the token back on the grid
            self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r] = self.variables.empty_space # empty captured position
            # redo: once capture is done again empty detected_capture_moves
            self.detected_capture_moves = []
            # redo captured move to illegal psotions for the next move
            self.player_captured_last[player] = [shifted_q,shifted_r] # make the position
            if self.flag_track:
                # add Redo capture event
                self.events.append({
                "capture":{
                    "captured_hex": captured_hex,
                    "player_turn": player,
                    "detected_capture_moves": detected_capture_moves,
                    "captured_hex_flat_cords": [shifted_q, shifted_r],
                    "removed_symbol":  removed_symbol,
                    "redo_flag_ind": True
                    }
                })
                # pprint("[DEBUG] - [EVENTS] - [redo_capture_move]- events - \n")
                # pprint(self.events[-5:])
                self.history_text.append(f"[Rodo] - {player} - captures - {captured_hex}")
            return oppn_player
        
    def play_user(self, clicked_hex_name: str, player: str):
        """
        Normal Flow: checks if move is valid, Places token in board, checks game over, detects capture moves
            Returns: game_over flag and opponent player, flag_valid_move
        Capture Flow: checks if capture move is valid, Places token in board, checks game over, detects capture moves
            Input: in capture flow input player holds opponent player
            Returns: game_over flag and same player, flag_valid_move
        """
        game_over = False # default declaration
        
        # normal flow of game (capture not detected)
        if not(len(self.detected_capture_moves) > 0):
            print(f"[DEBUG]-[play_user]- game in - Normal Flow!!")
            # check if the move is vald or not
            if self.check_valid_move(clicked_hex_name, player):
                flag_valid_move = True
                # make move on the flat_board
                self.make_move(clicked_hex_name, player)
                # Check the board if game is over and get trap positions
                game_over, detected_traps =  self.check_board(player)
                
                # check if current move can lead to a capture
                # for inital few turns- detected_traps=[], detected_capture_moves=[]
                self.detect_capture_move(clicked_hex_name, detected_traps)
                
                # if (len(self.detected_capture_moves) > 0): # debugging purpose
                #     print(f"[DEBUG]-[main]- game_logics.detected_capture_moves are - ")
                #     pprint(self.detected_capture_moves)
                #     print(f"[DEBUG]-[main]- Entering - Capture Mode")
                
                # in normal move, refresh any illegal move due to capture in prev turn
                self.reset_last_captured()
                if game_over:
                    print(f"[DEBUG]-[play_user]-game over winner- {player}")
                    self.history_text.append(f"[Game Over] Winner is - {player} !!")
                    # break
                
                # switch player
                player = self.get_opponent_player(player)
                
            else:
                flag_valid_move = False
                print("[DEBUG]-[play_user]- [check_valid_move]- Invalid Move!")
                self.history_text.append(f"Invalid Move!")
                

        else: # game in capture flow
            print(f"[DEBUG]-[play_user]- game in - Capture Mode")
            # check if user is clicking on valid capture hex
            if (self.check_click_capture_hex(clicked_hex_name)):
                flag_valid_move = True
                self.capture_move_v2(
                    clicked_hex_name, 
                    player,
                    )
                # empty the detected capture moves so that each turn it will check 
                self.detected_capture_moves = []
                print(f"[DEBUG]-[play_user]- Exiting - Capture Mode")
            else:
                self.history_text.append(f"Invalid Move!, you have to capture.")
                flag_valid_move = False
        return game_over, player, flag_valid_move


if __name__ == "__main__":
    board_variables = BoardVariables()
    # print("[DEBUG]-[geometry]- board_variable.HEX_GRID_FLAT_MAP after BoardVariables() \n")
    # pprint(board_variables.HEX_GRID_FLAT_MAP)
    board_geometry = BoardGeometry(board_variables)
    # print("[DEBUG]-[geometry]- board_variable.HEX_GRID_FLAT_MAP after BoardGeometry() \n")
    # pprint(board_variables.HEX_GRID_FLAT_MAP)
    game_logics = GameLogics(board_variables, board_geometry)
    # test game logics
    start_time = time.time()
    game_logics.check_board("p1")
    time.sleep(3)
    print(f"[DEBUG]-[game_logics]-[check_board]- time - {round(time.time()-start_time,2)}")



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
