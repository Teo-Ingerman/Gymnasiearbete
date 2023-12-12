import mine_functions as mf

rows = int(input("rows: "))
columns = int(input("columns: "))
grids = int(input("grids: "))


mf.json_data_handler([mf.create_minesweeper_grid(rows, columns) for _ in range(grids)], "generated_grids")




# grids = mf.json_data_handler(None, "generated_grids", "read")

# mf.display_minesweeper_game_sequence(grids)