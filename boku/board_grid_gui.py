import pygame
import sys
import math
import numpy as np

# Constants
WIDTH, HEIGHT = 1200, 800
GRID_RADIUS = 6  # Grid radius, determines the size of the grid
HEX_SIZE = 40  # Hexagon size
BG_COLOR = (250, 250, 250)
HEX_COLOR = (0, 0, 200, 100)
HEX_WIDTH = 1
FONT_SIZE = 20
LABEL_COLOR = (255,0,0)

board_grid = {
        # x=0, y<0
        'F6': (0,0),
        'E5': (0,1),
        'D4': (0,2),
        'C3': (0,3),
        'B2': (0,4),
        'A1': (0,5),
        # x=0, y>0
        'G7': (0,-1),
        'H8': (0,-2),
        'I9': (0,-3),
        'J10': (0,-4),
        
        # x=-1, y<0
        'F7': (-1,0),
        'E6': (-1,1),
        'D5': (-1,2),
        'C4': (-1,3),
        'B3': (-1,4),
        'A2': (-1,5),
        # x=-1, y<0
        'G8': (-1,-1),
        'H9': (-1,-2),
        'I10': (-1,-3),
        
        # x=-2, y<0
        'F8': (-2,0),
        'E7': (-2,1),
        'D6': (-2,2),
        'C5': (-2,3),
        'B4': (-2,4),
        'A3': (-2,5),
        # x=-2, y<0
        'G9': (-2,-1),
        'H10': (-2,-2),

        # x=-3, y<0
        'F9': (-3,0),
        'E8': (-3,1),
        'D7': (-3,2),
        'C6': (-3,3),
        'B5': (-3,4),
        'A4': (-3,5),
        # x=-3, y<0
        'G10': (-3,-1),

        # x=-4, y<0
        'F10': (-4,0),
        'E9': (-4,1),
        'D8': (-4,2),
        'C7': (-4,3),
        'B6': (-4,4),
        'A5': (-4,5),
        
        # x=-5 , y<0
        'E10': (-5,1),
        'D9': (-5,2),
        'C8': (-5,3),
        'B7': (-5,4),
        'A6': (-5,5),

        # x=1, y<0
        'F5': (1,0),
        'E4': (1,1),
        'D3': (1,2),
        'C2': (1,3),
        'B1': (1,4),
        # x=1, y<0
        'G6': (1,-1),
        'H7': (1,-2),
        'I8': (1,-3),
        'J9': (1,-4),
        
        # x=2, y<0
        'F4': (2,0),
        'E3': (2,1),
        'D2': (2,2),
        'C1': (2,3),
        # x=2, y>0
        'G5': (2,-1),
        'H6': (2,-2),
        'I7': (2,-3),
        'J8': (2,-4),

        # x=3, y<0
        'F3': (3,0),
        'E2': (3,1),
        'D1': (3,2),
        # x=3, y>0
        'G4': (3,-1),
        'H5': (3,-2),
        'I6': (3,-3),
        'J7': (3,-4),

        # x=4 y<0
        'F2': (4,0),
        'E1': (4,1),
        # x=4, y>0
        'G3': (4,-1),
        'H4': (4,-2),
        'I5': (4,-3),
        'J6': (4,-4),
        
        # x=5
        'F1': (5,0),
        # x=5, y>0
        'G2': (5,-1),
        'H3': (5,-2),
        'I4': (5,-3),
        'J5': (5,-4),
        
    }



# Function to convert cube coordinates to pixel coordinates
def cube_to_pixel(cube_cordinates):
    q,r = cube_cordinates[0], cube_cordinates[1]
    # s = -q -r 
    x = (3/2 * q) * HEX_SIZE
    y = (math.sqrt(3)/2 * q + math.sqrt(3) * r) * HEX_SIZE
    return x, y

def draw_hexagon(cube_cordinates, label):
    # get the center co-ordinates
    q,r = cube_cordinates[0], cube_cordinates[1]
    s = -q -r 
    # get the center of the screen
    screen_center_x, screen_center_y = WIDTH // 2 -200, HEIGHT // 2 - 50
    # get center co-ordinates of a hex
    center_cordinates = cube_to_pixel(cube_cordinates)
    # offset center to screen center
    x_center = screen_center_x + center_cordinates[0]
    y_center = screen_center_y + center_cordinates[1]
    # [DEBUG] lebel
    label_points = f": {(q,r,s)}"
    # label_points = f": (q={q}, r={r}, s={s}), center=({np.round(center_cordinates[0],2), np.round(center_cordinates[1],2)})"
    label=label+label_points

    # crate all the vertices
    vertices = []
    for i in range(6):
        angle_deg = 60 * i #30 + (60*i)
        angle_rad = math.radians(angle_deg)
        x = x_center + HEX_SIZE * math.cos(angle_rad)
        y = y_center + HEX_SIZE * math.sin(angle_rad)
        vertices.append((x,y))

    pygame.draw.polygon(screen, HEX_COLOR, vertices, HEX_WIDTH)
    # create a font object
    font = pygame.font.Font(None, FONT_SIZE)
    # create a text surface with anti aliased text
    text_surface = font.render(label, True, LABEL_COLOR)
    # get the rectangle of the text surface
    text_rect = text_surface.get_rect()
    text_rect.center = pygame.Vector2((x_center, y_center))#[0], center_cordinates[1])

    # blit, copy the text surface on to the screen
    screen.blit(text_surface, text_rect)

# Initialize Pygame
pygame.init()
# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagonal Grid")

clock = pygame.time.Clock()
running = True
while running:
    # check for quit by user
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)
    # draw the hexagonal grid
    for name, points in board_grid.items():
        draw_hexagon(points,name)
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
