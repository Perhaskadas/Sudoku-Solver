import pygame
from Functions import Board
# Initialize Pygame
pygame.init()

# Define colors
BLACK = (25, 36, 35)
WHITE = (245, 226, 190)
GRAY = (200, 200, 200)
GREEN = (77, 141, 83)
RED = (197, 30, 27)
DARK_GRAY = (44, 58, 56)


# Define the size of the grid
GRID_SIZE = 9
CELL_SIZE = 60
GRID_WIDTH = CELL_SIZE * GRID_SIZE
GRID_HEIGHT = CELL_SIZE * GRID_SIZE
BUTTON_WIDTH = GRID_WIDTH
BUTTON_HEIGHT = 50

# Set up the display window
screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT + BUTTON_HEIGHT))
pygame.display.set_caption("Sudoku Input")

# Create a 2D grid to store the numbers
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Create a copy of the original grid to differentiate user-inputted numbers from solved numbers
original_grid = [row[:] for row in grid]

# Variable to store the selected cell
selected_cell = None

# Helper function to draw the grid on the screen
def draw_grid():
    for i in range(GRID_SIZE + 1):
        if i % 3 == 0:
            line_width = 3
        else:
            line_width = 1

        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_HEIGHT), line_width)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (GRID_WIDTH, i * CELL_SIZE), line_width)

# Helper function to draw the numbers on the grid
def draw_numbers():
    font = pygame.font.Font(None, 36)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            number = grid[row][col]
            if number != 0:
                text_color = DARK_GRAY
                if original_grid[row][col] != 0:
                    text_color = RED
                text = font.render(str(number), True, text_color)
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

# Helper function to draw the solve button
def draw_button():
    font = pygame.font.Font(None, 30)

    button_rect = pygame.Rect(0, GRID_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, GREEN, button_rect)

    text = font.render("Solve", True, (0, 0, 0))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    return button_rect

# Function to solve the Sudoku puzzle
def solve_sudoku():
    # Update the original_grid with the user's inputs
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if original_grid[row][col] == 0:  # Only update the cells that were initially empty
                original_grid[row][col] = grid[row][col]

    sudoku_input = []  # List to store the input numbers

    for row in range(GRID_SIZE):
        sudoku_row = []
        for col in range(GRID_SIZE):
            sudoku_row.append(grid[row][col])
        sudoku_input.append(sudoku_row)

    # Do something with the sudoku_input list
    solved_board = solve_sudoku_puzzle(sudoku_input)  # Solve the Sudoku puzzle and get the solved board

    # Update the grid with the solved numbers
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if original_grid[row][col] == 0:  # Only update the cells that were initially empty
                grid[row][col] = solved_board[row][col]

# Helper function to solve the Sudoku puzzle
def solve_sudoku_puzzle(board):
    sudoku_input = []  # List to store the input numbers

    for row in range(GRID_SIZE):
        sudoku_row = []
        for col in range(GRID_SIZE):
            sudoku_row.append(grid[row][col])
        sudoku_input.append(sudoku_row)
    sudoku_board = Board(sudoku_input)
    sudoku_board.solve_sudoku()
    return sudoku_board.rows

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Get the clicked cell coordinates
                mouse_pos = pygame.mouse.get_pos()
                cell_row = mouse_pos[1] // CELL_SIZE
                cell_col = mouse_pos[0] // CELL_SIZE

                if cell_row < GRID_SIZE and cell_col < GRID_SIZE:
                    selected_cell = (cell_row, cell_col)
                elif button_rect.collidepoint(mouse_pos):
                    solve_sudoku()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                selected_cell = None
            elif selected_cell is not None and pygame.K_1 <= event.key <= pygame.K_9:
                # Get the number from the key pressed
                number = event.key - pygame.K_1 + 1
                row, col = selected_cell
                grid[row][col] = number

    # Clear the screen
    screen.fill(WHITE)

    # Draw the grid and numbers
    draw_grid()
    draw_numbers()

    # Draw the solve button and get its rectangle
    button_rect = draw_button()

    # Highlight the selected cell
    if selected_cell is not None:
        cell_rect = pygame.Rect(selected_cell[1] * CELL_SIZE, selected_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, cell_rect, 4)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()