import mine_functions as mf
import time, copy, random




# sequence = mf.file_handling(type="r", file_choice="finished_games")

# mf.display_minesweeper_game_sequence(sequence[0])


# quit()






def get_neighbors(grid, position):
    neighbors = []
    neighbors_position =[]
    row, col = position

    # Define the possible offsets for neighboring squares
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Iterate over the offsets to get neighboring positions
    for offset_row, offset_col in offsets:
        neighbor_row = row + offset_row
        neighbor_col = col + offset_col

        # Check if the neighboring position is within the grid bounds
        if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):
            neighbors.append(grid[neighbor_row][neighbor_col])
            neighbors_position.append((neighbor_row, neighbor_col))

    return neighbors, neighbors_position

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


def click_square(position, current_game_state, current_game_solved):

    # value and position of neighboring squares
    values, pos = get_neighbors(current_game_solved, position)
    print(len(values))
    # If there's an empty square check the surrounding squares until all empty connecting squares and the numbered squares on the edges are opened
    for i, value in enumerate(values):
        
        row, column = pos[i]
        
        if row < 0 or column < 0:
            print(row, column)
            continue
        
        if value == -1:
            raise RuntimeError("something went wrong, bomb is not suppupsed to be here!")
            
        if value != 0:
            current_game_state[row][column] = current_game_solved[row][column]
            
            continue
        
        if current_game_state[row][column] == current_game_solved[row][column]:
            print("work")
            continue
        
        current_game_state[row][column] = current_game_solved[row][column]
        current_game_state = click_square(pos[i], current_game_state, current_game_solved)
        
    empty_squares = []
            
    for i in current_game_state:
        for j, square in enumerate(i):
            if square == 0:
                empty_squares.append((i, j))
    
    
    for pos in empty_squares:
        squares = get_surrounding_squares(current_game_solved, pos)
        for square in squares:
            row, column = pos
            if square == -1:
                continue
            current_game_state[row][column] = current_game_solved[row][column]
    
    
    
    
    return current_game_state

    
def open_square(position, current_game_state, current_game_solved, value=None):
    row, column = position
    if value == None:
        current_game_state[row][column] = current_game_solved[row][column]
    else:
        current_game_state[row][column] = value
    return current_game_state




width = int(input("width: "))
height = int(input("height: "))
grid_amount = int(input("grid amount: "))
mine_count = int((width*height) * 0.1)
print(mine_count)
start = time.time()

grids = []

for i in range(grid_amount):
    grids.append(mf.create_minesweeper_grid(height, width, mine_count, True))
  
  
mf.file_handling(grids, "w", "data")
quit()
    
    
    
grid_cover = mf.replace_all(grid_mine_positions, "c")
grids.append(grid_mine_positions, grid_cover)















game_sequence = []


current_grid = grid_cover


# making sure the first square is not a mine
while True:
    start_position = (random.randint(0, len(current_grid)-1), random.randint(0, len(current_grid[0])-1))
    if grid_mine_positions[start_position[0]][start_position[1]] != 0:
        
        continue
    break


current_grid = open_square(start_position, current_grid, grid_mine_positions)
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
                    
                    current_grid = open_square(surround_pos[index], current_grid, grid_mine_positions, value="f")
                    game_sequence.append(copy.deepcopy(current_grid))
                    
                
                continue
            
            
            # removes the the covered squares if the amount of bombs is equal to the number
            if value == surround_value.count("f"):
                for index, value in enumerate(surround_value):
                    if value != "c":
                        continue
                    
                    relevant_squares.append(surround_pos[index])

                
                continue

    
    if len(relevant_squares) == 0:
        running = False         
                    
    # print(relevant_squares)
    for position in relevant_squares:
        current_grid = open_square(position, current_grid, grid_mine_positions)
        game_sequence.append(copy.deepcopy(current_grid))
        
    if mines_discovered == mine_count:
        running = False
        print("Done")    

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


end = time.time()
time_elapsed = end - start


if time_elapsed < 60:
    print(f"{round(time_elapsed, 2)} s")

if time_elapsed > 60:
    seconds = round(time_elapsed % 60, 2)
    minutes = (time_elapsed - seconds)/60
    print(f"{minutes} m {seconds} s")
   
print(len(game_sequence))

print(has_duplicates(game_sequence))

if has_duplicates(game_sequence):
    game_sequence = remove_duplicates(game_sequence)

print(len(game_sequence))


mf.display_minesweeper_game_sequence(game_sequence)