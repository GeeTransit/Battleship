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

def printboard(board, phrase=None):
    print()
    if phrase is not None:
        print(phrase)
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
    print("   1 2 3 4 5 6 7 8 9 10")
    print()

def checkboard(reportboard):
# True = game is ongoing
# False = game is finished
    for row in reportboard:
        if 1 in row:
            return True
    return False

'''
Setup

player set ships
for i in shipsizes :
print (where do you want your i ship)
input y
input x
input direction

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
change variable name (rep ==> report)
'''

bombboard1 = newboard()
bombboard2 = newboard()
reportboard1 = newboard()
reportboard2 = newboard()


shipsizes = [2, 3, 3, 4, 5]

# # creating player board
# for shipsize in shipsizes:
    # while True:
        # y = randint(0,7)
        # x = randint(0,7)
        # shipdirection = randint(0,1)
        # if checkship(reportboard1, y, x, shipsize, shipdirection):
            # break
    # addship(reportboard1, y, x, shipsize, shipdirection)


# creating robo board
for shipsize in shipsizes:
    while True:
        y = randint(0,7)
        x = randint(0,7)
        shipdirection = randint(0,1)
        if checkship(reportboard2, y, x, shipsize, shipdirection):
            break
    addship(reportboard2, y, x, shipsize, shipdirection)

# player setting ships
for length in shipsizes:
    printboard(reportboard1, f"WHERE DO YOU WANT YOUR LENGTH {length} SHIP?")
    #taking input
    while True:
        try:
            # checking y and x
            y = int(input("Y POSITION:")) - 1
            if not 0 <= y <= 9:
                print("DAmn bro")
                continue
            x = int(input("X POSITION:")) - 1
            if not 0 <= x <= 9:
                print("DAmn bro")
                continue
            # checking direction
            direction = int(input("DIRECTION (0 = horizontal, 1 = vertical):"))
            if direction not in [0, 1]:
                print("DAmn bro")
                continue
        #checking other random stuff
        except ValueError:
            print("DAmn bro")
            continue
        # checking placement
        if not checkship(reportboard1, y, x, length, direction):
            print("DAmn bro")
            continue
        break
    # adding ship
    addship(reportboard1, y, x, length, direction)

printboard(reportboard1, "OUR FLEET STATUS")

# game loop
while True:

    printboard(bombboard1, "WHERE DO YOU WANT TO BOMB?")

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
    printboard(bombboard1, "BOMBING REPORT")

    if not checkboard(reportboard2):
        print()
        print("YOU HAVE WON THE WAR")
        break
    input()

    # robo bombing
    while True:
        y = randint(0, 9)
        x = randint(0, 9)
        if not checkhit(bombboard2, y, x):
            continue
        break

    hit(bombboard2, y, x, reportboard1)
    printboard(reportboard1, "OUR FLEET STATUS")

    if not checkboard(reportboard1):
        print()
        print("YOU HAVE LOST THE WAR")
        break
    input()