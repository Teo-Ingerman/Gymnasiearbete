import mine_functions as mf


combo = mf.json_data_handler(None, "finished_grids", "read")


grid, sequence = combo[0]
# print(sequence)

# def find_missing_values(matrix):
#     positions_set = set(matrix)
#     missing_values = []

#     for i in range(len(matrix)):
#         for j in range(len(matrix[i])):
#             if [i, j] not in positions_set:
#                 missing_values.append([i, j])

#     return missing_values



# print(find_missing_values(sequence))


mf.display_minesweeper_grid(grid, sequence)