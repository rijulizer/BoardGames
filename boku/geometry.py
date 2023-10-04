import pygame
import sys
import math
import numpy as np
from init import (WIDTH, HEIGHT, HEX_SIZE, BG_COLOR, 
                  HEX_COLOR, HEX_WIDTH, FONT_SIZE, LABEL_COLOR, 
                  boku_rule_cont_pos, PLAYERS, HEX_GRID_CORDS, 
                  HEX_GRID_FLAT_MAP, TRAP_PATTERN
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
    screen_center_x, screen_center_y = WIDTH // 2 - 200, HEIGHT // 2 - 50
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

def flat_map_gird(hex_name: str):
    """
    returns row and column index of flat_grid_map from hex_name
    """
    
    hex_points = HEX_GRID_CORDS[hex_name]
    q,r = hex_points[0], hex_points[1]
    shifted_q = q+5 # this shifts are due to the index shift in flat map
    shifted_r = r+4
    return (shifted_q, shifted_r)

def update_hex_points():
    """
    creates certasian updates hex points in HEX_GRID_CORDS and HEX_GRID_FLAT_MAP
        """
    # generate ceratsaian co-ords of HEX_GRID udate Hex_grid
    for hex_name, cube_cords in HEX_GRID_CORDS.items():
        # generate certasian co-ords
        hex_cords = create_hex_vertices(cube_cords)
        # add hex points to HEX_GRID_CORDS
        hex_points = cube_cords.copy()
        hex_points.extend(hex_cords)
        HEX_GRID_CORDS[hex_name] = hex_points
        # generated row-cols for flat_map
        (shifted_q, shifted_r) = flat_map_gird(hex_name)
        HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r] = hex_points

# if __name__ == "__main__":
update_hex_points()