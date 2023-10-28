import sys
import numpy as np
from pprint import pprint
import time
import copy
from tqdm import tqdm
import hashlib
# import cProfile

from init import BoardVariables
from geometry import BoardGeometry
from game_logics import GameLogics

class Agent():
    """
    Random agent as base calss, randomly places tokens on th board
    """
    def __init__(self, game_variables, game_logics):
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
            game_over =  self.game_logics.check_game_over(player, clicked_hex_name)
            # check if current move can lead to a capture
            # for inital few turns- detected_traps=[], detected_capture_moves=[]
            self.game_logics.get_capture_moves(player, clicked_hex_name)
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
    """
    Agent with Minimax search and alpha beta capabilities
    """
    def __init__(self, game_variables, game_logics, geometry):
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
    def get_player_proximity_center(self, player):
        """
        # how close the player tokens are to the center, 
        # for token the further it is from the center the lesser the value
        # Value ranges for each token [5,4,3,2,1,0]
        # higher pos_value = better position
        """
        # # proximity to center value, values range from 5 to 0 fromcenter to extreme outer hex
        # shifted_q, shifted_r = self.geometry.get_flat_map_gird(pos)
        # q, r = shifted_q-5, shifted_r-4 # map to cube-cord q,r
        # s = -q -r
        # pos_value = int(5 - np.max(np.abs(np.array([q,r,s]))))
        # return pos_value
        
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
    
    def static_eval(self, player, pos):
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
        # print(f"[DEBUG]-[static_eval] - pos_value: {pos_value}")
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
            game_over =  self.game_logics.check_game_over(player, clicked_hex_name)
            # check if current move can lead to a capture
            # for inital few turns- detected_traps=[], detected_capture_moves=[]
            self.game_logics.get_capture_moves(player, clicked_hex_name)
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
                   
    def minimax_ab(self, player: str, max_player: bool, select_hex_name: str, depth: int, alpha: int, beta: int) -> int:
        """
        Always -> MAX -p1, MIN -p2
        """
        # Check the board if game is over and get trap positions
        game_over =  self.game_logics.check_game_over(player, select_hex_name)
        if game_over:
            if player == 'p1':
                return 10000
            elif player == 'p2':
                return -10000
            else:
                # draw scenario
                return 0
        if (depth <=0) and not(len(self.game_logics.detected_capture_moves) > 0):
            # if capture move deteceted play another round
            # player = self.game_logics.get_opponent_player(player)
            # print(f"[DEBUG]-[minimax]-depth==0: input_player: {player}, abs(score): {self.static_eval(player)}")
            # return value functions
            if player == 'p1':
                return self.static_eval(player, select_hex_name)
            else:
                return -(self.static_eval(player, select_hex_name))
        
        # generate available moves of the player
        avilable_moves = self.get_valid_moves(player)
        if max_player:
            max_score = -np.inf
            # iterate through all available moves
            for move_index in range(avilable_moves.shape[0]):
                shifted_q, shifted_r = avilable_moves[move_index]
                # get the eqivalent hex name
                select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
                game_over, oppn_player, depth_reduce = self.agent_make_move(select_hex_name, player)
                score = self.minimax_ab(player, False, select_hex_name, depth-depth_reduce, alpha, beta)
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
                game_over, oppn_player, depth_reduce = self.agent_make_move(select_hex_name, player)
                score = self.minimax_ab(player, True, select_hex_name, depth-depth_reduce, alpha, beta)
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
            game_over, oppn_player, _ = self.agent_make_move(select_hex_name, player)
            score = self.minimax_ab(player, True, select_hex_name, depth, - np.inf, + np.inf) 
            if score < min_score:
                min_score = score
                best_hex = select_hex_name
                self.mark_best_capture_event()
                best_events = self.game_logics.events[-3:]
            # print(f"player: {player}, score: {score}, min_hex: {best_hex}, min_score: {min_score}")
            # undo move
            player = self.game_logics.undo_events()
        print(f"[Debug]-[play_agent]-best_hex: {best_hex}, last_score: {score}, min_score: {min_score}")
        # print("[DEBUG]-[play_agent]-[best_events]- last 5 events- \n")
        # pprint(best_events)          
        # trasnfer back copied game states to games_logics object
        player = self.trasfer_prev_game_states()
        # make the final move, if the move leads to capture it will capture
        game_over, player, _  = self.agent_make_move(best_hex, player)
        if 'best_capture_hex' in best_events[-1]['move'].keys():
            capture_hex = best_events[-1]['move']['best_capture_hex']
            # call agent_make_move again to capture
            game_over, player, _  = self.agent_make_move(capture_hex, player)

        return game_over, player

