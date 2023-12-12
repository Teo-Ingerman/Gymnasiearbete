import pygame, sys, random, json, win32gui




def create_minesweeper_grid(rows, cols, num_mines, advanced):
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
    CELL_SIZE = 30
    SCALE_SIZE = (CELL_SIZE, CELL_SIZE)
    GAP = 0

    screen_width = len(board[0]) * (CELL_SIZE + GAP)
    screen_height = len(board) * (CELL_SIZE + GAP)
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
                x = col * (CELL_SIZE + GAP)
                y = row * (CELL_SIZE + GAP)

                if cell_value == -1:
                    screen.blit(flag_image, (x, y))
                elif cell_value == "c":
                    screen.blit(concealed_image, (x, y))    
                else:
                    if cell_value > 0:
                        number_image = number_images[cell_value - 1]
                        screen.blit(number_image, (x, y))
                    else:
                        screen.blit(revealed_image, (x, y))
                    

        pygame.display.flip()
        clock.tick(10)  # Change the frame rate as needed
        board_index += 1
        if board_index < len(boards):
            board = boards[board_index]
        else:
            # playing = False
            board = boards[-1]

    pygame.quit()
    sys.exit()

def replace_all(arr, value):
    if isinstance(arr, list):
        new_arr = []
        for item in arr:
            new_arr.append(replace_all(item, value))
        return new_arr
    else:
        return value


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