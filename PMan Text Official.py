"""
from random import randint

def setBoardPython():
    global board
    board = []
    for Rows in range(0,20,1): 
        board.append(["| |"] * 10)
    for Wall in range(0,100,1):
        Walls = randint(0,5)
        RandX = randint(0,10)
        RandY = randint(0,20)
        if Walls == 4:
            board[RandY-1][RandX-1] = "|/|"
"""
def setBoardFile():
    global board
    board = []
    Map = open("Map1.txt","r")
    Maps = Map.read()
    Maps = Maps.split("\n")
    for Rows in range(0,20,1):
        board.append([])
        Maps2 = Maps[Rows].split("  ")
        for Columns in range(0,10,1):
            board[Rows].append(Maps2[Columns])
    

def printBoard():
    for Row in board:
        print(" ".join(Row))

def gameDef():
    print("Welcome to pac man!")
    while True:
        x = 1
        y = 1
        xadd = 0
        yadd = 0
        score = 0
        dont = True
        print("WASD to move.")
        while True:
            x = x + xadd
            y = y + yadd
            board[y][x] = "|O|"
            if dont == False:
                board[y-yadd][x-xadd]= "| |"
            dont = False
            printBoard()
            print(x,y)
            while True:
                while True:
                    move = str(input())
                    if move == "w":
                        xadd = 0
                        yadd = -1
                        break
                    elif move == "a":
                        xadd = -1
                        yadd = 0
                        break
                    elif move == "s":
                        xadd = 0
                        yadd = 1
                        break
                    elif move == "d":
                        xadd = 1
                        yadd = 0
                        break
                if x + xadd == 10:
                    if board[y+yadd][0] != "| |":
                        print("Ouff. You hit a wall.")
                    else:
                        x = -1
                        break
                elif y + yadd == 20:
                    if board[0][x+xadd] != "| |":
                        print("Ouff. You hit a wall.")
                    else:
                        y = -1
                        break
                elif x + xadd == -1:
                    if board[y+yadd][9] != "| |":
                        print("Ouff. You hit a wall.")
                    else:
                        x = 10
                        board[y-yadd][0]= "| |"
                        dont = True
                        break
                elif y + yadd == -1:
                    if board[19][x+xadd] != "| |":
                        print("Ouff. You hit a wall.")
                    else:
                        y = 20
                        board[0][x-xadd]= "| |"
                        dont = True
                        break
                if board[y+yadd][x+xadd] == "|W|":
                    print("Ouff. You hit a wall.")
                elif board[y+yadd][x+xadd] == "|•|":
                    score = score + 1
                    print("                                           Your score is now %s!" % (score))
                    break
                else:
                    break
                

setBoardFile()
gameDef()