class AgentMiniMaxID(AgentMiniMax):
    """
    Agent has Minimax, alpha-beta, Iterative Deepening
    """
    def __init__(self, game_variables, game_logics, geometry):
        super().__init__(game_variables, game_logics, geometry)
    def get_line_preference(self, player, pos):
        """
        gets a preference value based on whether a particular move of a player makes contiguous lines
        Logic: 1. get the lines(q,r,s) containing current pos
               2. Create windows of size=4 in each line direction including the pos
               3. Convolute with filters that has sense of contunous elements of 4
               # as size 5 would lead to win/loose that is already considered
               4. take the max of convolution value that gives max cont. lines in a direction
        Input: pos= hex name, player =plyaer turn
        """
        shifted_q, shifted_r = self.geometry.get_flat_map_gird(pos)
        # get the lines(q,r,s) containing current pos
        [shifted_q_row, shifted_r_col, anti_diag_elems, pos_adiag] = self.game_logics.get_hex_axis_lines(pos)
        # get different direction of lines
        same_lines = [shifted_q_row, shifted_r_col, anti_diag_elems]
        # euivalent point index in each direction
        point_poss = [shifted_r, shifted_q, pos_adiag]
        cont_size = 5
        # Create windows of size=cont_size in each line direction including the pos
        line_windows = []
        for same_line, point_pos in zip(same_lines, point_poss):
            l_lim = len(same_line[:point_pos+1]) # includes nones
            l_lim = min(l_lim, cont_size) # cosider board boundary cases
            r_lim = len(same_line[point_pos:])
            r_lim = min(r_lim, cont_size)
            # dir_windows = []
            for i in range((point_pos+1 - l_lim), ((point_pos + r_lim - cont_size)+1)):
                # print(same_line[i:i+cont_size])
                if (None not in same_line[i:i+cont_size]) and (len(same_line[i:i+cont_size])==cont_size):
                    line_windows.append(np.array(same_line[i:i+cont_size]).astype('int'))
            # line_windows.append(dir_windows)
            # pprint(dir_windows)
        # pprint(line_windows)
        line_windows = np.array(line_windows).reshape(-1, cont_size)
        oppn_player = self.game_logics.get_opponent_player(player)
        # filter_p1 = np.array([1,1,1,1])
        # filter_p2 = np.array([-1,-1,-1,-1])
        filter_p1 = np.array([self.variables.PLAYERS[player]["symbol"] for i in range(cont_size)])
        filter_p2 = np.array([self.variables.PLAYERS[oppn_player]["symbol"] for i in range(cont_size)])
        max_conv_fp1 = -np.inf
        max_conv_fp2 = 0
        for win in line_windows:
            conv_fp1 = np.dot(win, filter_p1)
            conv_fp2 = np.dot(win, filter_p2)
            # find the max conv value across all directions
            max_conv_fp1 = max(max_conv_fp1, conv_fp1)
            max_conv_fp2 = max(max_conv_fp2, conv_fp2) 
        if max_conv_fp2>0: # there are nearby opponent players
            if max_conv_fp2>=2: # opponent close to win
                max_conv_fp2 *= 2 # add more priority than self win
                max_conv_fp1 += max_conv_fp2 # add to players value 

        return max_conv_fp1 + cont_size # as the minimum value is -cont_size to make it zero

    def static_eval(self, player, pos):
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
        line_conv_val = self.get_line_preference(player, pos)
        statc_val = pos_value + 3 * line_conv_val
        # print(f"[DEBUG]-[static_eval]-player: {player}, pos: {pos}, eval: {[pos_value, line_conv_val]}")
        return statc_val
               
    def iter_deep_search(self, player, max_depth, max_time: float = None):
        """
        Iteratively increase the depth of search
        Input: max_time - maximum allowed time in mintues, if both max depth and max time is given max time gets higher preference
        """
        min_score = + np.inf
        start_time = time.time()
        # generate all valid moves before each move
        avilable_moves = self.get_valid_moves(player)
        print(f"[Debug]-[play_agent]-avilable_moves len:{len(avilable_moves)}")    
        
        for depth in tqdm(range(max_depth+1)): 
            print(f"\n[Debug]-[play_agent]-[ID]- depth: {depth}")
            # iterate through all available moves
            for move_index in tqdm(range(avilable_moves.shape[0])):
                shifted_q, shifted_r = avilable_moves[move_index]
                # get the eqivalent hex name
                select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
                # print(f"[Debug]-[play_agent]-[ID]-player: {player}, select_hex_name: {select_hex_name}")
                # search best move
                game_over, oppn_player, _ = self.agent_make_move(select_hex_name, player)
                score = self.minimax_ab(player, True, select_hex_name, depth, - np.inf, + np.inf)
                if score < min_score:
                    min_score = score
                    best_hex = select_hex_name
                    # if best move lead to capture manipulate events
                    self.mark_best_capture_event()
                    best_events = self.game_logics.events[-3:]
                # print(f"player: {player}, score: {score}, min_hex: {best_hex}, min_score: {min_score}")
                # undo move
                player = self.game_logics.undo_events() 
        if (max_time) and ((time.time() - start_time) > int(max_time*60)):
            return min_score, best_hex, best_events
        # print(f"[Debug]-[play_agent]-best_hex: {best_hex}, last_score: {score}, min_score: {min_score}")
        # print("[DEBUG]-[play_agent]-[best_events]- last 5 events- \n")
        # pprint(best_events)          
        # trasnfer back copied game states to games_logics object
        return min_score, best_hex, best_events
    
    def play_agent(self, player, max_depth):
        """
        parent function that makes agent make the final move
        Agent - 2nd player
        """
        # copy game states before changes are made during the search
        self.copy_game_states(player)
        # iteratively increase search depth and find best move
        min_score, best_hex, best_events = self.iter_deep_search(player, max_depth)
        # transfer back the previous states
        player = self.trasfer_prev_game_states()

        # make the actual move based on search 
        # if the move leads to capture it will capture
        game_over, player, _  = self.agent_make_move(best_hex, player)
        if 'best_capture_hex' in best_events[-1]['move'].keys():
            capture_hex = best_events[-1]['move']['best_capture_hex']
            # call agent_make_move again to capture
            game_over, player, _  = self.agent_make_move(capture_hex, player)
       
        return game_over, player

