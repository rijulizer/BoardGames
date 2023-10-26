import sys
import numpy as np
from pprint import pprint
import time
import copy
from tqdm import tqdm
# import cProfile

from init import BoardVariables
from geometry import BoardGeometry
from game_logics import GameLogics


class Agent():
    """
    Random agent as base calss, randomly places tokens on th board
    """
    def __init__(self, game_variables, game_logics,):
        self.game_logics = game_logics
        self.variables = game_variables
    
    def get_valid_moves(self, player):
        """
        player: players turn
        generates all valid moves
        return: [[q1,r1], [q2, r2], [q3, r3]]
        """
        avilable_moves = []

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
                    avilable_moves.append(list(pair))
            avilable_moves = np.array(avilable_moves)
        
        else: # game in capture flow
            # all the capture moves are valid moves
            avilable_moves = self.game_logics.detected_capture_moves
            # flatten to list of indices -
            avilable_moves = np.array(avilable_moves).reshape(-1, len(avilable_moves[0][0]))
        # pprint(f"[DEBUG]-[Agent]- get_valid_moves - \n {avilable_moves}")
        return avilable_moves
    
    def play_random_agent(self, player):
        
        # agent player
        game_over = False # default declaration
        
        # generate valid moves
        avilable_moves = self.get_valid_moves(player)
        # randomly select a move
        rand_indexes = np.random.choice(avilable_moves.shape[0])
        shifted_q, shifted_r = avilable_moves[rand_indexes]
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
            self.game_logics.detect_capture_move(clicked_hex_name, detected_traps)
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
            avilable_moves = self.get_valid_moves(player)
            # randomly select one capture move
            rand_indexes = np.random.choice(avilable_moves.shape[0])
            shifted_q, shifted_r = avilable_moves[rand_indexes]
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
class AgentMiniMax(Agent):
    def __init__(self, game_variables, geometry, game_logics):
        super().__init__(game_variables, game_logics)
        self.geometry = geometry

    def copy_game_states(self, player):
        """
        Save the game states before minimax starts
        """
        # save a copy of different game states
        self.state_board = copy.deepcopy(self.variables.HEX_GRID_FLAT_MAP[0]) # pass a copy of the board
        self.state_player = player
        self.state_last_captured = copy.deepcopy(self.game_logics.player_captured_last)
        self.state_history_text = copy.deepcopy(self.game_logics.history_text)
        self.state_events = copy.deepcopy(self.game_logics.events)
        self.state_events_redo = copy.deepcopy(self.game_logics.events_redo)
    
    def trasfer_prev_game_states(self):
        """
        Trasfer back the saved game states after minimax
        """
        # save a copy of different game states
        self.variables.HEX_GRID_FLAT_MAP[0] = copy.deepcopy(self.state_board) # pass a copy of the board
        player = self.state_player
        self.game_logics.player_captured_last = copy.deepcopy(self.state_last_captured)
        self.game_logics.history_text = copy.deepcopy(self.state_history_text)
        self.game_logics.events = copy.deepcopy(self.state_events)
        self.game_logics.events_redo = copy.deepcopy(self.state_events_redo)
        return player
    
    def get_token_count_diff(self, player):
        """
        counts the differnece of number of players in the board
        """
        oppn_player = self.game_logics.get_opponent_player(player)
        player_count = np.count_nonzero(self.variables.HEX_GRID_FLAT_MAP[0]
                  == self.variables.PLAYERS[player]["symbol"])
        oppn_player_count = np.count_nonzero(self.variables.HEX_GRID_FLAT_MAP[0]
                  == self.variables.PLAYERS[oppn_player]["symbol"])
        # count diff values are like - +1, +2, -1, -2 
        # more the count_differnece better the value
        count_diff =  int(player_count - oppn_player_count)
        return count_diff
    
    def get_player_proximity_center(self, player):
        """
        # how close the player tokens are to the center, 
        # for token the further it is from the center the lesser the value
        # Value ranges for each token [5,4,3,2,1,0]
        # higher pos_value = better position
        """
        # proximity to center value, values range from 5 to 0 fromcenter to extreme outer hex
        pos_value = 0
        row_indices, col_indices = np.where(
                np.array(self.variables.HEX_GRID_FLAT_MAP[0])
                  == self.variables.PLAYERS[player]['symbol']
                )  
        for row, col in zip(row_indices, col_indices):
            q, r = row-5, col-4 # map to cube-cord q,r
            s = -q -r
            pos_value += int(5 - np.max(np.abs(np.array([q,r,s]))))
        return pos_value
    
    def static_eval(self, player):
        """
        Static evaluation function -
        Input: has access to board state, player 
        Features: 1. difference of count of tokens of the two players
                  2. Position Value, how close to the center the position is
                  3. how many capture move a certain move leads to.
        Return: Integer value
        """
        oppn_player = self.game_logics.get_opponent_player(player)
        pos_value = self.get_player_proximity_center(player) - self.get_player_proximity_center(oppn_player)
        return pos_value
    
    def agent_capture_move(
            self,
            clicked_hex_name: str, 
            player: str,
            ):
        """
        player: takes the current player (unlike game_logics) 
        only valid capture move is passed: 
        """
        
        shifted_q, shifted_r = self.geometry.get_flat_map_gird(clicked_hex_name)
        # get the player whos turn it was.
        oppn_player = self.game_logics.get_opponent_player(player)
        removed_symbol =  self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r]
        self.variables.HEX_GRID_FLAT_MAP[0][shifted_q][shifted_r] = self.variables.empty_space # empty captured position
        # add captured move to illegal positions for the next move of the opponent
        self.game_logics.player_captured_last[oppn_player] = [shifted_q, shifted_r]
        
        if self.game_logics.flag_track:
            self.game_logics.history_text.append(f"{player} - captures - {clicked_hex_name}")
            # add capture event
            self.game_logics.events.append({
            "capture":{
                "captured_hex": clicked_hex_name,
                "player_turn": player,
                "detected_capture_moves": self.game_logics.detected_capture_moves,
                "captured_hex_flat_cords": [shifted_q, shifted_r],
                "removed_symbol":  removed_symbol,
                "redo_flag_ind": True
                }
            })
            # print("[DEBUG]-[agents]-[capture_move]- last 3 events- \n")
            # pprint(self.game_logics.events[-3:])
        return oppn_player

    def agent_make_move(self, clicked_hex_name, player):
        """
        One step of the agent movement. Agent plays either in normal flow and/or in capture flow.
        If a normal-flow move leads to capture then it goes to capture flow in the same session. 
        Considers a valid hex_name has been trasnfered
        Return: game over flag, opponent player
        """
        game_over = False
        depth_reduce = 1 # educe minimax depth by 1 but if its a capture move dont reduce depth 
        # Normal Flow
        if not(len(self.game_logics.detected_capture_moves) > 0):
            # make move on the flat_board
            self.game_logics.make_move(clicked_hex_name, player)
            # Check the board if game is over and get trap positions
            game_over, detected_traps =  self.game_logics.check_board(player)
            # check if current move can lead to a capture
            # for inital few turns- detected_traps=[], detected_capture_moves=[]
            self.game_logics.detect_capture_move(clicked_hex_name, detected_traps)
            # in normal move, refresh any illegal move due to capture in prev turn
            self.game_logics.reset_last_captured()
            
            # check if the last move lead to detected_capture_moves
            if len(self.game_logics.detected_capture_moves) > 0: # capture flow
                # if move leads to capture then return the same player
                depth_reduce = 0 # dont reduce minimax depth 
            else: 
                # switch player if normal move does not lead to a capture move
                player = self.game_logics.get_opponent_player(player)
            

        # Capture flow
        else: 
            # switch player once capture move is done
            player = self.agent_capture_move(clicked_hex_name, player)
            # empty the detected capture moves so that each turn it will check 
            self.game_logics.detected_capture_moves = []

        return game_over, player, depth_reduce    
    
    def mark_best_capture_event(self,):
        """
        If the last event is a capture event, then add the capture information to previous move information.
        The function is invoked in minimax where the last capture event is the best capture event.
        This informatio will be added with the best move that lead to this best capture
        """
        # get the last event
        last_event = self.game_logics.events[-1] # shallow copy
        # get the type of event a string
        event_type = list(last_event.keys())[0]
        # if the last event is a capture read data
        if event_type == "capture":
            # get the event data
            captured_hex = last_event[event_type]["captured_hex"]
            [shifted_q, shifted_r] = last_event[event_type]["captured_hex_flat_cords"]
        
            # get the type of the second last event as string
            event_type = list(self.game_logics.events[-2].keys())[0]
            # put the last capture information in the sencond last move event
            if event_type == "move":
                self.game_logics.events[-2][event_type]["best_capture_hex"] = captured_hex
                self.game_logics.events[-2][event_type]["best_capture_hex_cords"] = [shifted_q, shifted_r]
                
        
    def minimax_ab(self, player: str, depth: int, alpha: int, beta: int) -> int:
        """
        Always -> MAX -p1, MIN -p2
        """
        # Check the board if game is over and get trap positions
        game_over, _ =  self.game_logics.check_board(player)
        if game_over:
            if player == 'p1':
                return 10
            elif player == 'p2':
                return -10
            else:
                # draw scenario
                return 0
        if depth <= 0:
            # player = self.game_logics.get_opponent_player(player)
            # print(f"[DEBUG]-[minimax]-depth==0: input_player: {player}, abs(score): {self.static_eval(player)}")
            # return value functions
            if player == 'p1':
                return self.static_eval(player)
            else:
                return -(self.static_eval(player))
        
        # generate available moves of the player
        avilable_moves = self.get_valid_moves(player)
        if player == 'p1':
            max_score = -np.inf
            # iterate through all available moves
            for move_index in range(avilable_moves.shape[0]):
                shifted_q, shifted_r = avilable_moves[move_index]
                # get the eqivalent hex name
                select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
                game_over, player, depth_reduce = self.agent_make_move(select_hex_name, player)
                score = self.minimax_ab(player, depth-depth_reduce, alpha, beta)
                # max_score = max(score, max_score)
                if score> max_score:
                    max_score=score
                    self.mark_best_capture_event()
                alpha = max(alpha, score)
                # undo move
                player = self.game_logics.undo_events()
                
                if alpha >= beta:
                    break
                
            return max_score
        else:
            min_score = +np.inf
            # iterate through all available moves
            for move_index in range(avilable_moves.shape[0]):
                shifted_q, shifted_r = avilable_moves[move_index]
                # get the eqivalent hex name
                select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
                game_over, player, depth_reduce = self.agent_make_move(select_hex_name, player)
                score = self.minimax_ab(player, depth-depth_reduce, alpha, beta)
                # min_score = min(score, min_score)
                if score< min_score:
                    min_score=score
                    self.mark_best_capture_event()
                beta = min(beta, score)
                # undo move
                player = self.game_logics.undo_events()
                if alpha >= beta:
                    break
            
            return min_score
     
    def play_agent(self, player, depth):
        """
        parent function that makes agent make the final move
        Agent - 2nd player
        """
        # agent player
        # generate all valid moves before each move
        avilable_moves = self.get_valid_moves(player)
        print(f"[Debug]-[play_agent]-avilable_moves len:{len(avilable_moves)}")
        min_score = + np.inf
        # copy game states before changes are made during the search
        self.copy_game_states(player)
        
        # iterate through all available moves
        for move_index in tqdm(range(avilable_moves.shape[0])):
            shifted_q, shifted_r = avilable_moves[move_index]
            # get the eqivalent hex name
            select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
            # print(f"[Debug]-[play_agent]-player: {player}, select_hex_name: {select_hex_name}")
            # search best move
            game_over, player, depth_reduce = self.agent_make_move(select_hex_name, player)
            score = self.minimax_ab(player, depth, - np.inf, + np.inf) 
            if score < min_score:
                min_score = score
                best_hex = select_hex_name
                self.mark_best_capture_event()
                best_events = self.game_logics.events[-5:]
            # print(f"score: {score}, min_hex: {best_hex}, min_score: {min_score}")
            # undo move
            player = self.game_logics.undo_events()
        print(f"[Debug]-[play_agent]-best_hex: {best_hex}, last_score: {score}, min_score: {min_score}")
        # print("[DEBUG]-[play_agent]-[best_events]- last 5 events- \n")
        # pprint(best_events)          
        # trasnfer back copied game states to games_logics object
        player = self.trasfer_prev_game_states()
        # make the final move, if the move leads to capture it will capture
        game_over, player, depth_reduce  = self.agent_make_move(best_hex, player)
        if 'best_capture_hex' in best_events[-1]['move'].keys():
            capture_hex = best_events[-1]['move']['best_capture_hex']
            # call agent_make_move again to capture
            game_over, player, _  = self.agent_make_move(capture_hex, player)

        return game_over, player
    
    
    
    # def place_token(self, board, pos, player):
    #     """
    #     Places player token on board position
    #     Return: 2D board with placed token, empty detected capture list
    #     """
    #     # shifted_q, shifted_r = self.geometry.flat_map_gird(pos)
    #     shifted_q, shifted_r = pos
    #     board[shifted_q][shifted_r] = self.variables.PLAYERS[player]['symbol']
    #     # after a new move has been made referesh the old detected_capture_moves list
    #     detected_capture_moves = []
    #     return board, detected_capture_moves
    
    # def check_board(self, board, player: str) -> tuple[bool, list]:
    #     """
    #     Check board for->
    #     1. 5 contigous tokens in same line
    #     2. trap condition
    #     """
    #     grid_flat_map = np.array(board)
    #     player_symbol = self.variables.PLAYERS[player]['symbol']
    #     n = self.variables.boku_rule_cont_pos
        
    #     rows, cols = len(grid_flat_map), len(grid_flat_map[0])

    #     detect_traps = []
    #     # iterating over r
    #     # check for contiguos elements in rows
    #     for row_i, row in enumerate(grid_flat_map):
    #         for i in range (cols - n + 1):
    #             if all(row[i:i+n] == player_symbol):
    #                 return True, detect_traps
    #             if list(row[i:i+4]) in self.variables.TRAP_PATTERN:
    #                 detect_trap = [[row_i,i] for i in range(i,i+4)]
    #                 detect_traps.append(detect_trap)
    #         # since n=5 i will stop 1 before so add one more check for i+1: i+1+5
    #         if list(row[i+1:i+1+4]) in self.variables.TRAP_PATTERN:
    #                 detect_trap = [[row_i,i] for i in range(i+1,i+1+4)]
    #                 detect_traps.append(detect_trap)
        
    #     # iterating over q
    #     # check for contiguos elements in cols
    #     for col_i, col in enumerate(grid_flat_map.T):
    #         for i in range (rows - n + 1):
    #             if all(col[i:i+n] == player_symbol):
    #                 return True, detect_traps
    #             if list(col[i:i+4]) in self.variables.TRAP_PATTERN:
    #                 detect_trap = [[i, col_i] for i in range(i,i+4)]
    #                 detect_traps.append(detect_trap)
    #         # since n=5 i will stop 1 before so add one more check for i+1: i+1+5
    #         if list(col[i+1:i+1+4]) in self.variables.TRAP_PATTERN:
    #                 detect_trap = [[i, col_i] for i in range(i+1,i+1+4)]
    #                 detect_traps.append(detect_trap)

    #     # check for contiguos elements in anti-diagonals
    #     for i in range (rows - n + 1):
    #         for j in range(cols - n + 1):
    #             anti_diagonal = np.fliplr(grid_flat_map[i:i+n, j:j+n]).diagonal()
    #             if all(anti_diagonal == player_symbol):
    #                 return True, detect_traps
                
    #             # check for trap pattern
    #             anti_diagonal = np.fliplr(grid_flat_map[i:i+4, j:j+4]).diagonal()
    #             if list(anti_diagonal) in self.variables.TRAP_PATTERN:
    #                 # Pattern matched; now find the original indices
    #                 detect_trap = [[i + k, j + 4 - k - 1] for k in range(4)]
    #                 detect_traps.append(detect_trap)
                    
    #         # additional j+1 case because n=5 and trap_size=4
    #         anti_diagonal = np.fliplr(grid_flat_map[i:i+4, j+1:j+1+4]).diagonal()
    #         if list(anti_diagonal) in self.variables.TRAP_PATTERN:
    #             # Pattern matched; now find the original indices
    #             detect_trap = [[i + k, j + 1 + 4 - k - 1] for k in range(4)]
    #             detect_traps.append(detect_trap)
                
    #     # consider one more case with i+1 and iterate over all j
    #     for j in range(cols - 4 + 1):
    #         anti_diagonal = np.fliplr(grid_flat_map[i+1:i+1+4, j:j+4]).diagonal()
    #         if list(anti_diagonal) in self.variables.TRAP_PATTERN:
    #             # Pattern matched; now find the original indices
    #             detect_trap = [[i+1 + k, j + 4 - k - 1] for k in range(4)]
    #             detect_traps.append(detect_trap)

    #     return False, detect_traps            

    # def detect_capture_move(self, pos, detected_traps: list):
    #     """
    #     checks if a particular move leads to a capture situation
    #     """
    #     detected_capture_moves = []
    #     shifted_q, shifted_r = pos
        
    #     # check if the current move is part of any of the two ends of a trap pattern
    #     for trap in detected_traps:
    #         if [shifted_q, shifted_r] in [trap[0],trap[3]]: 
    #             detected_capture_moves.append(trap[1:3])
    #     return detected_capture_moves
        
    #     # if (len(detected_capture_moves) > 0):
    #     #     # check if last event is a move event
    #     #     event_type = list(self. events[-1].keys())[0]
    #     #     if event_type == "move":
    #     #         # modify the detected captured moves 
    #     #         self.events[-1][event_type]["detected_capture_moves"] = self.detected_capture_moves
    


if __name__ == "__main__":
    board_variables = BoardVariables()
    board_geometry = BoardGeometry(board_variables)
    game_logics = GameLogics(board_variables, board_geometry)
    agent = Agent(board_variables, game_logics,)
    agent_ab = AgentMiniMax(board_variables, game_logics,)

