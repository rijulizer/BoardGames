import pygame
import numpy as np

class Graphics():
    def __init__(self, screen, game_variables, ):
        print("[DEBUG]- Initiating Graphics...")
        self.screen = screen
        self.variables = game_variables
        # self.geometry = game_geometry

    def draw_hexagon(
            self,
            hex_points: list[float], 
            label: str, 
            flag_cords_label: bool = False):
        """
        Input: hex_points=[q, r, x_center, y_center, v1, v2, v3, v4, v5, v6]
        takes the hex points and draws a hex on screen
        """
        if flag_cords_label:
            # get the center co-ordinates
            q,r = hex_points[0], hex_points[1]
            s = -q -r 
            label_points = f": {(q,r,s)}"
            label = label + label_points

        x_center, y_center = hex_points[2], hex_points[3]
        vertices = hex_points[4:]
        assert len(vertices) ==6, "[Debug] hex points are incorrect"

        pygame.draw.polygon(self.screen, self.variables.HEX_COLOR, vertices, self.variables.HEX_WIDTH)
        # create a font object
        font = pygame.font.Font(None, self.variables.FONT_SIZE)
        # create a text surface with anti aliased text
        text_surface = font.render(label, True, self.variables.LABEL_COLOR)
        # get the rectangle of the text surface
        text_rect = text_surface.get_rect()
        text_rect.center = pygame.Vector2((x_center, y_center))#[0], center_cordinates[1])
        # blit, copy the text surface on to the screen
        self.screen.blit(text_surface, text_rect)
    
    def draw_circle(self, center_cords, player):
        player_color = self.variables.PLAYERS[player]["color"]
        border_color = (128, 104, 73)
        border_width = 5
        radius = int(0.7 * self.variables.HEX_SIZE) # 70 % of hex radius

        pygame.draw.circle(self.screen, player_color, center_cords, radius)
        pygame.draw.circle(self.screen, border_color, center_cords, radius, border_width)

    def create_hist_box(
            self,
            hist_stat: list, 
            pos : tuple[int,int], 
            scrolling_offset, 
            max_scroll):
        """
        draws history box in the right side of the window
        """
        # declare variables
        # Define colors
        text_color = (247, 229, 205)
        text_box_color = (0, 0, 0)
        scrollbar_color = (150, 150, 150)
        scrollbar_button_color = (100, 100, 100)
        text_line_space = 30
        box_height, box_width = 600, 350
        
        pos_x, pos_y = pos
        # Create a rectangle for the text box
        text_box_rect = pygame.Rect(pos_x, pos_y, box_width, box_height)
        # Create a surface for the text box
        text_box_surface = pygame.Surface((text_box_rect.width, text_box_rect.height))
        text_box_surface.fill(text_box_color)

        # Create a rectangle for the scrollbar
        scrollbar_rect = pygame.Rect(pos_x + box_width - 20, pos_y, 10, box_height)
        scrollbar_button_rect = pygame.Rect(pos_x + box_width - 20, pos_y, 10, 20)
        
        # Create a font for the text
        font = pygame.font.Font(None, 24)
        # Render and display text lines within the text box
        y = 0
        for line in hist_stat:
            text = font.render(line, True, text_color)
            if y - scrolling_offset > text_box_rect.height:
                break
            text_box_surface.blit(text, (20, y - scrolling_offset))
            y += text_line_space

        self.screen.blit(text_box_surface, text_box_rect.topleft)

        # Draw the scrollbar
        pygame.draw.rect(self.screen, scrollbar_color, scrollbar_rect)
        # Calculate the position of the scrollbar button based on scrolling offset and max_scroll
        if max_scroll != 0:
            scrollbar_button_rect.top = 10 + (scrolling_offset / max_scroll) * (text_box_rect.height - 50)
        pygame.draw.rect(self.screen, scrollbar_button_color, scrollbar_button_rect)

    def draw_player_tokens(self,):
        """
        draws circles for tokens in flatmap grid
        """
        n_rows, n_cols = len(self.variables.HEX_GRID_FLAT_MAP[0]), len(self.variables.HEX_GRID_FLAT_MAP[0][0])
        for r in range(n_rows):
            for c in range(n_cols):
                if self.variables.HEX_GRID_FLAT_MAP[0][r][c] in [self.variables.PLAYERS["p1"]["symbol"],self.variables.PLAYERS["p2"]["symbol"]]: # check if the board has a token 
                    if self.variables.HEX_GRID_FLAT_MAP[1][r][c]: # not None invalid positions
                        # get the center of the hexagon 
                        (hex_center_x, hex_center_y) = self.variables.HEX_GRID_FLAT_MAP[1][r][c][2], self.variables.HEX_GRID_FLAT_MAP[1][r][c][3] 
                        if self.variables.HEX_GRID_FLAT_MAP[0][r][c]==self.variables.PLAYERS["p1"]["symbol"]:
                            player="p1"
                        elif self.variables.HEX_GRID_FLAT_MAP[0][r][c]==self.variables.PLAYERS["p2"]["symbol"]:
                            player="p2"
                        self.draw_circle((hex_center_x, hex_center_y), player)

    # def draw_player_turn(self, center_cords, player):
        
    #     c1_player = player
    #     # c1_color = PLAYERS[c1_player]["color"]
    #     c1_color = (247, 229, 205, 100) #(10, 21, 23)
    #     c1_border_color = (128, 104, 73, 100)
    #     border_width = 5
    #     radius = int(0.7 * self.variables.HEX_SIZE) # 70 % of hex radius
    #     c1_x, c1_y = center_cords[0] + radius, center_cords[1] + radius
    #     # Create a surface for the circle
    #     circle_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    #     pygame.draw.circle(circle_surface, c1_color, center_cords, radius)
    #     pygame.draw.circle(circle_surface, c1_border_color, center_cords, radius, border_width)
    #     self.screen.blit(circle_surface, (center_cords[0],center_cords[1]))

    def highlight_capture_moves(self, detected_capture_moves):
        
        highlight_color = 247, 62, 102
        highlight_hex_width = self.variables.HEX_WIDTH + 6
        # detected_capture_moves = [[[5, 4], [5, 5]], [[4, 6], [4, 5]]]
        # flat_capture_moves = [[5, 4], [5, 5], [4, 6], [4, 5]]
        detected_capture_moves_np = np.array(detected_capture_moves)
        flat_capture_moves = detected_capture_moves_np.reshape(-1, detected_capture_moves_np.shape[-1])
        # get all the poins of interest from the
        detected_hex_points = [self.variables.HEX_GRID_FLAT_MAP[1][shifted_q][shifted_r][2:-1] for [shifted_q, shifted_r] in flat_capture_moves]
        for hex_points in detected_hex_points:
            # x_center, y_center = hex_points[1], hex_points[1]
            vertices = hex_points[2:]
            assert len(vertices) ==6, "[Debug] hex points are incorrect"
            pygame.draw.polygon(self.screen, highlight_color, vertices, highlight_hex_width)
            
    # Function to draw a button
    def draw_button(self, x, y, width, height, text):
        BUTTON_COLOR = (200, 200, 200)
        TEXT_COLOR = (0, 0, 0)
        pygame.draw.rect(self.screen, BUTTON_COLOR, (x, y, width, height))
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    # Function to check if a point is inside a rectangle
    def is_point_inside_rect(self, x, y, rect):
        return rect.collidepoint(x, y)
