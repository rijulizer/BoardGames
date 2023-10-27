# test hashing 
# import hashlib
# a = [1,2,3]

# hash_fn = hashlib.md5()
# hash_fn.update(str(a).encode('utf-8'))

# hash_op = hash_fn.hexidigest()
# print(hash_op)


import numpy as np
grid_flat_map = [
    [None, None, None, None, None, 0, 0, 0, 0, 0],
    [None, None, None, None, -1, 0, 0, 0, 0, 0],
    [None, None, None, 0, -1, 0, 0, 0, 0, 0],
    [None, None, 0, 0, -1, 0, 0, 0, 0, 0],
    [None, 0, 0, 0, -1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, None],
    [0, 0, 0, 0, 0, 0, 0, 0, None, None],
    [0, 0, 0, 0, 0, 0, 0, None, None, None],
    [0, 0, 0, 0, 0, 0, None, None, None, None],
    [0, 0, 0, 0, 0, None, None, None, None, None]
    ]
player = "p1"

import hashlib
class TTable:
    def __init__(self,):
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

    def store_state_value(self, board_state, player_turn, value, depth):
        """
        Stores the game states in Transposiotin tables
        """
        hash_digest = self.get_hash_key(board_state, player_turn)
        if self.tt_dict.get(hash_digest): # entry already exists
            (ext_player_turn, ext_value, ext_depth) = self.tt_dict[hash_digest]
            if(ext_depth > depth):
                # as the value of depth-=1 rediced as the tree grows deeper 
                # ext_depth > depth: means the new depth is lower ie, deeper
                self.tt_dict[hash_digest] = (player_turn, value, depth)
        else: # new entry
            self.tt_dict[hash_digest] = (player_turn, value, depth)

    def get_state_value(self, board_state, player_turn,):
        """
        Searches Transposition Table to retrieve existing value of the state
        """
        hash_digest = self.get_hash_key(board_state, player_turn)
        if self.tt_dict.get(hash_digest): # entry already exists
            (ext_player_turn, ext_value, ext_depth) = self.tt_dict[hash_digest]
            return ext_value
        
        
trans_table = TTable()
print(trans_table.get_hash_key(grid_flat_map, player))
trans_table.store_state_value(grid_flat_map, player, 5, 2)
print(trans_table.tt_dict)
print(trans_table.get_state_value(grid_flat_map, player))

trans_table.store_state_value(grid_flat_map, player, 2, 3)
print(trans_table.tt_dict)
print(trans_table.get_state_value(grid_flat_map, player))

trans_table.store_state_value(grid_flat_map, player, 7, 1)
print(trans_table.tt_dict)
print(trans_table.get_state_value(grid_flat_map, player))
