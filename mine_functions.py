import pygame, sys, random, json, win32gui, pyautogui, ctypes


def create_minesweeper_grid(rows, cols, advanced=True):

    num_mines = rows*cols*0.15

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

def solve_grid(current_grid):
    # Makes a default covered version of the grid
    default_grid = switch_values(current_grid, "c")
    


# revealed_image = pygame.image.load("highres_images/Tile_Flat.png")
# covered_image = pygame.image.load("highres_images/Tile_1.png")
# bomb_image = pygame.image.load("highres_images/Skull.png")
# number_images = [pygame.image.load(f"highres_images/Number_{i}.png") for i in range(1, 9)]

def display_minesweeper_grid(grid, revealed_positions):
    pygame.init()

    # Get screen dimensions
    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Set up the display
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Minesweeper Grid")

    # Minesweeper grid settings
    grid_size = len(grid)
    cell_size = min(screen_width // grid_size, screen_height // grid_size)

    # Load images
    revealed_image = pygame.image.load("revealed_cell.png")  # Replace with your revealed cell image
    covered_image = pygame.image.load("covered_cell.png")  # Replace with your covered cell image
    bomb_image = pygame.image.load("bomb.png")  # Replace with your bomb image
    number_images = [pygame.image.load(f"number_{i}.png") for i in range(1, 9)]  # Replace with your number images

    # Main game loop
    running = True

    # Iterator for revealed positions
    revealed_iter = iter(revealed_positions)
    current_revealed_position = next(revealed_iter, None)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw Minesweeper grid
        screen.fill((255, 255, 255))

        for row in range(grid_size):
            for col in range(grid_size):
                rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)

                # Check if the cell is in the current revealed position
                if (row, col) == current_revealed_position:
                    if grid[row][col] == 0:
                        screen.blit(revealed_image, rect)
                    elif grid[row][col] == 9:  # Assuming 9 represents a bomb in the grid
                        screen.blit(bomb_image, rect)
                    else:
                        screen.blit(number_images[grid[row][col] - 1], rect)
                else:
                    screen.blit(covered_image, rect)

        # Update the display
        pygame.display.flip()

        # Delay between revealed positions
        pygame.time.delay(1000)

        # Get the next revealed position
        current_revealed_position = next(revealed_iter, None)
        if current_revealed_position is None:
            # Restart the iterator when all positions are revealed
            revealed_iter = iter(revealed_positions)
            current_revealed_position = next(revealed_iter, None)

    pygame.quit()
    sys.exit()

def display_time(start, end):
    time_elapsed = end - start


    if time_elapsed < 60:
        return(f"{round(time_elapsed, 2)} s")

    if time_elapsed > 60:
        seconds = round(time_elapsed % 60, 2)
        minutes = (time_elapsed - seconds)/60
        return(f"{minutes} m {seconds} s")