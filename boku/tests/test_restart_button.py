import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (255, 255, 255)
BUTTON_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game with Restart Button")

# Function to draw a button
def draw_button(x, y, width, height, text):
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Function to check if a point is inside a rectangle
def is_point_inside_rect(x, y, rect):
    return rect.collidepoint(x, y)

# Main game loop
running = True
restart_button_rect = pygame.Rect(50, 50, 150, 50)  # Define the restart button's position and size

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if is_point_inside_rect(x, y, restart_button_rect):
                print("Restart button clicked")  # Perform restart action here

    # Clear the screen
    screen.fill(BG_COLOR)

    # Draw the restart button
    draw_button(restart_button_rect.x, restart_button_rect.y, restart_button_rect.width, restart_button_rect.height, "Restart")

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
