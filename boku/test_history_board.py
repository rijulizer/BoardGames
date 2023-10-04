# import pygame
# import sys

# # Initialize Pygame
# pygame.init()

# # Set up display
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Rectangle with Lines Example")

# # Define colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)

# # Define the rectangle's position and size
# rect_x, rect_y = 100, 100
# rect_width, rect_height = 400, 200

# # Create a font for the text
# font = pygame.font.Font(None, 36)

# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Clear the screen
#     screen.fill(WHITE)

#     # Draw the rectangle
#     pygame.draw.rect(screen, RED, (rect_x, rect_y, rect_width, rect_height), 2)

#     # Create and render lines of text
#     text_lines = ["Line 1: This is some text",
#                   "Line 2: On a rectangle",
#                   "Line 3: You can add more lines here"]

#     y_offset = 0
#     for line in text_lines:
#         text = font.render(line, True, BLACK)
#         screen.blit(text, (rect_x + 10, rect_y + 10 + y_offset))
#         y_offset += 30  # Adjust the vertical spacing

#     pygame.display.flip()

# # Quit Pygame
# pygame.quit()
# sys.exit()

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Linux Command Line Style Text Box")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create a list to store text lines
text_lines = []

# Create a font for the text
font = pygame.font.Font(None, 24)

# Create a rectangle for the text box
text_box_rect = pygame.Rect(10, 10, 780, 580)

# Create a scrolling offset
scroll_offset = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # When Enter is pressed, add the text to the text_lines list
                text_lines.append("")
            elif event.key == pygame.K_BACKSPACE:
                # When Backspace is pressed, remove the last character from the current line
                if len(text_lines) > 0:
                    text_lines[-1] = text_lines[-1][:-1]
            else:
                # Add the pressed character to the current line
                if len(text_lines) == 0:
                    text_lines.append(event.unicode)
                else:
                    text_lines[-1] += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                scroll_offset += 20
            elif event.button == 5:  # Scroll down
                scroll_offset -= 20

    # Clear the screen
    screen.fill(WHITE)

    # Create a surface for the text box
    text_box_surface = pygame.Surface((text_box_rect.width, text_box_rect.height))
    text_box_surface.fill(WHITE)

    # Render and display text lines within the text box
    y = 0
    for i, line in enumerate(text_lines):
        text = font.render(line, True, BLACK)
        if i * 20 - scroll_offset > text_box_rect.height:
            break
        text_box_surface.blit(text, (10, y - scroll_offset))
        y += 20

    screen.blit(text_box_surface, text_box_rect.topleft)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
