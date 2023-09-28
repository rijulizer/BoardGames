board = {
    1: 'X', 2: ' ', 3: ' ',
    4: ' ', 5: ' ', 6: ' ',
    7: ' ', 8: ' ', 9: 'O'
    }
def print_board(board):
    print(board[1]+ '|' + board[2]+ '|' + board[3])
    print('-+-+-')
    print(board[4]+ '|' + board[5]+ '|' + board[6])
    print('-+-+-')
    print(board[7]+ '|' + board[8]+ '|' + board[9])
    print("\n")

def position_is_free(board, position):
    if board[position] == ' ':
        return True
    else:
        return False


def make_move(board, position, player: str):
    if position_is_free(board, position):
        board[position] = player
    else:
        print("Position already taken!")

def check_terminal(board):
    # row 1
    if (board[1] == board[2]) and (board[2] == board[3]) and (board[1] != ' '):
        terminal = True
        winner = board[1]
        return terminal, winner
    # row 2
    elif (board[4] == board[5]) and (board[5] == board[6]) and (board[4] != ' '):
        terminal = True
        winner = board[4]
        return terminal, winner
    # row 3
    elif (board[7] == board[8]) and (board[7] == board[9]) and (board[7] != ' '):
        terminal = True
        winner = board[7]
        return terminal, winner
    # col 1
    elif (board[1] == board[4]) and (board[1] == board[7]) and (board[1] != ' '):
        terminal = True
        winner = board[1]
        return terminal, winner
    # col 2
    elif (board[2] == board[5]) and (board[2] == board[8]) and (board[2] != ' '):
        terminal = True
        winner = board[2]
        return terminal, winner
    # col 3
    elif (board[3] == board[6]) and (board[3] == board[9]) and (board[3] != ' '):
        terminal = True
        winner = board[3]
        return terminal, winner
    # diagonal 1
    elif (board[1] == board[5]) and (board[1] == board[9]) and (board[1] != ' '):
        terminal = True
        winner = board[1]
        return terminal, winner
    # diagonal 2
    elif (board[3] == board[5]) and (board[3] == board[7]) and (board[3] != ' '):
        terminal = True
        winner = board[3]
        return terminal, winner    
    # draw scenario or incomplete
    else:
        winner = False
        terminal = True
        # check all rows if one empty then not a terminal state
        for i in board.values():
            if i == " ":
                terminal = False
        # otheriwse draw match
        return terminal, winner
    
def get_player_move(player: str):
    print(f"Enter {player} move position - ")
    pos = int(input())
    print(pos)
    return pos

def switch_player(player: str):
    if player == 'X':
        return "O"
    elif player == 'O':
        return "X"
    else:
        raise ValueError("Player should be X or O .")

def main():
    print("New game !!\nPlayer - X\nBot - O")
    board = {
    1: ' ', 2: ' ', 3: ' ',
    4: ' ', 5: ' ', 6: ' ',
    7: ' ', 8: ' ', 9: ' '
    }
    print_board(board)
    
    game_over  = False
    player = "X"
    while not game_over:
        pos = get_player_move(player)
        make_move(board, pos, player)
        print_board(board)
        game_over, winner = check_terminal(board)
        print("debug  -", game_over, winner)
        player = switch_player(player)
    if winner:
        print("Winner is - ", winner)
    else:
        print("Match Draw")

main()
    