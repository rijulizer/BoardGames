from tkinter import *
from tic_tac_toe_minimax import position_is_free, print_board, check_terminal, minimax

class CustomButton(Button):
    def __init__(self, master=None, button_name=None, **kwargs):
        super().__init__(master, **kwargs)
        self.button_name = button_name


def click_button(event):
    global winning_label
    button = event.widget
    # get button position from button_name
    pos = button.button_name
    game_over, winner = check_terminal(board)
    # game is already over then simpply  return 
    if game_over:
        return 
    else:
        if position_is_free(board, pos):
            board[pos] = player
            button["text"] = player
            print_board(board)
            # check after puting the move if its a terminal move
            game_over, winner = check_terminal(board)
            if not game_over:
                make_bot_move(board, bot, buttons)
            else:
                if winner:
                    print("Winner is - ", winner)
                    winning_label = Label(frame2, text=f"{winner} is Winner !!", width = 12, bg= "orange",font=("Arial", 30))
                    winning_label.grid(row=1, column=0, columnspan=5)
                else:
                    print("Match Draw")
                    winning_label = Label(frame2, text=f"Match Draw ! :/", width = 12, bg= "orange",font=("Arial", 30))
                    winning_label.grid(row=1, column=0, columnspan=5)

        else:
            print("Position already taken!")

def make_bot_move(board, bot, buttons):
    global winning_label
    min_score = +100000 #+np.inf
    for i in board.keys():
        if board[i] == ' ':
            board[i] = bot
            score = minimax(board, 9, True)
            board[i] = ' '
            if score < min_score:
                min_score = score
                best_move = i
    board[best_move]= bot
    buttons[best_move]["text"] = bot
    print_board(board)
    # check after puting the move if its a terminal move
    game_over, winner = check_terminal(board)
    if game_over:
        if winner:
            print("Winner is - ", winner)
            winning_label = Label(frame2, text=f"{winner} is Winner !! :(", width = 12, bg= "orange",font=("Arial", 30))
            winning_label.grid(row=1, column=0, columnspan=5)
        else:
            print("Match Draw")
            winning_label = Label(frame2, text=f"Match Draw ! :/", width = 12, bg= "orange",font=("Arial", 30))
            winning_label.grid(row=1, column=0, columnspan=5)

def restart_game():
    print("Before restart - the board is/n")
    print_board(board)
    print("Game Restarted")
    for i in buttons.keys():
        buttons[i]["text"] = " " 
        board[i] = " "
    winning_label.destroy()
    print("Before restart - the board is/n")
    print_board(board)

def main():
    print("New game !!\nPlayer - X\nBot - O")
    
    global board, player, bot, game_over, winner, buttons, frame2, buttons

    board = {
    1: ' ', 2: ' ', 3: ' ',
    4: ' ', 5: ' ', 6: ' ',
    7: ' ', 8: ' ', 9: ' '
    }
    print_board(board)

    player = 'X'
    bot = 'O'
    print("First Player - ", player)
    game_over  = False
    winner = False

    root = Tk()
    root.geometry("500x500")
    root.title("Tic Tac Toe")

    frame1 = Frame(root)
    frame1.pack()

    title_label = Label(frame1, text="Tic Tac Toe", font=("Ariel", 30), width=20, bg="orchid")
    title_label.pack()
    
    frame2 = Frame(root)
    frame2.pack()

    # display initial tic-tac-toe board with buttons
    # frst row of buttons
    buttons = {}
    i = 0
    for row in range(3):
        for col in range(3):
            i+=1
            buttons[i] = CustomButton(frame2, button_name=i, text= board[i], width=4, height=2, font=("Arial", 30), bg="skyblue", borderwidth=5)
            buttons[i].grid(row = row, column = col)
            buttons[i].bind("<Button-1>", click_button)
            
    restart_button = CustomButton(frame2, button_name='restart', text= "Restart Game", width=15, height=1, font=("Arial", 12), bg="tan", borderwidth=5,
                                  command=restart_game)
    restart_button.grid(row = 4, column = 0, columnspan=5)
    # restart_button.bind("<Button-1>", restart_game)
    # while not game_over:
    # #     # ask for players move
    # #     pos = get_player_move(player)
    # #     # put players move in the board
    # #     make_move(board, pos, player)
    # #     print_board(board)
    # #     if game_over:
    # #         break
    # #     print("debug  -", game_over, winner)
    # #     # player = switch_player(player)
    #     make_bot_move(board, bot)
    #     print_board(board)
    #     game_over, winner = check_terminal(board)
    # if game_over:
    #     if winner:
    #         print("Winner is - ", winner)
    #         winning_label = Label(frame2, text=f"Winner is - {winner}", bg= "orange",font=("Arial", 35))
    #         winning_label.grid(row=3, column=0, columnspan=3)
    #     else:
    #         print("Match Draw")
    #         winning_label = Label(frame2, text=f"Match Draw", bg= "orange",font=("Arial", 35))
    #         winning_label.grid(row=3, column=0, columnspan=3)

    root.mainloop()

if __name__ == "__main__":
    main()


    
