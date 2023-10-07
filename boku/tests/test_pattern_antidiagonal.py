import numpy as np

def find_pattern_in_anti_diagonals(grid_flat_map, pattern, n):
    rows, cols = grid_flat_map.shape
    original_indices_list = []
    for i in range(rows - n + 1):
        for j in range(cols - n + 1):
            anti_diagonal = np.fliplr(grid_flat_map[i:i+4, j:j+4]).diagonal()
            if list(anti_diagonal) == pattern:
                # Pattern matched; now find the original indices
                original_indices = [(i + k, j + 4 - k - 1) for k in range(4)]
                original_indices_list.append(original_indices)
        
        anti_diagonal = np.fliplr(grid_flat_map[i:i+4, j+1:j+1+4]).diagonal()
        if list(anti_diagonal) == pattern:
            # Pattern matched; now find the original indices
            original_indices = [(i + k, j+1 + 4 - k - 1) for k in range(4)]
            original_indices_list.append(original_indices)
            
    # consider one more case with i+1 and iterate over all j
    for j in range(cols - 4 + 1):
        print(f"Case-i+1,{j}: square - \n", grid_flat_map[i+1:i+1+4, j:j+4])
        anti_diagonal = np.fliplr(grid_flat_map[i+1:i+1+4, j:j+4]).diagonal()
        if list(anti_diagonal) == pattern:
            # Pattern matched; now find the original indices
            original_indices = [(i+1 + k, j + 4 - k - 1) for k in range(4)]
            original_indices_list.append(original_indices)

    return original_indices_list

# Example usage:
grid_flat_map = np.array([[1, 2, 3, 4, 5],
                          [6, 7, 3, 9, 3],
                          [1, 7, 3, 7, 5],
                          [1, 7, 1, 9, 2],
                          [1, 6, 9, 7, 5]
                          ])

pattern = [3,7,1]
n = 4

original_indices_list = find_pattern_in_anti_diagonals(grid_flat_map, pattern, n)

if len(original_indices_list):
    print("Pattern found in anti-diagonals at indices:", len(original_indices_list))
    print(original_indices_list, sep='\n')
else:
    print("Pattern not found.")
