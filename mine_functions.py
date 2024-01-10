import pygame, sys, random, json, win32gui, pyautogui, ctypes


def create_minesweeper_grid(rows, cols, advanced=True):

    num_mines = int(rows*cols*0.15)

    # Initialize an empty grid filled with zeros
    """advanced variable makes the grid get all number in the grid"""
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Randomly place a portion of mines to ensure solvability
    initial_mines = int(0.1 * rows * cols)  # 10% of the total cells
    for _ in range(initial_mines):
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        grid[row][col] = -1  # Place a mine

    # Calculate the number of remaining mines to place
    remaining_mines = num_mines - initial_mines

    # Randomly place the remaining mines while avoiding marked safe cells
    while remaining_mines > 0:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        # Check if the cell is already a mine or a marked safe cell
        if grid[row][col] == -1 or grid[row][col] > 0:
            continue

        grid[row][col] = -1  # Place a mine
        remaining_mines -= 1

    if advanced:
        visual_list = []
        for x in range(len(grid)):
            temp_list = []
            for pos, value in enumerate(grid[x]):
                
                surround_value = 0
                
                if value == -1:
                    temp_list.append(-1)
                    continue
                    
                
                    # General case
                for i in range(x-1,x+2):
                    
                    for j in range(pos-1, pos+2):
                        
                        if i == -1 or j == -1:
                            continue
                        
                        try:
                            surround_value -= grid[i][j]
                        except IndexError:
                            pass

                temp_list.append(surround_value)
        
            visual_list.append(temp_list)
        grid = visual_list

    return grid

def display_minesweeper_game_sequence(boards):
    pygame.init()
    board = boards[0]  # Initialize with the first board
    board_index = 0

    # Define cell size and gap
    CELL_SIZE = screen_height = (pyautogui.size().height)/(len(board)+10)
    SCALE_SIZE = (CELL_SIZE, CELL_SIZE)

    screen_width = len(board[0]) * (CELL_SIZE)
    screen_height = len(board) * (CELL_SIZE)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Minesweeper Playback")

    # Load images
    
    # mine_image = pygame.transform.scale(pygame.image.load("images/-1.png"), SCALE_SIZE)
    # revealed_image = pygame.transform.scale(pygame.image.load("images/0.png"), SCALE_SIZE)
    # number_images = [pygame.transform.scale(pygame.image.load(f"images/{i}.png"), SCALE_SIZE) for i in range(1, 9)]
    # concealed_image = pygame.transform.scale(pygame.image.load("images/concealed.png"), SCALE_SIZE)
    # flag_image = pygame.transform.scale(pygame.image.load("images/flag.png"), SCALE_SIZE)

    revealed_image = pygame.transform.scale(pygame.image.load("highres_images/Tile_Flat.png"), SCALE_SIZE)
    concealed_image = pygame.transform.scale(pygame.image.load("highres_images/Tile_1.png"), SCALE_SIZE)
    flag_image = pygame.transform.scale(pygame.image.load("highres_images/Skull.png"), SCALE_SIZE)
    number_images = [pygame.transform.scale(pygame.image.load(f"highres_images/Number_{i}.png"), SCALE_SIZE) for i in range(1, 9)]


    
    win_w = (len(board))*CELL_SIZE
    win_h = (len(board))*CELL_SIZE

    x = round((pygame.display.Info().current_w - win_w) / 2)
    y = round((pygame.display.Info().current_h - win_h) / 2 * 0.8)  # 80 % of the actual height

    # pygame screen parameter for further use in code
    screen = pygame.display.set_mode((win_w, win_h))

    # Set window position center-screen and on top of other windows
    # Here 2nd parameter (-1) is essential for putting window on top
    win32gui.SetWindowPos(pygame.display.get_wm_info()["window"], -1, x, y, 0, 0, 1)


    clock = pygame.time.Clock()
    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        screen.fill((255, 255, 255))

        for row in range(len(board)):
            for col in range(len(board[row])):
                cell_value = board[row][col]
                x = col * (CELL_SIZE)
                y = row * (CELL_SIZE)

                if cell_value == "c":
                    screen.blit(concealed_image, (x, y))
                elif cell_value == "f":
                    screen.blit(flag_image, (x, y))
                elif cell_value == -1:
                    screen.blit(flag_image, (x, y))
                
                else:
                    if cell_value > 0:
                        number_image = number_images[cell_value - 1]
                        screen.blit(number_image, (x, y))
                    else:
                        screen.blit(revealed_image, (x, y))
                    

        pygame.display.flip()
        clock.tick(10)  # Change the frame rate as needed
        board_index += 1
        print(board_index)
        if board_index < len(boards):
            board = boards[board_index]
        else:
            # playing = False
            board = boards[-1]

    pygame.quit()
    sys.exit()

def switch_values(original_list, new_value):
    # Base case: if the element is not a list, replace it with new_value
    if not isinstance(original_list, list):
        return new_value

    # Recursively call switch_values for each element in the list
    return [switch_values(element, new_value) for element in original_list]

def json_data_handler(data, filename, mode="write"):
    # Add ".json" extension to the filename if it doesn't have one
    if not filename.endswith(".json"):
        filename += ".json"

    try:
        if mode == "write":
            with open(filename, "w") as file:
                json.dump(data, file, indent=2)
            print(f"Data successfully stored in {filename}")

        elif mode == "read":
            with open(filename, "r") as file:
                read_data = json.load(file)
            return read_data
        else:
            print('Invalid mode. Use "write" or "read".')
    except Exception as e:
        print(f"Error: {e}")
        return None

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

