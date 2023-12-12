import mine_functions as mf
import time



if __name__ == "__main__":
    
    # starts the time chekcer
    start = time.time()


    # Loads the generated grids 
    generated_grids = mf.json_data_handler(None, "generated_grids", "read")


    # Makes a default covered version of the grids
    default_grid = mf.switch_values(generated_grids[0], "c")


    solved_grids = []

    for grid in generated_grids:

        solved_grid = mf.solve_grid(default_grid, grid)

        if type(solved_grid) == list:
            solved_grids.append(solved_grid)



    end = time.time()


    mf.display_time(start, end)

