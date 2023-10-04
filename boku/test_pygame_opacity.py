import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Transparent Circle Example")

# Define colors
WHITE = (255, 255, 255)
TRANSPARENT_BLUE = (0, 0, 255, 128)

# Create a surface for the circle
circle_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
pygame.draw.circle(circle_surface, TRANSPARENT_BLUE, (100, 100), 100)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Blit the circle surface onto the screen
    screen.blit(circle_surface, (300, 250))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
