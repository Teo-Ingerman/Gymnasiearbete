import pygame
import sys
import random

def display_minesweeper_grid(grid, reveal_sequence):
    pygame.init()

    # Set up the display
    screen_width, screen_height = 800, 600  # Set your desired window dimensions
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
        clock.tick(10)  # Set your desired frame rate (frames per second)

    pygame.quit()
    sys.exit()

# Example usage with placeholder values
minesweeper_grid = [[random.choice([-1, 0, 1, 2, 3, 4, 5, 6, 7, 8]) for _ in range(5)] for _ in range(5)]
reveal_sequence = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]

display_minesweeper_grid(minesweeper_grid, reveal_sequence)
