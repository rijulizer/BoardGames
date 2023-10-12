import sys
import numpy as np
from pprint import pprint
import time
from copy import copy, deepcopy
from tqdm import tqdm

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
    # def play_agent(self, player):
    #     # agent player
    #     game_over = False # default declaration
    #     # generate valid moves
    #     self.get_valid_moves(player)
    #     # randomly select a move
    #     rand_indexes = np.random.choice(avilable_moves.shape[0])
    #     shifted_q, shifted_r = avilable_moves[rand_indexes]
    #     # get the eqivalent hex name
    #     clicked_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
    #     # normal flow of game (capture not detected)
    #     print(f"[DEBUG]-[Agent]-[play_agent]- selected_hex_name- ", clicked_hex_name)
    #     # Normal Flow
    #     if not(len(self.game_logics.detected_capture_moves) > 0):
    #         print(f"[DEBUG]-[Agent]-[play_agent]- Normal Flow!!")
    #         # make move on the flat_board
    #         self.game_logics.make_move(clicked_hex_name, player)
    #         # Check the board if game is over and get trap positions
    #         game_over, detected_traps =  self.game_logics.check_board(player)
    #         # check if current move can lead to a capture
    #         # for inital few turns- detected_traps=[], detected_capture_moves=[]
    #         self.game_logics.detect_capture_move(clicked_hex_name, player, detected_traps)

    #         # in normal move, refresh any illegal move due to capture in prev turn
    #         self.game_logics.reset_last_captured()
    #         if game_over:
    #             print(f"[DEBUG]-[play_game_multiuser]-game over winner- {player}")
    #             self.game_logics.history_text.append(f"[Game Over] Winner is - {player} !!")
    #             # break
            
    #         # switch player
    #         player = self.game_logics.get_opponent_player(player)
        
    #     else: # game in capture flow
    #         print(f"[DEBUG]-[main]- game in - Capture Mode")
    #         self.game_logics.capture_move_v2(
    #             clicked_hex_name, 
    #             player,
    #             )
    #         # empty the detected capture moves so that each turn it will check 
    #         self.game_logics.detected_capture_moves = []
    #         print(f"[DEBUG]-[main]- Exiting - Capture Mode")
    #         # click anywhere else in the board to not capture
        
    #     return game_over, player
    
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
    def __init__(self, game_variables, game_logics):
        super().__init__(game_variables, game_logics)
        # self.geometry = geometry

    def copy_game_states(self, player):
        """
        Save the game states before minimax starts
        """
        # save a copy of different game states
        self.state_board = self.variables.HEX_GRID_FLAT_MAP[0].copy() # pass a copy of the board
        self.state_player = player
        self.state_last_captured = self.game_logics.player_captured_last
        self.state_history_text = self.game_logics.history_text.copy()
        self.state_events = self.game_logics.events.copy()
        self.state_events_redo = self.game_logics.events_redo.copy()
    
    def trasfer_prev_game_states(self):
        """
        Trasfer back the saved game states after minimax
        """
        # save a copy of different game states
        self.variables.HEX_GRID_FLAT_MAP[0] = self.state_board.copy() # pass a copy of the board
        player = self.state_player
        self.game_logics.player_captured_last = self.state_last_captured.copy()
        self.game_logics.history_text = self.state_history_text.copy()
        self.game_logics.events  =self.state_events.copy()
        self.game_logics.events_redo = self.state_events_redo.copy()
        return player
    
    def agent_make_move(self, clicked_hex_name, player):
        """
        One step of the agent movement. Agent plays either in normal flow and/or in capture flow.
        If a normal-flow move leads to capture then it goes to capture flow in the same session. 
        Considers a valid hex_name has been trasnfered
        Return: game over flag, opponent player
        """
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
            self.game_logics.capture_move_v2(
                clicked_hex_name, 
                oppn_player,
                )
            # empty the detected capture moves so that each turn it will check 
            self.game_logics.detected_capture_moves = []
            
    
        return game_over, oppn_player    

    def minimax_ab(self, select_hex_name: str, player: str, depth: int, alpha: int, beta: int) -> int:
        """
        Always -> MAX -p1, MIN -p2
        """
        # Check the board if game is over and get trap positions
        game_over, _ =  self.game_logics.check_board(player)
        if game_over:
            # print(f"\n[Debug]-depth- {depth}, finsihed")# max_player- score: {score}, max_score :{max_score}")
            # print("\n[Debug]-depth- {depth}, min_player- score: {score}, min_score :{min_score}")
            if player == 'p1':
                return 10, player
            elif player == 'p2':
                return -10, player
            else:
                # draw scenario
                return 0, player
        if depth == 0:
            # return value functions
            if player == 'p1':
                return self.variables.board_pos_values[select_hex_name], _
            else:
                return -(self.variables.board_pos_values[select_hex_name]), _
            
        
        avilable_moves = self.get_valid_moves(player)
        if player == 'p1':
            max_score = -np.inf
            # iterate through all available moves
            for move_index in range(avilable_moves.shape[0]):
                shifted_q, shifted_r = avilable_moves[move_index]
                # get the eqivalent hex name
                select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
                game_over, oppn_player = self.agent_make_move(select_hex_name, player)
                score, _ = self.minimax_ab(select_hex_name, oppn_player, depth-1, alpha, beta)
                # undo move
                player = self.game_logics.undo_events()
                max_score = max(score, max_score)
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
                
            return max_score, player
        else:
            min_score = +np.inf
            # iterate through all available moves
            for move_index in range(avilable_moves.shape[0]):
                shifted_q, shifted_r = avilable_moves[move_index]
                # get the eqivalent hex name
                select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
                game_over, oppn_player = self.agent_make_move(select_hex_name, player)
                score, _ = self.minimax_ab(select_hex_name, oppn_player, depth-1, alpha, beta)
                # undo move
                player = self.game_logics.undo_events()
                min_score = min(score, min_score)
                beta = min(beta, score)
                if alpha >= beta:
                    break
            
            return min_score, player
     
    def play_agent(self, player, depth):
        """
        parent function that makes agent make the final move
        Agent - 2nd player
        """
        # agent player
        game_over = False # default declaration
        # generate valid moves before each move
        avilable_moves = self.get_valid_moves(player)
        min_score = + np.inf
        # self.game_logics.flag_track = False
        # print(f"[DEBUG]-[play_agent]- searching {len(avilable_moves)} available moves")
        # iterate through all available moves
        for move_index in tqdm(range(avilable_moves.shape[0])):
            shifted_q, shifted_r = avilable_moves[move_index]
            # get the eqivalent hex name
            select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
            self.copy_game_states(player)
            # search best move
            score, _ = self.minimax_ab(select_hex_name, player, depth, alpha = -np.inf, beta = np.inf,)
            if score < min_score:
                min_score = score
                best_hex = select_hex_name
        player = self.trasfer_prev_game_states()
        # make the final move, if the move leads to capture it will capture
        game_over, oppn_player  = self.agent_make_move(best_hex, player)
        return game_over, oppn_player
    
                
    # def get_token_count_diff(self, player):
    #     """
    #     counts the differnece of number of players in the board
    #     """
    #     oppn_player = self.game_logics.get_opponent_player(player)
    #     player_count = np.count_nonzero(self.variables.HEX_GRID_FLAT_MAP[0]
    #               == self.variables.PLAYERS[player]["symbol"])
    #     oppn_player_count = np.count_nonzero(self.variables.HEX_GRID_FLAT_MAP[0]
    #               == self.variables.PLAYERS[oppn_player]["symbol"])
    #     # count diff values are like - +1, +2, -1, -2 
    #     # more the count_differnece better the value
    #     count_diff =  int(player_count - oppn_player_count)
    #     return count_diff

    # def static_eval(self, player):
    #     """
    #     Static evaluation function - 
    #     Features: 1. differnce of count of tokens of the two players
    #               2. Position Value, how close to the center the position is
    #               3. how many capture move a certain move leads to.
    #     """
    #     hex_name = None
    #     token_count_diff = self.get_token_count_diff(player)
    #     pos_value = self.variables.board_pos_values[hex_name]
    
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