class AgentMiniMaxTT(AgentMiniMaxID):
    """
    Agent has Minimax, alpha-beta, Iterative Deepening, Transposition tables
    """
    def __init__(self, game_variables, game_logics, geometry, trans_table):
        super().__init__(game_variables, game_logics, geometry)
        self.trans_table = trans_table
    
    def minimax_ab_TT(self, player: str, max_player: bool, select_hex_name: str, depth: int, alpha: int, beta: int) -> int:
        """
        # MiniMax, Alpha_Beta, Transposition Tables
        Always -> MAX -p1, MIN -p2
        """
        # Check the board if game is over and get trap positions
        game_over =  self.game_logics.check_game_over(player, select_hex_name)
        if game_over:
            if player == 'p1':
                return 10000
            elif player == 'p2':
                return -10000
            else:
                # draw scenario
                return 0

        # get the hash of the board state
        old_alpha = alpha
        old_beta = beta
        hash_digest = self.trans_table.get_hash_key(self.variables.HEX_GRID_FLAT_MAP[0], player)    
        # check if table_state, player combo exists in transposition table 
        # and it has results of deeper search
        if (self.trans_table.get_state_value(hash_digest) and (self.trans_table.get_state_value(hash_digest)[2] >= depth)):
            
            (ext_player_turn, score, ext_depth, flag_ind) = self.trans_table.get_state_value(hash_digest)
            # print(f"[DEBUG]-[minimax_ab_TT]- found matching entry in TT: {ext_player_turn, score, ext_depth, flag_ind}")
            if flag_ind == 'exact':
                return score
            elif flag_ind == 'lower_bound':
                alpha = max(alpha, score)
            elif flag_ind == 'upper_bound':
                beta = min(beta, score)
            if alpha>=beta:
                return score
            
        
        # get heuristic evaluation 
        if (depth <=0) and not(len(self.game_logics.detected_capture_moves) > 0):
            # player = self.game_logics.get_opponent_player(player)
            # print(f"[DEBUG]-[minimax]-depth==0: input_player: {player}, abs(score): {self.static_eval(player)}")
            # return value functions
            if player == 'p1':
                score = self.static_eval(player, select_hex_name)
            else:
                score = -(self.static_eval(player, select_hex_name))
            # save state information in TT
            # self.trans_table.store_state_value(hash_digest, player, score, depth, 'exact')
            return score
        # generate available moves of the player
        avilable_moves = self.get_valid_moves(player)
        if max_player == True:
            max_score = -np.inf
            # iterate through all available moves
            for move_index in range(avilable_moves.shape[0]):
                shifted_q, shifted_r = avilable_moves[move_index]
                # get the eqivalent hex name
                select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
                game_over, player, depth_reduce = self.agent_make_move(select_hex_name, player)
                player_turn = player # save the turn player(whose turn it is), as play will be switched
                score = self.minimax_ab_TT(player, False, select_hex_name, depth-depth_reduce, alpha, beta)
                # max_score = max(score, max_score)
                if score> max_score:
                    max_score=score
                    self.mark_best_capture_event()
                alpha = max(alpha, score)
                # undo move
                player = self.game_logics.undo_events()
                if alpha >= beta:
                    break
            # save state information in TT
            if max_score <= old_alpha:
                self.trans_table.store_state_value(hash_digest, player_turn, max_score, depth, 'upper_bound')
            elif max_score >= old_beta:
                self.trans_table.store_state_value(hash_digest, player_turn, max_score, depth, 'lower_bound')
            else:
                self.trans_table.store_state_value(hash_digest, player_turn, max_score, depth, 'exact')
            return max_score
        else:
            min_score = +np.inf
            # iterate through all available moves
            for move_index in range(avilable_moves.shape[0]):
                shifted_q, shifted_r = avilable_moves[move_index]
                # get the eqivalent hex name
                select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
                
                game_over, oppn_player, depth_reduce = self.agent_make_move(select_hex_name, player)
                player_turn = player # variables that go input to minimax will be arguments of TT
                score = self.minimax_ab_TT(player, True, select_hex_name, depth-depth_reduce, alpha, beta)
                # min_score = min(score, min_score)
                if score< min_score:
                    min_score=score
                    self.mark_best_capture_event()
                beta = min(beta, score)
                # undo move
                player = self.game_logics.undo_events()
                if alpha >= beta:
                    break
            # save state information in TT
            if min_score <= old_alpha:
                self.trans_table.store_state_value(hash_digest, player_turn, min_score, depth, 'upper_bound')
            elif min_score >= old_beta:
                self.trans_table.store_state_value(hash_digest, player_turn, min_score, depth, 'lower_bound')
            else:
                self.trans_table.store_state_value(hash_digest, player_turn, min_score, depth, 'exact')
            
            return min_score
    
    def iter_deep_search(self, player, max_depth, max_time: float = None):
        """
        Iteratively increase the depth of search
        Input: max_time - maximum allowed time in mintues, if both max depth and max time is given max time gets higher preference
        """
        min_score = + np.inf
        start_time = time.time()
        # generate all valid moves before each move
        avilable_moves = self.get_valid_moves(player)
        print(f"[Debug]-[play_agent]-avilable_moves len:{len(avilable_moves)}")    
        # refresh TT each time the user plays a new move
        self.trans_table.refresh_tt()
        for depth in tqdm(range(max_depth+1)): 
            print(f"\n[Debug]-[play_agent]-[ID]- depth: {depth}")
            # iterate through all available moves
            for move_index in tqdm(range(avilable_moves.shape[0])):
                shifted_q, shifted_r = avilable_moves[move_index]
                # get the eqivalent hex name
                select_hex_name = self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][-1]
                # print(f"[Debug]-[play_agent]-[ID]-player: {player}, select_hex_name: {select_hex_name}")
                # search best move
                game_over, oppn_player, _ = self.agent_make_move(select_hex_name, player)
                score = self.minimax_ab_TT(player, True, select_hex_name, depth, - np.inf, + np.inf)
                if score < min_score:
                    min_score = score
                    best_hex = select_hex_name
                    # if best move lead to capture manipulate events
                    self.mark_best_capture_event()
                    best_events = self.game_logics.events[-3:]
                # print(f"player: {player}, score: {score}, min_hex: {best_hex}, min_score: {min_score}")
                # undo move
                player = self.game_logics.undo_events()
            # print(f"[Debug]-[play_agent]-TT: total entries - {len(self.trans_table.tt_dict.keys())}")
            # pprint(self.trans_table.tt_dict)  
        if game_over:
            return min_score, best_hex, best_events
        if (max_time) and ((time.time() - start_time) > int(max_time*60)):
            return min_score, best_hex, best_events
        # print(f"[Debug]-[play_agent]-best_hex: {best_hex}, last_score: {score}, min_score: {min_score}")
        # print("[DEBUG]-[play_agent]-[best_events]- last 5 events- \n")
        # pprint(best_events)          
        # trasnfer back copied game states to games_logics object
        return min_score, best_hex, best_events
    
    
