import mine_functions as mf

rows = int(input("rows: "))
columns = int(input("columns: "))
grids = int(input("grids: "))

def get_dimensions(lst):
    if not isinstance(lst, list):
        # If it's not a list, it's a scalar (0 dimensions)
        return 0
    elif not lst:
        # If it's an empty list, return 1 dimension
        return 1
    else:
        # Recursively find dimensions for each element in the list
        sub_dimensions = [get_dimensions(item) for item in lst]
        # Return the maximum dimension found in the list
        return 1 + max(sub_dimensions)


multi_dim_list = [mf.create_minesweeper_grid(rows, columns) for _ in range(grids)]


print(get_dimensions(multi_dim_list))


mf.json_data_handler(multi_dim_list, "generated_grids")




# grids = mf.json_data_handler(None, "generated_grids", "read")

# mf.display_minesweeper_game_sequence(grids)