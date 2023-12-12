import mine_functions as mf
import time



if __name__ == "__main__":
    
    # starts the time chekcer
    start = time.time()

    
    # Loads the generated grids 
    generated_grids = mf.json_data_handler(None, "generated_grids", "read")


    # Solves all the grids
    solved_grids = []

    for grid in generated_grids:

        solve_squence = mf.solve_grid(grid)

        # Checking if grid gets solved, if not function returns None

        if type(solve_squence) == list:

            # saves the solved grid and the sequence to solve it as a tuple
            solved_grids.append((grid, solve_squence))


    # saving the solved grids to a json file
    mf.json_data_handler(solved_grids, "finished_grids")

    # displays the time
    end = time.time()
    print(mf.display_time(start, end))