class TTable:
    """
    Transposition table: used to store and retrieve game states
    """
    def __init__(self,):
        self.tt_dict = {}
    
    def refresh_tt(self,):
        """
        Deletes the memery of TT
        """
        self.tt_dict = {}

    def get_hash_key(self, board_state, player_turn: str) -> str:
        """
        convert gameboard state and player turn to a hash key
        """
        hash_fn = hashlib.md5()
        # update a, update b has the same effect as update (a+b)
        hash_fn.update(str(board_state).encode('utf-8'))
        hash_fn.update(player_turn.encode('utf-8'))
        hash_digest = hash_fn.hexdigest()
        return hash_digest

    def store_state_value(self, hash_digest, player_turn, value, depth, ind_flag: str):
        """
        Stores the game states in Transposiotin tables
        """
        # hash_digest = self.get_hash_key(board_state, player_turn)
        if self.tt_dict.get(hash_digest): # entry already exists
            (ext_player_turn, ext_value, ext_depth, ind_flag) = self.tt_dict[hash_digest]
            if(depth > ext_depth):
                # as the value of depth-=1 reduces as the tree grows deeper 
                # depth > ext_depth: means the new depth is deeper
                self.tt_dict[hash_digest] = (player_turn, value, depth, ind_flag)
            else:
                pass
        else: # new entry
            self.tt_dict[hash_digest] = (player_turn, value, depth, ind_flag)

    def get_state_value(self, hash_digest):
        """
        Searches Transposition Table to retrieve existing value of the state
        """
        # hash_digest = self.get_hash_key(board_state, player_turn)
        if self.tt_dict.get(hash_digest): # entry already exists
            (ext_player_turn, ext_value, ext_depth, ind_flag) = self.tt_dict[hash_digest]
            return ext_player_turn, ext_value, ext_depth, ind_flag

if __name__ == "__main__":
    board_variables = BoardVariables()
    board_geometry = BoardGeometry(board_variables)
    trans_table = TTable()
    game_logics = GameLogics(board_variables, board_geometry)
    agent = Agent(board_variables, game_logics,)
    agent_ab = AgentMiniMax(board_variables, game_logics, board_geometry)
    agent_ID = AgentMiniMaxID(board_variables, game_logics, board_geometry)
    agnet_TT = AgentMiniMaxTT(board_variables, game_logics, board_geometry, trans_table)
