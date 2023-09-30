import pygame
import sys
import math
import numpy as np
from init import (WIDTH, HEIGHT, GRID_RADIUS, HEX_SIZE, BG_COLOR, 
                  HEX_COLOR, HEX_WIDTH, FONT_SIZE, LABEL_COLOR, 
                  boku_rule_cont_pos, PLAYERS, HEX_GRID_CORDS, HEX_GRID_FLAT_MAP
)

# Function to convert cube coordinates to pixel coordinates
def cube_to_pixel(cube_cordinates):
    q,r = cube_cordinates[0], cube_cordinates[1]
    # s = -q -r 
    x = (3/2 * q) * HEX_SIZE
    y = (math.sqrt(3)/2 * q + math.sqrt(3) * r) * HEX_SIZE
    return x, y

def create_hex_vertices(cube_cordinates: list[int]):
    """
    gets cube co-ordinate of a hexagon and creates certasian co-ordinates of center and vertices 
    """
    # get the center co-ordinates
    q,r = cube_cordinates[0], cube_cordinates[1]
    s = -q -r 
    # get the center of the screen
    screen_center_x, screen_center_y = WIDTH // 2, HEIGHT // 2 - 50
    # get center co-ordinates of a hex
    center_cordinates = cube_to_pixel(cube_cordinates)
    # offset center to screen center
    x_center = screen_center_x + center_cordinates[0]
    y_center = screen_center_y + center_cordinates[1]
    # a list of all points of interest - first two are x_center,y_center after that the 6 points
    hex_points = [x_center, y_center]
    # crate all the vertices
    vertices = []
    for i in range(6):
        angle_deg = 60 * i # flat top hexagon  
        angle_rad = math.radians(angle_deg)
        x = x_center + HEX_SIZE * math.cos(angle_rad)
        y = y_center + HEX_SIZE * math.sin(angle_rad)
        vertices.append((x,y))
    hex_points.extend(vertices)
    return hex_points

# generate ceratsaian co-ords of HEX_GRID
for hex_name, cube_cords in HEX_GRID_CORDS.items():
    # generate certasian co-ords
    hex_cords = create_hex_vertices(cube_cords)
    # add hex points to HEX_GRID_CORDS
    hex_points = cube_cords.copy()
    hex_points.extend(hex_cords)
    HEX_GRID_CORDS[hex_name] = hex_points


def draw_hexagon(hex_points: list[float], label: str, cords_label: bool = False):
    """
    Input: hex_points=[q, r, x_center, y_center, v1, v2, v3, v4, v5, v6]
    takes the hex points and draws a hex on screen
    """
    if cords_label:
        # get the center co-ordinates
        q,r = hex_points[0], hex_points[1]
        s = -q -r 
        label_points = f": {(q,r,s)}"
        label = label + label_points

    x_center, y_center = hex_points[2], hex_points[3]
    vertices = hex_points[4:]
    assert len(vertices) ==6, "[Debug] hex points are incorrect"

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

def uclidean_distance(p1, p2):
    dist = [(a - b)**2 for a, b in zip(p1, p2)]
    dist = math.sqrt(sum(dist))
    return dist

def find_hex_center_near_mouse_click(mouse_x, mouse_y):
    """
    finds the nearest hexagon of mouse click position
    """
    shortest_dist = WIDTH # or set this to +infinty
    nearest_hex = None

    # filter all hexagons center within a range |R| to shorten the search space
    for hex_name, hex_points in HEX_GRID_CORDS.items():
        hex_center_x, hex_center_y = hex_points[2], hex_points[3]
        if (
            (hex_center_x >= mouse_x - HEX_SIZE) and 
            (hex_center_x <= mouse_x + HEX_SIZE) and 
            (hex_center_y >= mouse_y - HEX_SIZE) and 
            (hex_center_y <= mouse_y + HEX_SIZE)
        ):  
        # at max 3 hexagons will be selected if mouse is clicked in the intersection point 
        # then calcualte the nearest center
            dist = uclidean_distance((mouse_x, mouse_y), (hex_center_x, hex_center_y))
            if dist < shortest_dist:
                shortest_dist = dist
                nearest_hex = hex_name

    return nearest_hex      

def draw_circle(circle_info):

    center_cords = circle_info[0]
    circle_player = circle_info[1]
    player_color = PLAYERS[circle_player]["color"]
    border_color = (128, 104, 73)
    border_width = 5
    radius = int(0.7 * HEX_SIZE) # 70 % of hex radius

    pygame.draw.circle(screen, player_color, center_cords, radius)
    pygame.draw.circle(screen, border_color, center_cords, radius, border_width)

