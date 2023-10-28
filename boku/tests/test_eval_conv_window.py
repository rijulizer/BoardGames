# p1 -          >  1
# empty space - >  0
# p2 -          > -1

# The 5 in a row case will be an end game and will be picked up.
# So only think about 4 in a row.
# evaluate based on the current move, current player.

# main idea if a current move increases the chances of puting tokens in the same line.

# after putting a token(1) twas put in 2nd position he pattern becomes as the different cases
# case_1 = [
#     [1,1,1,1],
#     [1,0,1,1],
#     [1,1,1,0],
#     [1,-1,1,1],
#     [-1,1,1,1],
#     [1,-1,1,0],
# ]
# window: w1 = [1,1,1,1]
# # token(1) was put in 2nd position Convolution
# [1,1,|1|,1] . [1,1,|1|,1] = 4
# [1,0,|1|,1] . [1,1,|1|,1] = 3
# [1,1,|1|,0] . [1,1,|1|,1] = 3
# [1,-1,|1|,1]. [1,1,|1|,1] = 2
# [-1,1,|1|,1]. [1,1,|1|,1] = 2
# [1,-1,|1|,0]. [1,1,|1|,1] = 1

# # token(1) was put in 2nd position Convolution
# [|1|,1,1,1] . [|1|,1,1,1] = 4
# [|1|,0,1,1] . [|1|,1,1,1] = 3
# [|1|,1,1,0] . [|1|,1,1,1] = 3
# [|1|,-1,1,1]. [|1|,1,1,1] = 2
# [|1|,-1,1,0]. [|1|,1,1,1] = 1
# [|1|,-1,-1,0].[|1|,1,1,1] = -1
# [|1|,0,-1,0]. [|1|,1,1,1] = -1

import numpy as np
grid_flat_map = [
    [None, None, None, None, None, 0, 0, 0, 0, 0],
    [None, None, None, None, -1, -2, -4, 0, 0, 0],
    [None, None, None, 0, -1, -3, -5, 0, 0, 0],
    [None, None, 0, 0, -1, -8, 0, 0, 0, 0],
    [None, 0, 0, 0, -1, 0, 0, 0, 0, 0],
    [1, 2, 1, 3, 1, 5, 0, 6, 0, 9],
    [0, 5, 0, 4, 0, 0, 0, 0, 8, None],
    [0, 1, 0, 4, 0, 0, 0, 0, None, None],
    [0, 6, 3, 0, 0, 0, 0, None, None, None],
    [0, 0, 0, 0, 0, 0, None, None, None, None],
    [1, 8, 0, 0, 0, None, None, None, None, None]
    ]
player = "p1"
pos = [5,4]
shifted_q, shifted_r = pos
player_symbol = 1 
n = 5
n_rows, n_cols = len(grid_flat_map), len(grid_flat_map[0])
grid_flat_map = np.array(grid_flat_map)

# get the lines 

# def get_lines_point():
# """
# For a given point in 2d array, get the column, row and antidiagonal thourgh the point
# """
# shifted_q, shifted_r = self.geometry.get_flat_map_gird(pos)
# grid_flat_map = np.array(self.variables.HEX_GRID_FLAT_MAP[0])
n_rows, n_cols = len(grid_flat_map), len(grid_flat_map[0])

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

row_index = shifted_q - 1
col_index = shifted_r + 1
# anti_diag_index
while(row_index>=0 and col_index<n_cols):
    anti_diag_index.append([row_index, col_index])
    row_index -=1
    col_index +=1
sorted_anti_diag_index = sorted(anti_diag_index, key=lambda x: x[0])
# get the position of the point in sorted_anti_diag_index 
pos_adiag = shifted_q = np.where((sorted_anti_diag_index==np.array([shifted_q, shifted_r])).all(axis=1))[0][0]
anti_diag_elems = []
for row, col in sorted_anti_diag_index:
    anti_diag_elems.append(grid_flat_map[row, col])
anti_diag_elems = np.array(anti_diag_elems)
# return [shifted_q_row, shifted_r_col, anti_diag_elems, pos_adiag]

# [shifted_q_row, shifted_r_col, anti_diag_elems, pos_adiag] = get_lines_point()

print([shifted_q_row, shifted_r_col, anti_diag_elems, pos_adiag])


