from IPython.display import clear_output
import random


def display_board(board):
    clear_output()
    print(f"{board[7]} | {board[8]} | {board[9]}")
    print("--|---|--")
    print(f"{board[4]} | {board[5]} | {board[6]}")
    print("--|---|--")
    print(f"{board[1]} | {board[2]} | {board[3]}")


test_board = ["#", "x", "o", "x", "o", "x", "o", "x", "o", "x"]
display_board(test_board)


def player_input():
    marker = ""
    while marker != "x" and marker != "o":
        marker = input("Please input x or o: ")
    player1 = marker
    if player1 == "x":
        player2 = "o"
    else:
        player2 = "x"

    return f"player1 - {player1} player2 - {player2}  "


print(player_input())

def board_position(board, marker, position):
    board[position] = marker


print(board_position(test_board, "5", 5))
display_board(test_board)

def win_test(board, marker):
    if board[1] == board[2] == board[3] == marker or board[4] == board[5] == board[6] == marker or board[7] == board[8] == board[9] == marker:
        return f" you win"
    elif board[1] == board[4] == board[7] == marker or board[2] == board[5] == board[8] == marker or board[3] == board[6] == board[9] == marker:
        return f"You win"
    elif board[3] == board[5] == board[7] == marker or board[1] == board[5] == board[9] == marker:
        return f"You win"
    else:
        return f"nichya"

def choose_first():
    flip = random.randint(0,1)
    if flip ==1:
        return "player1"
    else:
        return "player2"

def space_check(board, position):
    return board[position] == " "

def full_board_check(board):
    for i in range(1,10):
        if space_check(board,i):
            return False

    return True

# выбор игрока
def player_choise(board):
    position = 0
    while position not in [1,2,3,4,5,6,7,8,9] or not space_check(board, position):
        position = int(input("chack a position: (1-9)"))
        return  position

def replay():
    choise = input("Do you want to play again? (please input yes or no)")
    return choise == "yes"



print("welcome to game X or O")
