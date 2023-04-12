
def InitializeBoard():
    board = []
    for i in range(4):  # 4 layers
        layer = []
        for j in range(4):  # 4 rows
            row = []
            for k in range(4):  # 4 columns
                row.append('.')
            layer.append(row)
        board.append(layer)
    return board

def SetPlayer(player):
    if player[1] == 0 :
        player[0] = 'X' if player[0]=='O' else 'O'
        # player = 'X'  # set the initial player to 'X'
    return player

def PrintBoard(board):
    for i in range(len(board)):
        print("Layer " + str(i + 1) + ":")
        for j in range(len(board[i])):
            row = ""
            for k in range(len(board[i][j])):
                row += board[i][j][k] + " "
            print(row)
        print("")

def check_all_values(lst):
    for elem in lst :
        if not elem :
            return False
    return True

def GetPlayerMove(player):
    move = input("Player " + player[0] + " (" + str(player[1]) + " wrong moves), enter your move (row v, column >): ")
    move = move.strip().split(",")
    print(check_all_values(move))
    if len(move) == 2 and check_all_values(move):
        # check that the move is inside range
        if int(move[0]) > 0 and int(move[0]) < 5 and int(move[1]) > 0 and int(move[1]) < 5 :
            layer = 3 # always put the marker on the top layer
            row = int(move[0]) - 1
            column = int(move[1]) - 1
            return (layer, row, column)
        else :
            print("Invalid move")
            player[1] += 1

def DropPiece(board, move, player):
    # print(type(move))
    if isinstance(move, tuple) and len(move) == 3:
        layer, row, column = move
        if board[layer][row][column] == '.':
            # move marker downwards as far as it goes
            for i in range(4) :
                if board[i][row][column] == '.' :
                    board[i][row][column] = player[0]
                    player[1] = 0
                    break # for loop is done

        else:
            print("Invalid move")
            player[1] += 1
    else:
        print("Invalid move")
        player[1] += 1

    return board

def CheckWin(board, player):
    # Check all 3D diagonals
    for i in range(4):
        if board[i][0][0] == player[0] and board[i][1][1] == player[0] and board[i][2][2] == player[0] and board[i][3][3] == player[0]:
            return True
        if board[i][3][0] == player[0] and board[i][2][1] == player[0] and board[i][1][2] == player[0] and board[i][0][3] == player[0]:
            return True
    if board[0][0][0] == player[0] and board[1][1][1] == player[0] and board[2][2][2] == player[0] and board[3][3][3] == player[0]:
        return True
    if board[0][3][0] == player[0] and board[1][2][1] == player[0] and board[2][1][2] == player[0] and board[3][0][3] == player[0]:
        return True

    # Check all 3D verticals and horizontals
    for i in range(4):
        for j in range(4):
            if board[i][j][0] == player[0] and board[i][j][1] == player[0] and board[i][j][2] == player[0] and board[i][j][3] == player[0]:
                return True
            if board[i][0][j] == player[0] and board[i][1][j] == player[0] and board[i][2][j] == player[0] and board[i][3][j] == player[0]:
                return True
            if board[0][i][j] == player[0] and board[1][i][j] == player[0] and board[2][i][j] == player[0] and board[3][i][j] == player[0]:
                return True

    return False

def CheckTie(board):
    for layer in range(4):
        for row in range(4):
            for column in range(4):
                if board[layer][row][column] == '.':
                    return False
    return True

def PrintWinner(player):
    print(f"Congratulations player {player[0]}, you have won the game!")

def PrintTie():
    print("The game has ended in a tie.")


def main():
    board = InitializeBoard()
    player = ['X', 0]
    PrintBoard(board)
    
    while True:
        move = GetPlayerMove(player)
        DropPiece(board, move, player)
        PrintBoard(board)
        
        if CheckWin(board, player):
            PrintWinner(player)
            break
        
        if CheckTie(board):
            PrintTie()
            break
        
        player = SetPlayer(player)

if __name__ == '__main__':
    main()