# get all possible windows in row - shifted_q_row
# shifted_q_row = [1, 2, 1, 3, 1, 5, 0, 6, 0, 9], move |2|
# check how many tokens are on left and on right, consider board boundery cases
# l_lim = len(shifted_q_row[:shifted_r+1]) # includes nones
# l_lim = min(l_lim, 4)
# r_lim = len(shifted_q_row[shifted_r:])
# r_lim = min(r_lim, 4)
# print(l_lim, r_lim)
# r_windows = []
# for i in range((shifted_r+1 - l_lim), ((shifted_r + r_lim - 4)+1)):
#     print(shifted_q_row[i:i+4])
#     if (None not in shifted_q_row[i:i+4]) and (len(shifted_q_row[i:i+4])==4):
#         r_windows.append(shifted_q_row[i:i+4])
# print(r_windows)


# get all possible windows in col - shifted_r_row
# shifted_q_row = [None None None None 0 2 5 1 6 0 8], pos = [7,1]
# print(shifted_r_col)
# l_lim = len(shifted_r_col[:shifted_q+1]) # includes nones
# l_lim = min(l_lim, 4) 
# r_lim = len(shifted_r_col[shifted_q:]) # includes nones
# r_lim = min(r_lim, 4)
# print(l_lim, r_lim)
# c_windows = []
# for i in range((shifted_q+1 - l_lim), ((shifted_q + r_lim - 4)+1)):
#     print(shifted_r_col[i:i+4])
#     # must not contain Nones and addition must be len 4
#     if (None not in shifted_r_col[i:i+4]) and (len(shifted_r_col[i:i+4])==4):
#         c_windows.append(shifted_r_col[i:i+4])
# print(c_windows)


# print("anti_diag_index", anti_diag_index)
# print("sorted_anti_diag_index",sorted_anti_diag_index) 
# find the original tokens position in the sorted antidiagonal elements
# print(np.where((sorted_anti_diag_index==np.array(pos)).all(axis=1))[0])
# # get all possible windows in antidiagonal - shifted_r_row
# # anti_diag_elems = [ 0  0 -5 -8 -1  3  0  1  0] pos = [5,3], elem- 3
# shifted_r_col = anti_diag_elems
# shifted_q = np.where((sorted_anti_diag_index==np.array(pos)).all(axis=1))[0][0]
# print(anti_diag_elems, shifted_q)
# l_lim = len(shifted_r_col[:shifted_q+1]) # includes nones
# l_lim = min(l_lim, 4) 
# r_lim = len(shifted_r_col[shifted_q:]) # includes nones
# r_lim = min(r_lim, 4)
# print(l_lim, r_lim)
# c_windows = []
# for i in range((shifted_q+1 - l_lim), ((shifted_q + r_lim - 4)+1)):
#     print(shifted_r_col[i:i+4])
#     # must not contain Nones and addition must be len 4
#     if (None not in shifted_r_col[i:i+4]) and (len(shifted_r_col[i:i+4])==4):
#         c_windows.append(shifted_r_col[i:i+4])
# print(c_windows)
from pprint import pprint 
# get different direction of lines
same_lines = [shifted_q_row, shifted_r_col, anti_diag_elems]
# euivalent point index in each direction
point_poss = [shifted_r, shifted_q, pos_adiag]
line_windows = []
for same_line, point_pos in zip(same_lines, point_poss):
    print("#################")
    l_lim = len(same_line[:point_pos+1]) # includes nones
    l_lim = min(l_lim, 4)
    r_lim = len(same_line[point_pos:])
    r_lim = min(r_lim, 4)
    print(l_lim, r_lim)
    dir_windows = []
    for i in range((point_pos+1 - l_lim), ((point_pos + r_lim - 4)+1)):
        # print(same_line[i:i+4])
        if (None not in same_line[i:i+4]) and (len(same_line[i:i+4])==4):
            dir_windows.append(same_line[i:i+4])
    line_windows.append(dir_windows)
    # pprint(dir_windows)
line_windows = np.array(line_windows).reshape(-1, 4)
pprint(line_windows)
filter_p1 = np.array([1,1,1,1])
filter_p2 = np.array([-1,-1,-1,-1])
max_conv = -np.inf
for win in line_windows:
    conv_fp1 = np.dot(win, filter_p1)
    conv_fp2 = np.dot(win, filter_p2)
    max_conv = max(max_conv, conv_fp1)
    print(win, filter_p1, conv_fp1, filter_p2, conv_fp2, max_conv)