def solve_grid(open_grid):
    # Makes a default covered version of the grid
    closed_grid = switch_values(open_grid, "c")

    # Calculating the total amount of mines
    total_mines = 0

    for row in open_grid:
        total_mines += row.count(-1)

    
    def open_square(pos):
        closed_grid[pos[0]][pos[1]] = open_grid[pos[0]][pos[1]]
    

    # Choosing a valid starting square
    while True:
        start_pos = (random.randint(0, len(open_grid)-1), random.randint(0, len(open_grid[0])-1))
        
        if open_grid[start_pos[0]][start_pos[1]] != 0:
            continue
        open_square(start_pos)
        break
            
    
    # Starting the main loop
    reveal_sequence = []
    
    running = True

    while running:


        squares_to_open = []
        # keeping the mines discovered counted
        mines_discovered = 0

        for i, _ in enumerate(closed_grid):
            for j, value in enumerate(closed_grid[i]):
                pos = (i, j)


                #  if all mines are discovered the remaining covered squares are safe
                if mines_discovered == total_mines and value == "c":
                    squares_to_open.append(pos)

                # if the square is covered or a bomb it skips it
                if value == "c" or value == -1:
                    continue
                
                surround_value, surround_pos = get_surrounding_squares(closed_grid, pos)
                
                if surround_value.count("c") == 0:
                    continue
                
                    
                if value == 0:
                    for position in surround_pos:
                        row, column = position
                        
                        
                        squares_to_open.append(position)

                    continue

                # removes the the covered squares if the amount of bombs is equal to the number
                if value == surround_value.count(-1):
                    for index, value in enumerate(surround_value):
                        if value != "c":
                            continue
                        
                        squares_to_open.append(surround_pos[index])

                    continue

                # checks if if there are the same amount of uncovered squares and bombs as the number 
                bomb_check = value - surround_value.count("c") - surround_value.count("f")
                
                if bomb_check == 0:
                    mines_discovered += 1
                    for index, value in enumerate(surround_value):
                        if value != "c":
                            continue
                        
                        squares_to_open.append(surround_pos[index])
                        
                    continue


        
        
        # removes all duplicates from the list
        # then opens all squares in the list
        for pos in list(dict.fromkeys(squares_to_open)):
            open_square(pos)
            reveal_sequence.append(pos)



        # Checking if any squares are covered
        covered_squares = 0
        for row in closed_grid:
            covered_squares += row.count("c")
        
        # this happems if the program is unable to solve the grid
        if len(squares_to_open) == 0 and covered_squares != 0:
            # print("nej")
            return False
        
        # if all covered squares are revealed the program is not finished
        if covered_squares != 0:
            continue

        running = False

    return reveal_sequence


# revealed_image = pygame.image.load("highres_images/Tile_Flat.png")
# covered_image = pygame.image.load("highres_images/Tile_1.png")
# bomb_image = pygame.image.load("highres_images/Skull.png")
# number_images = [pygame.image.load(f"highres_images/Number_{i}.png") for i in range(1, 9)]


def display_minesweeper_grid(grid, reveal_sequence):
    pygame.init()

    # Set up the display
    screen_width, screen_height = 1000, 1000  # Set your desired window dimensions
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Minesweeper Grid")

    # Minesweeper grid settings
    grid_size = len(grid)
    cell_size = min(screen_width // grid_size, screen_height // grid_size)

    # Load images
    revealed_image = pygame.image.load("highres_images/Tile_Flat.png").convert_alpha()
    covered_image = pygame.image.load("highres_images/Tile_1.png").convert_alpha()
    bomb_image = pygame.image.load("highres_images/Skull.png").convert_alpha()
    number_images = [pygame.image.load(f"highres_images/Number_{i}.png").convert_alpha() for i in range(1, 9)]

    # Scale images to match the cell size
    revealed_image = pygame.transform.scale(revealed_image, (cell_size, cell_size))
    covered_image = pygame.transform.scale(covered_image, (cell_size, cell_size))
    bomb_image = pygame.transform.scale(bomb_image, (cell_size, cell_size))
    number_images = [pygame.transform.scale(img, (cell_size, cell_size)) for img in number_images]

    # Set background color
    background_color = (0, 0, 0)

    # Main game loop
    running = True

    # List to store previously revealed positions
    previously_revealed = []

    clock = pygame.time.Clock()

    # Iterate over the specified reveal sequence
    reveal_iter = iter(reveal_sequence)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw Minesweeper grid
        screen.fill(background_color)

        for row in range(grid_size):
            for col in range(grid_size):
                rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)

                # Check if the cell is in the current or previously revealed positions
                if [row, col] in previously_revealed:
                    if grid[row][col] == 0:
                        screen.blit(revealed_image, rect)
                    elif grid[row][col] == -1:  # Assuming -1 represents a bomb in the grid
                        screen.blit(bomb_image, rect)
                    elif grid[row][col] == 9:
                        screen.blit(covered_image, rect)
                    else:
                        screen.blit(number_images[grid[row][col] - 1], rect)
                else:

                    screen.blit(covered_image, rect)

        # Update the display
        pygame.display.flip()

        # Get the next revealed position
        current_revealed_position = next(reveal_iter, None)
        if current_revealed_position is not None:
            # Add the current revealed position to the list of previously revealed
            previously_revealed.append(current_revealed_position)

        # Limit frames per second
        clock.tick(20)  # Set your desired frame rate (frames per second)

    pygame.quit()
    sys.exit()

def display_time(start, end):
    time_elapsed = end - start


    if time_elapsed < 60:
        return(f"{round(time_elapsed, 2)} s")

    if time_elapsed > 60:
        seconds = round(time_elapsed % 60, 2)
        minutes = int((time_elapsed - seconds)/60)
        return(f"{minutes} m {seconds} s")