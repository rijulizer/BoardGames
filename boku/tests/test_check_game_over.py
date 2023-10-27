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
pos = [5,0]
shifted_q, shifted_r = pos
player_symbol = 1 
n = 5
n_rows, n_cols = len(grid_flat_map), len(grid_flat_map[0])
grid_flat_map = np.array(grid_flat_map)
# get the row (q), col(r) of the move in falt_map
shifted_q_row  = grid_flat_map[shifted_q,:]
shifted_r_col  = grid_flat_map[:,shifted_r]

# Check the antidiagonal
# collect [row, col] of the antidiagonal containing [shifted_q, shifted_r]
anti_diag_index = [[shifted_q, shifted_r]]

row_index = shifted_q + 1
col_index = shifted_r - 1
while(row_index<n_rows and col_index>=0):
    anti_diag_index.append([row_index, col_index])
    row_index +=1
    col_index -=1

# row_index = shifted_q - 1
# col_index = shifted_r + 1
# # anti_diag_index
# while(row_index>=0 and col_index<n_cols):
#     anti_diag_index.append([row_index, col_index])
#     row_index -=1
#     col_index +=1
# sorted_anti_diag_index = sorted(anti_diag_index, key=lambda x: x[0])
anti_diag_elems = []
# for row, col in sorted_anti_diag_index:
#     anti_diag_elems.append(grid_flat_map[row, col])
anti_diag_elems = np.array(anti_diag_elems)
# for elem in [row, col, anti_diag_elems]:
#     # check if it has more than n number of elements in the row/col/
#     count_player_symbol = np.count_nonzero(elem == player_symbol)
#     if count_player_symbol >= n:
#         # check for contiguous occurences 
#         for i in range(len(elem) - n + 1):
#             if all(elem[i:i+n] == player_symbol):
# for elem in [shifted_q_row, shifted_r_col, anti_diag_elems]:
#     # check if it has more than n number of elements in the row/col/
#     count_player_symbol = np.count_nonzero(elem == player_symbol)
#     if count_player_symbol >= n:
#         # check for contiguous occurences 
#         for i in range(len(elem) - n + 1):
#             if all(elem[i:i+n] == player_symbol):
#                 print(True)
#                        
# def check_game_over(self, player: str, pos: str):
#         """
#         Check if game is over after player makes a particular move
#         # 5 contigous tokens in same line, but only check the lines where player just moved.
#         Input: Player = current player, pos(hex_name) = latest move of current player
#         """
#         shifted_q, shifted_r = self.geometry.get_flat_map_gird(pos)
#         grid_flat_map = np.array(self.variables.HEX_GRID_FLAT_MAP[0])
#         player_symbol = self.variables.PLAYERS[player]['symbol']
#         n = self.variables.boku_rule_cont_pos
#         n_rows, n_cols = len(grid_flat_map), len(grid_flat_map[0])
        
#         # get the row (q), col(r) of the move in falt_map
#         row  = grid_flat_map[shifted_q,:]
#         col  = grid_flat_map[:,shifted_r]
    
#         # Check the antidiagonal
#         # collect [row, col] of the antidiagonal containing [shifted_q, shifted_r]
#         anti_diag_index = [[shifted_q, shifted_r]]

#         row_index = shifted_q + 1
#         col_index = shifted_r - 1
#         while(row_index<n_rows and col_index>=0):
#             anti_diag_index.append([row_index, col_index])
#             row_index +=1
#             col_index -=1

#         row_index = shifted_q - 1
#         col_index = shifted_r + 1
#         # anti_diag_index
#         while(row_index>=0 and col_index<n_cols):
#             anti_diag_index.append([row_index, col_index])
#             row_index -=1
#             col_index +=1
#         sorted_anti_diag_index = sorted(anti_diag_index, key=lambda x: x[0])
#         anti_diag_elems = []
#         for row, col in sorted_anti_diag_index:
#             anti_diag_elems.append(grid_flat_map[row, col])
        
#         for elem in [row, col, anti_diag_elems]:
#             # check if it has more than n number of elements in the row/col/
#             count_player_symbol = np.count_nonzero(elem == player_symbol)
#             if count_player_symbol >= n:
#                 # check for contiguous occurences 
#                 for i in range(len(elem) - n + 1):
#                     if all(elem[i:i+n] == player_symbol):
#                             return True, []# dummy [] TODO: delete [] later
#         return False, []
                
    