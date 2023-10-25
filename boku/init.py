import numpy as np

class BoardVariables():
    """
    The class has all the neccessary variables which should be initialized
    """
    def __init__(self,):
        
        print("[DEBUG]- Initiating Board Variables...")
        # Constants
        self.WIDTH, self.HEIGHT = 1200, 800
        # GRID_RADIUS = 6  # Grid radius, determines the size of the grid
        self.HEX_SIZE = 40  # Hexagon size
        self.BG_COLOR = (117, 228, 250)
        self.HEX_COLOR = (89, 86, 82)
        self.HEX_WIDTH = 5
        self.FONT_SIZE = 40
        self.LABEL_COLOR = (255,0,0)
        # boku rules:
        # continuous positions to win boku
        self.boku_rule_cont_pos = 5

        self.PLAYERS = {
            "p1":{
                "symbol": 1,
                "color": (247, 229, 205),
            },
            "p2":{
                "symbol": 0,
                "color": (10, 21, 23),
            }
        }
        self.empty_space = -1
        # preset trap patterns - [[0,1,1,0],[1,0,0,1]
        self.TRAP_PATTERN = [
            [self.PLAYERS["p1"]["symbol"], self.PLAYERS["p2"]["symbol"], self.PLAYERS["p2"]["symbol"],self.PLAYERS["p1"]["symbol"]],
            [self.PLAYERS["p2"]["symbol"], self.PLAYERS["p1"]["symbol"], self.PLAYERS["p1"]["symbol"],self.PLAYERS["p2"]["symbol"]],
        ]
        # manually create the hex grid cube co-ordinates
        self.HEX_GRID_CORDS = {
                # x=0, y<0
                'F6': [0,0],
                'E5': [0,1],
                'D4': [0,2],
                'C3': [0,3],
                'B2': [0,4],
                'A1': [0,5],
                # x=0, y>0
                'G7': [0,-1],
                'H8': [0,-2],
                'I9': [0,-3],
                'J10': [0,-4],
                
                # x=-1, y<0
                'F7': [-1,0],
                'E6': [-1,1],
                'D5': [-1,2],
                'C4': [-1,3],
                'B3': [-1,4],
                'A2': [-1,5],
                # x=-1, y<0
                'G8': [-1,-1],
                'H9': [-1,-2],
                'I10': [-1,-3],
                
                # x=-2, y<0
                'F8': [-2,0],
                'E7': [-2,1],
                'D6': [-2,2],
                'C5': [-2,3],
                'B4': [-2,4],
                'A3': [-2,5],
                # x=-2, y<0
                'G9': [-2,-1],
                'H10': [-2,-2],

                # x=-3, y<0
                'F9': [-3,0],
                'E8': [-3,1],
                'D7': [-3,2],
                'C6': [-3,3],
                'B5': [-3,4],
                'A4': [-3,5],
                # x=-3, y<0
                'G10': [-3,-1],

                # x=-4, y<0
                'F10': [-4,0],
                'E9': [-4,1],
                'D8': [-4,2],
                'C7': [-4,3],
                'B6': [-4,4],
                'A5': [-4,5],
                
                # x=-5 , y<0
                'E10': [-5,1],
                'D9': [-5,2],
                'C8': [-5,3],
                'B7': [-5,4],
                'A6': [-5,5],

                # x=1, y<0
                'F5': [1,0],
                'E4': [1,1],
                'D3': [1,2],
                'C2': [1,3],
                'B1': [1,4],
                # x=1, y<0
                'G6': [1,-1],
                'H7': [1,-2],
                'I8': [1,-3],
                'J9': [1,-4],
                
                # x=2, y<0
                'F4': [2,0],
                'E3': [2,1],
                'D2': [2,2],
                'C1': [2,3],
                # x=2, y>0
                'G5': [2,-1],
                'H6': [2,-2],
                'I7': [2,-3],
                'J8': [2,-4],

                # x=3, y<0
                'F3': [3,0],
                'E2': [3,1],
                'D1': [3,2],
                # x=3, y>0
                'G4': [3,-1],
                'H5': [3,-2],
                'I6': [3,-3],
                'J7': [3,-4],

                # x=4 y<0
                'F2': [4,0],
                'E1': [4,1],
                # x=4, y>0
                'G3': [4,-1],
                'H4': [4,-2],
                'I5': [4,-3],
                'J6': [4,-4],
                
                # x=5
                'F1': [5,0],
                # x=5, y>0
                'G2': [5,-1],
                'H3': [5,-2],
                'I4': [5,-3],
                'J5': [5,-4],
                
            }

        # Create flat map grid to map (q,r) to sqare matrix and fill with -1. 
        # This will be used to check contiguous occurence of player tokens
        # the lowest q nad r is translated to zero Ex- {-5 -> 0, 5->10}
        # HEX_GRID_FLAT_MAP
        # (0,q,r) -> player symbols
        # (1,q,r) -> mapping from flat_map to hex_info
        self.HEX_GRID_FLAT_MAP = [[[self.empty_space if [q-5,r-4] in self.HEX_GRID_CORDS.values() else None for r in range(0,10)] for q in range(0,11)],
                            [[None for r in range(0,10)] for q in range(0,11)]]
        # self.board_pos_values = {}
        # self.get_pos_values()
    
    # def get_pos_values(self):
    #     """
    #     assigns value to an empty board based on different codnitions
    #     # 1. proximity to center
    #     """
    #     # proximity to center value, values range from 5 to 0 fromcenter to extreme outer hex
    #     for key, val in self.HEX_GRID_CORDS.items():
    #         q, r = val
    #         s = -q -r
    #         self.board_pos_values[key] = int(5 - np.max(np.abs(np.array([q,r,s]))))


if __name__ == "__main__":
    board_variables =  BoardVariables()
    print("[DEBUG]- [Boardvariables]- Players - ",board_variables.PLAYERS)