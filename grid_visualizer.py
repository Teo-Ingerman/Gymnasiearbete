import mine_functions as mf


combo = mf.json_data_handler(None, "finished_grids", "read")


grid, sequence = combo[0]


# grid_array = mf.json_data_handler(None, "C#_code/minesweeper_grid", "read")

# for row in grid_array:
#     for col in row:
#         if col == -1:
#             print(f"X ", end="")
#             continue
#         print(f"{col} ", end="")
#     print("")


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