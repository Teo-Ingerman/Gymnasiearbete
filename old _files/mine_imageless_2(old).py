import random, copy
import mine_functions as mf


grids = []
solved_grids = mf.file_handling()

for grid in solved_grids:
    new_grid = mf.replace_all(grid, "c")
    mine_count = 0
    for row in grid:
        mine_count += row.count(-1)

    grids.append((grid, new_grid))




def solve_grid(current_grid, solved_grid, mine_count):
    
    def get_surrounding_squares(grid, position, return_state="all"):
        neighbors = []
        neighbors_position =[]
        row, col = position
        # Define the possible offsets for all eight surrounding squares
        offsets = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Up, down, left, right
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
        ]

        # Iterate over the offsets to get neighboring positions
        for offset_row, offset_col in offsets:
            neighbor_row = row + offset_row
            neighbor_col = col + offset_col

            # Check if the neighboring position is within the grid bounds
            if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):
                neighbors.append(grid[neighbor_row][neighbor_col])
                neighbors_position.append((neighbor_row, neighbor_col))


        if return_state == "all":
            return neighbors, neighbors_position
        
        if return_state == "pos":
            return neighbors_position

        if return_state == "value":
            return neighbors
    
    def open_square(position, current_game_state, current_game_solved, value=None):
        row, column = position
        if value == None:
            current_game_state[row][column] = current_game_solved[row][column]
        else:
            current_game_state[row][column] = value
        return current_game_state
    
    
    
    
    game_sequence = []
    
    while True:
        start_position = (random.randint(0, len(current_grid)-1), random.randint(0, len(current_grid[0])-1))
        if solved_grid[start_position[0]][start_position[1]] != 0:
            
            continue
        break


    current_grid = open_square(start_position, current_grid, solved_grid)
    game_sequence.append(copy.deepcopy(current_grid))


    # main loop
    running = True

    while running:
        
        relevant_squares = []
        
        mines_discovered = 0
        
        for i, _ in enumerate(current_grid):
            for j, value in enumerate(current_grid[i]):
                pos = (i, j)

                
                if value == "f":
                    mines_discovered += 1
                    continue
                
                if value == "c":
                    continue
                
                surround_value, surround_pos = get_surrounding_squares(current_grid, pos)
                
                if surround_value.count("c") == 0:
                    continue
                
                    
                if value == 0:
                    for position in surround_pos:
                        row, column = position
                        
                        if current_grid[row][column] != "c":
                            continue
                        
                        relevant_squares.append(position)
                    continue
                
                
                # checks if if there are the same amount of uncovered squares and bombs as the number 
                bomb_check = value - surround_value.count("c") - surround_value.count("f")
                
                if bomb_check == 0:
                    for index, value in enumerate(surround_value):
                        if value != "c":
                            continue
                        
                        current_grid = open_square(surround_pos[index], current_grid, solved_grid, value="f")
                        game_sequence.append(copy.deepcopy(current_grid))
                        
                    
                    continue
                
                
                # removes the the covered squares if the amount of bombs is equal to the number
                if value == surround_value.count("f"):
                    for index, value in enumerate(surround_value):
                        if value != "c":
                            continue
                        
                        relevant_squares.append(surround_pos[index])

                    
                    continue
        
        
    
        
        
        
        # if len(relevant_squares) == 0 and mines_discovered != mine_count:
        #     # running = False
        #     return False
                 
        if len(relevant_squares) == 0:
            running = False
        
               
        # print(relevant_squares)
        for position in relevant_squares:
            current_grid = open_square(position, current_grid, solved_grid)
            game_sequence.append(copy.deepcopy(current_grid))
            
          

        game_sequence.append(copy.deepcopy(current_grid))
    
    
    def convert_to_tuple(obj):
        if isinstance(obj, list):
            return tuple(convert_to_tuple(item) for item in obj)
        else:
            return obj

    def has_duplicates(list_of_lists):
        seen = set()
        for sublist in list_of_lists:
            sublist_tuple = convert_to_tuple(sublist)
            if sublist_tuple in seen:
                return True
            seen.add(sublist_tuple)
        return False


    def remove_duplicates(list_of_lists):
        seen = set()
        unique_list = [x for x in list_of_lists if convert_to_tuple(x) not in seen and not seen.add(convert_to_tuple(x))]
        return unique_list
    
    
    if has_duplicates(game_sequence):
        game_sequence = remove_duplicates(game_sequence)
    
    
    covered = 0

    for row in current_grid:
        covered += row.count("c")
    if covered == 0:
        # print("Solved")
        return game_sequence
        
    return False
                
    

    
failure = 0 
finished_games = []   

for solved_grid, unsolved_grid in grids:
    
    
    mine_count = int((len(solved_grid)*len(solved_grid[0]))*0.1)
    
    sequence = solve_grid(unsolved_grid, solved_grid, mine_count)
    
    
    if sequence:
        finished_games.append(sequence)
    else:
        failure += 1
        


mf.file_handling(finished_games, "w", "finished_games")
print(f"failure: {failure}")

        
    

