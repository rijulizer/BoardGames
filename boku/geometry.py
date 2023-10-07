import math
import numpy as np
from pprint import pprint
# (WIDTH, HEIGHT, HEX_SIZE, BG_COLOR, 
#                   HEX_COLOR, HEX_WIDTH, FONT_SIZE, LABEL_COLOR, 
#                   boku_rule_cont_pos, PLAYERS, HEX_GRID_CORDS, 
#                   HEX_GRID_FLAT_MAP, TRAP_PATTERN
# ) 
from init import BoardVariables

class BoardGeometry():
    def __init__(self, board_variable):
        print("[DEBUG]- Initiating Board Geometry...")
        self.board_variable = board_variable # obejct that holds all the board bariables
        # Updates the inital variables with hex points
        self.update_hex_points()
         
    # Function to convert cube coordinates to pixel coordinates
    def cube_to_pixel(self, cube_cordinates):
        q,r = cube_cordinates[0], cube_cordinates[1]
        # s = -q -r 
        x = (3/2 * q) * self.board_variable.HEX_SIZE
        y = (math.sqrt(3)/2 * q + math.sqrt(3) * r) * self.board_variable.HEX_SIZE
        return x, y

    def create_hex_vertices(self, cube_cordinates: list[int]):
        """
        gets cube co-ordinate of a hexagon and creates certasian co-ordinates of center and vertices 
        """
        # get the center co-ordinates
        q,r = cube_cordinates[0], cube_cordinates[1]
        s = -q -r 
        # get the center of the screen
        screen_center_x, screen_center_y = self.board_variable.WIDTH // 2 - 200, self.board_variable.HEIGHT // 2 - 50
        # get center co-ordinates of a hex
        center_cordinates = self.cube_to_pixel(cube_cordinates)
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
            x = x_center + self.board_variable.HEX_SIZE * math.cos(angle_rad)
            y = y_center + self.board_variable.HEX_SIZE * math.sin(angle_rad)
            vertices.append((x,y))
        hex_points.extend(vertices)
        return hex_points

    def uclidean_distance(self, p1, p2):
        dist = [(a - b)**2 for a, b in zip(p1, p2)]
        dist = math.sqrt(sum(dist))
        return dist

    def find_hex_center_near_mouse_click(self, mouse_x, mouse_y):
        """
        finds the nearest hexagon of mouse click position
        """
        shortest_dist = self.board_variable.WIDTH # or set this to +infinty
        nearest_hex = None

        # filter all hexagons center within a range |R| to shorten the search space
        for hex_name, hex_points in self.board_variable.HEX_GRID_CORDS.items():
            hex_center_x, hex_center_y = hex_points[2], hex_points[3]
            if (
                (hex_center_x >= mouse_x - self.board_variable.HEX_SIZE) and 
                (hex_center_x <= mouse_x + self.board_variable.HEX_SIZE) and 
                (hex_center_y >= mouse_y - self.board_variable.HEX_SIZE) and 
                (hex_center_y <= mouse_y + self.board_variable.HEX_SIZE)
            ):  
            # at max 3 hexagons will be selected if mouse is clicked in the intersection point 
            # then calcualte the nearest center
                dist = self.uclidean_distance((mouse_x, mouse_y), (hex_center_x, hex_center_y))
                if dist < shortest_dist:
                    shortest_dist = dist
                    nearest_hex = hex_name

        return nearest_hex 

    def flat_map_gird(self, hex_name: str):
        """
        returns row and column index of flat_grid_map from hex_name
        """
        
        hex_points = self.board_variable.HEX_GRID_CORDS[hex_name]
        q,r = hex_points[0], hex_points[1]
        shifted_q = q+5 # this shifts are due to the index shift in flat map
        shifted_r = r+4
        return (shifted_q, shifted_r)

    def update_hex_points(self):
        """
        Input: board variable object containing all the variables
        creates certasian updates hex points in board_variable object variables [HEX_GRID_CORDS and HEX_GRID_FLAT_MAP]
        """
        # generate ceratsaian co-ords of HEX_GRID udate Hex_grid
        for hex_name, cube_cords in self.board_variable.HEX_GRID_CORDS.items():
            # generate certasian co-ords
            hex_cords = self.create_hex_vertices(cube_cords)
            # add hex points to HEX_GRID_CORDS
            hex_points = cube_cords.copy()
            hex_points.extend(hex_cords)
            self.board_variable.HEX_GRID_CORDS[hex_name] = hex_points
            # generated row-cols for flat_map
            (shifted_q, shifted_r) = self.flat_map_gird(hex_name)
            self.board_variable.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r] = hex_points

if __name__ == "__main__":
    board_variables = BoardVariables()
    print("[DEBUG]-[geometry]- board_variable.HEX_GRID_FLAT_MAP after BoardVariables() \n")
    pprint(board_variables.HEX_GRID_FLAT_MAP)
    board_geometry = BoardGeometry(board_variables)
    print("[DEBUG]-[geometry]- board_variable.HEX_GRID_FLAT_MAP after BoardGeometry() \n")
    pprint(board_variables.HEX_GRID_FLAT_MAP)
    