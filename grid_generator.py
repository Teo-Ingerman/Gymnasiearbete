import mine_functions as mf

rows = int(input("rows: "))
columns = int(input("columns: "))
grids = int(input("grids: "))


mf.json_data_handler([mf.create_minesweeper_grid(rows, columns) for _ in range(grids)], "generated_grids")