def check_contiguous_players(grid_flat_map, player, n):

    rows, cols = len(grid_flat_map), len(grid_flat_map[0])
    grid_flat_map = np.array(grid_flat_map)

    # check for contiguos elements in rows
    for row in grid_flat_map:
        for i in range (cols - n + 1):
            if all(row[i:i+n] == player):
                return True  

    # check for contiguos elements in cols
    for col in grid_flat_map.T:
        for i in range (rows - n + 1):
            if all(col[i:i+n] == player):
                return True 
    # check for contiguos elements in anti-diagonals
    
    for i in range (rows - n + 1):
        for j in range(cols - n + 1):
            anti_diagonal = np.fliplr(grid_flat_map[i:i+n, j:j+n]).diagonal()
            if all(anti_diagonal == player):
                return True 

def test_check_contiguous_players(grid_flat_map, player, n):
    # same function except instad of returning true or falls it return number of times such occurence happens
    rows, cols = len(grid_flat_map), len(grid_flat_map[0])
    grid_flat_map = np.array(grid_flat_map)

    occurence = 0
    # check for contiguos elements in rows
    for row in grid_flat_map:
        # print(f"[Debug]- row - {row}")
        for i in range (cols - n + 1):
            # print(f"[Debug]- row segments - {row[i:i+n]}, occurance- {occurence}")
            if all(row[i:i+n] == player):
                occurence +=1 

    # check for contiguos elements in cols
    for col in grid_flat_map.T:
        for i in range (rows - n + 1):
            if all(col[i:i+n] == player):
                occurence +=1 
    # check for contiguos elements in anti-diagonals
    
    for i in range (rows - n + 1):
        for j in range(cols - n + 1):
            anti_diagonal = np.fliplr(grid_flat_map[i:i+n, j:j+n]).diagonal()
            if all(anti_diagonal == player):
                occurence +=1 
    
    return occurence

def flat_map_gird(clicked_hex_name: str, player: str):
    """
    Taps position to flat map grid. This helps in determining the contiguous occurance of players 
    """
    # 
    clicked_hex_points = HEX_GRID_CORDS[clicked_hex_name]
    q,r = clicked_hex_points[0], clicked_hex_points[1]
    shifted_q = q+5 # this shifts are due to the index shift in flat map
    shifted_r = r+4
    HEX_GRID_FLAT_MAP[shifted_q][shifted_r] = PLAYERS[player]["symbol"]
    # TEMP: print the flat map
    # for q in range(0,11):
    #     print(grid_flat_map[q], sep='\n')

def play_game_multiuser():
    # Initialize Pygame
    pygame.init()
    global screen
    # Create the Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boku")
    clock = pygame.time.Clock()

    circles = []   
    # start with player p1
    player = "p1"
    running = True
    while running:
        # check for quit by user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button ==1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # find the hex that was clicked
                    clicked_hex_name = find_hex_center_near_mouse_click(mouse_x, mouse_y)
                    print(f"[Debug] mouse position - {mouse_x, mouse_y} clicked_hex_name - {clicked_hex_name}")
                    
                    if clicked_hex_name: # if user actually clicks on a hex
                        # get center and vertices of clicked hexagon
                        clicked_hex_points = HEX_GRID_CORDS[clicked_hex_name]
                        (hex_center_x, hex_center_y) = clicked_hex_points[2], clicked_hex_points[3]
                        # add center to a list to represent player-tokens(circles) 
                        circles.append([(hex_center_x, hex_center_y), player])
                        # map the player symbol in 2d array
                        flat_map_gird(clicked_hex_name, player)                        
                        # count = test_check_contiguous_players(grid_flat_map, player, 5)
                        # print("[Debug] Contiguous occurence - ", count)
                        if check_contiguous_players(HEX_GRID_FLAT_MAP, PLAYERS[player]['symbol'], boku_rule_cont_pos):
                            print("[Debug] Contiguous occurence")
                        
                        # switch player
                        if player == "p1":
                            player = "p2"
                        else:
                            player = "p1"                        
        
        # display blank screen
        screen.fill(BG_COLOR)
        # Draw board and player tokens
        # draw the hexagonal grid
        for hex_name, hex_points in HEX_GRID_CORDS.items():
            draw_hexagon(hex_points,hex_name)
        
        for circle_info in circles:
            draw_circle(circle_info)
        
        pygame.display.flip()
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    play_game_multiuser()