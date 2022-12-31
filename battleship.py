from random import randint
from pprint import pp

def newboard():
    board = []

    for i in range(10):
        # board.append(0)
        miniboard = []
        for i in range(10):
            miniboard.append(0)
        board.append(miniboard)

    return board

def addship(board, y, x, shiplength, shipdirection):
    # 1 = vertical
    # 0 = horizontal
    for i in range(shiplength):
        if shipdirection == 1:
            board[y+i][x] = 1
        if shipdirection == 0:
            board[y][x+i] = 1

def checkship(board, y, x, shiplength, shipdirection):
    # 1 = vertical
    # 0 = horizontal

    # checking if outside board
    if shipdirection == 1:
        if shiplength + y > 10:
            return False
    if shipdirection == 0:
        if shiplength + x > 10:
            return False

    # checking if ship already exists
    for i in range(shiplength):
        if shipdirection == 1:
            if board[y+i][x] == 1:
                return False
        if shipdirection == 0:
            if board[y][x+i] == 1:
                return False

    return True

def hit(opbombboard, y, x, ourrepboard):
    # 0 = sea
    # 1 = ship unhit
    # 2 = ship hit
    # 3 = bomb sea
    if ourrepboard[y][x] == 0:
        ourrepboard[y][x] = 3
        opbombboard[y][x] = 3
        return 0
    if ourrepboard[y][x] == 1:
        ourrepboard[y][x] = 2
        opbombboard[y][x] = 2

def checkhit(opbombboard, y, x):
    if opbombboard[y][x] in [2, 3]:
        return False
    return True

def printboard(board):
    # adding y-axis numbers
    for num, List in enumerate(board):
        # formating y-axis
        print (f'{num + 1:2}', end = " ")
        # changing number to symbols
        for item in List:
            if item == 0:
                print("•", end = " ")
            if item == 1:
                print("■", end = " ")
            if item == 2:
                print("▣", end = " ")
            if item == 3:
                print("○", end = " ")
        print()
    # adding x-axis
    print("  1 2 3 4 5 6 7 8 9 10")
    print()

'''
Setup

player set ships
input y
input x

robo set ships


Game loop

forever
    player bomb
        report recieve
    if 1 not in robo
        print("YOU HAVE WON THE WAR")
        break
    robo bomb
        bombboard recieve
    if 1 not in player
        print("YOU HAVE LOST THE WAR")
        break


todo:
make last hit diff emoji
'''

bombboard1 = newboard()
bombboard2 = newboard()
reportboard1 = newboard()
reportboard2 = newboard()


shipsizes = [2, 3, 3, 4, 5]

# creating player board
for shipsize in shipsizes:
    while True:
        y = randint(0,7)
        x = randint(0,7)
        shipdirection = randint(0,1)
        if checkship(reportboard1, y, x, shipsize, shipdirection):
            break
    addship(reportboard1, y, x, shipsize, shipdirection)


# creating robo board
for shipsize in shipsizes:
    while True:
        y = randint(0,7)
        x = randint(0,7)
        shipdirection = randint(0,1)
        if checkship(reportboard2, y, x, shipsize, shipdirection):
            break
    addship(reportboard2, y, x, shipsize, shipdirection)


# game loop
while True:
    print()
    print("WHERE DO YOU WANT TO BOMB?")
    printboard(bombboard1)

    # player bombing
    while True:
        try:
            y = int(input("Y POSITION OF BOMB (1-10): ")) - 1
            if not 0 <= y <= 9:
                print("DAmn bro")
                continue
            x = int(input("X POSITION OF BOMB (1-10): ")) - 1
            if not 0 <= x <= 9:
                print("DAmn bro")
                continue
        except ValueError:
            print("DAmn bro")
            continue

        if not checkhit(bombboard1, y, x):
            print()
            print("nah bro, bombed already")
            print()
            continue
        break

    hit(bombboard1, y, x, reportboard2)

    print()
    print("BOMBING REPORT")
    printboard(bombboard1)
    input()

    # robo bombing
    while True:
        y = randint(0, 9)
        x = randint(0, 9)
        if not checkhit(bombboard2, y, x):
            continue
        break

    hit(bombboard2, y, x, reportboard1)

    print()
    print("OUR FLEET STATUS")
    printboard(reportboard1)
    input()
