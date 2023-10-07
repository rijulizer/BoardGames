# import pygame
# import sys

# # Initialize Pygame
# pygame.init()

# # Set up display
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Scrolling Text Box Example")

# # Define colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)

# # Create a list of text lines
# text_lines = [
#     "Line 1: This is the first line of text.",
#     "Line 2: Here's the second line.",
#     "Line 3: And another line for the text box.",
#     "Line 4: You can add more lines as needed.",
#     "Line 5: This is the first line of text.",
#     "Line 6: Here's the second line.",
#     "Line 7: And another line for the text box.",
#     "Line 8: You can add more lines as needed.",
#     "Line 9: This is the first line of text.",
#     "Line 10: Here's the second line.",
#     "Line 13: And another line for the text box.",
#     "Line 14: You can add more lines as needed.",
#     "Line 11: This is the first line of text.",
#     "Line 12: Here's the second line.",
#     "Line 13: And another line for the text box.",
#     "Line 14: You can add more lines as needed.",
#     "Line 11: This is the first line of text.",
#     "Line 112: Here's the second line.",
#     "Line 13: And another line for the text box.",
#     "Line 114: You can add more lines as needed.",
#     "Line 11: This is the first line of text.",
#     "Line 112: Here's the second line.",
#     "Line 23: And another line for the text box.",
#     "Line 24: You can add more lines as needed.",
#     "Line 21: This is the first line of text.",
#     "Line 22: Here's the second line.",
#     "Line 33: And another line for the text box.",
#     "Line 34: You can add more lines as needed.",
# ]

# # Create a font for the text
# font = pygame.font.Font(None, 24)

# # Create a rectangle for the text box
# text_box_rect = pygame.Rect(10, 10, 300, 400)

# # Create a rectangle for the scrollbar
# scrollbar_rect = pygame.Rect(800 - 20, 10, 10, 480)
# scrollbar_color = (150, 150, 150)
# scrollbar_button_rect = pygame.Rect(800 - 20, 10, 10, 20)
# scrollbar_button_color = (100, 100, 100)
# scrolling_offset = 0

# # Calculate the maximum scrolling range
# max_scroll = max(0, len(text_lines) * 20 - text_box_rect.height)

# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 4:  # Scroll up
#                 scrolling_offset = max(0, scrolling_offset - 20)
#             elif event.button == 5:  # Scroll down
#                 scrolling_offset = min(max_scroll, scrolling_offset + 20)

#     # Clear the screen
#     screen.fill(WHITE)

#     # Create a surface for the text box
#     text_box_surface = pygame.Surface((text_box_rect.width, text_box_rect.height))
#     text_box_surface.fill(BLACK)

#     # Render and display text lines within the text box
#     y = 0
#     for line in text_lines:
#         text = font.render(line, True, WHITE)
#         if y - scrolling_offset > text_box_rect.height:
#             break
#         text_box_surface.blit(text, (10, y - scrolling_offset))
#         y += 20

#     screen.blit(text_box_surface, text_box_rect.topleft)

#     # Draw the scrollbar
#     pygame.draw.rect(screen, scrollbar_color, scrollbar_rect)
#     # Calculate the position of the scrollbar button based on scrolling offset and max_scroll
#     if max_scroll != 0:
#         scrollbar_button_rect.top = 10 + (scrolling_offset / max_scroll) * (text_box_rect.height - 50)
#     pygame.draw.rect(screen, scrollbar_button_color, scrollbar_button_rect)

#     pygame.display.flip()

# # Quit Pygame
# pygame.quit()
# sys.exit()

###################################################################################################
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Scrolling Text Box Example")

# Create a list of text lines
text_lines = [
    "Line 1: This is the first line of text.",
    "Line 2: Here's the second line.",
    "Line 3: And another line for the text box.",
    "Line 4: You can add more lines as needed.",
    "Line 5: This is the first line of text.",
    "Line 6: Here's the second line.",
    "Line 7: And another line for the text box.",
    "Line 8: You can add more lines as needed.",
    "Line 9: This is the first line of text.",
    "Line 10: Here's the second line.",
    "Line 13: And another line for the text box.",
    "Line 14: You can add more lines as needed.",
    "Line 11: This is the first line of text.",
    "Line 12: Here's the second line.",
    "Line 13: And another line for the text box.",
    "Line 14: You can add more lines as needed.",
    "Line 11: This is the first line of text.",
    "Line 112: Here's the second line.",
    "Line 13: And another line for the text box.",
    "Line 114: You can add more lines as needed.",
    "Line 11: This is the first line of text.",
    "Line 112: Here's the second line.",
    "Line 23: And another line for the text box.",
    "Line 24: You can add more lines as needed.",
    "Line 21: This is the first line of text.",
    "Line 22: Here's the second line.",
    "Line 33: And another line for the text box.",
    "Line 34: You can add more lines as needed.",
]

def create_hist_box(hist_stat: list, pos : tuple[int,int], scrolling_offset, max_scroll):
    # declare variables
    # Define colors
    text_color = (247, 229, 205)
    text_box_color = (0, 0, 0)
    text_line_space = 30
    # Create a font for the text
    font = pygame.font.Font(None, 22)

    box_height, box_width = 600, 400
    pos_x, pos_y = pos
    # Create a rectangle for the text box
    text_box_rect = pygame.Rect(pos_x, pos_y, box_width, box_height)

    # Create a rectangle for the scrollbar
    scrollbar_rect = pygame.Rect(pos_x + box_width - 20, pos_y, 10, box_height)
    scrollbar_color = (150, 150, 150)
    scrollbar_button_rect = pygame.Rect(pos_x + box_width - 20, pos_y, 10, 20)
    scrollbar_button_color = (100, 100, 100)
    
    # Create a surface for the text box
    text_box_surface = pygame.Surface((text_box_rect.width, text_box_rect.height))
    text_box_surface.fill(text_box_color)

    # Render and display text lines within the text box
    y = 0
    for line in hist_stat:
        text = font.render(line, True, text_color)
        if y - scrolling_offset > text_box_rect.height:
            break
        text_box_surface.blit(text, (pos_y, y - scrolling_offset))
        y += text_line_space

    screen.blit(text_box_surface, text_box_rect.topleft)

    # Draw the scrollbar
    pygame.draw.rect(screen, scrollbar_color, scrollbar_rect)
    # Calculate the position of the scrollbar button based on scrolling offset and max_scroll
    if max_scroll != 0:
        scrollbar_button_rect.top = 10 + (scrolling_offset / max_scroll) * (text_box_rect.height - 50)
    pygame.draw.rect(screen, scrollbar_button_color, scrollbar_button_rect)

text_line_space = 30
# Calculate the maximum scrolling range
max_scroll = max(0, len(text_lines) * text_line_space - 600)
scrolling_offset = max_scroll

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                scrolling_offset = max(0, scrolling_offset - 20)
            elif event.button == 5:  # Scroll down
                scrolling_offset =  min(max_scroll, scrolling_offset + 20)

    # Clear the screen
    screen.fill((255,255,255))

    create_hist_box(text_lines, (100,10), scrolling_offset, max_scroll)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

