# Example usage:
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

n_rows, n_cols = len(matrix[0]), len(matrix) # 4,4
q,r = 2,2

anti_diag_index = [[q,r]]

row_index = q
col_index = r

row_index +=1
col_index -=1
while(row_index<n_rows and col_index>=0):
    anti_diag_index.append([row_index, col_index])
    row_index +=1
    col_index -=1

row_index = q
col_index = r

row_index -=1
col_index +=1
# anti_diag_index
while(row_index>=0 and col_index<n_cols):
    anti_diag_index.append([row_index, col_index])
    row_index -=1
    col_index +=1

print(anti_diag_index)
print("Sorted version")
print(sorted(anti_diag_index, key=lambda x: x[0]))