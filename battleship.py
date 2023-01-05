from random import randint, shuffle, choice

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
    shippoints = []
    for i in range(shiplength):
        # put all points in variable
        if shipdirection == 1:
            board[y+i][x] = 1
            shippoints.append([y+i, x])
        if shipdirection == 0:
            board[y][x+i] = 1
            shippoints.append([y, x+i])
    return shippoints

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

def hit(opbombboard, y, x, ourreportboard):
    # 0 = sea
    # 1 = ship unhit
    # 2 = ship hit
    # 3 = bomb sea
    if ourreportboard[y][x] == 0:
        ourreportboard[y][x] = 3
        opbombboard[y][x] = 3
        return 0
    if ourreportboard[y][x] == 1:
        ourreportboard[y][x] = 2
        opbombboard[y][x] = 2

def checkhit(opbombboard, y, x):
    if not 0 <= y <= 9:
        return False
    if not 0 <= x <= 9:
        return False
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

def checkboard(reportboard):
# True = game is ongoing
# False = game is finished
    for row in reportboard:
        if 1 in row:
            return True
    return False

def randomboard(reportboard, shipsizes, shipspoints):
    for length in shipsizes:
        while True:
            y = randint(0,9)
            x = randint(0,9)
            direction = randint(0,1)
            if checkship(reportboard, y, x, length, direction):
                break
        shipspoints.append(addship(reportboard, y, x, length, direction))

def customboard(reportboard, shipsizes, shipspoints):
    for length in shipsizes:
        printboard(reportboard1, f"WHERE DO YOU WANT YOUR LENGTH {length} SHIP?")
        print()
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
            if not checkship(reportboard, y, x, length, direction):
                print("DAmn bro")
                continue
            break
        # adding ship
        shipspoints.append(addship(reportboard, y, x, length, direction))

def switchuser(prompt):
    for i in range(50):
        print()
    input(prompt)

def shipdown(y, x, ourbombboard, opshipspoints):
    for shippoints in opshipspoints:
        if [y, x] in shippoints:
            for [y, x] in shippoints:
                if ourbombboard[y][x] != 2:
                    return False
            return True

def firstfree(ourbombboard, y, x, dx, dy):
    # returns [y, x] or raises ValueError if not found
    while True:
        y += dy
        x += dx
        if not 0 <= y < 10 or not 0 <= x < 10:  # outside board
            break
        if ourbombboard[y][x] == 3:  # bombed sea
            break
        if ourbombboard[y][x] == 0:  # can hit
            return [y, x]
    raise ValueError("no free tile found")

sidedeltas = [
    # dy, dx
    [+1, 0],  # down
    [0, +1],  # right
    [-1, 0],  # up
    [0, -1],  # left
]

def calculatescore(ourbombboard, y, x):
    # the weights here were reached by trial and error
    tilescore = 0
    for dy, dx in sidedeltas:
        dy += y
        dx += x
        if not 0 <= dy < 10 or not 0 <= dx < 10:  # outside board
            tilescore -= 1
        elif ourbombboard[dy][dx] == 3:  # bombed sea
            tilescore -= 2
    return tilescore
'''
todo:
make last hit diff emoji

make robo smarter!
- continue using older ship locations

more meaningful feedback messages
'''

bombboard1 = newboard()
bombboard2 = newboard()
reportboard1 = newboard()
reportboard2 = newboard()

lastxhit = None
lastyhit = None

shipsizes = [2, 3, 3, 4, 5]

potentialshipspace = 0

shipspoints1 = []
shipspoints2 = []

x = 0
y = 0

yrobo = 0
xrobo = 0

lastydelta = None
lastxdelta = None

roboscores = {
    (y, x): calculatescore(bombboard2, y, x)
    for y in range(10)
    for x in range(10)
}

# setting gamemode (loner or not)
while True:
    print("Which gamemode?")
    print("1. Singleplayer")
    print("2. Multiplayer")
    try:
        gamemode = int(input("1 or 2?"))
        if gamemode not in [1, 2]:
            continue
    except ValueError:
        continue
    break

if gamemode == 2:
    print("PLAYER 1 SETUP")
    input()
# creating player's board
while True:
    boardtype = input("Do you want a random board (yes or no)?\n")
    if boardtype not in ["yes", "no"]:
        print("DAmn  bro")
        continue
    break

# random player board
if boardtype == "yes":
    randomboard(reportboard1, shipsizes, shipspoints1)

# custom player board
if boardtype == "no":
    customboard(reportboard1, shipsizes, shipspoints1)

printboard(reportboard1, "OUR FLEET STATUS")

# creating robo board
if gamemode == 1:
    input()
    randomboard(reportboard2, shipsizes, shipspoints2)

# creating player 2 board
if gamemode == 2:
    input("READY FOR BATTLE?")
    switchuser("PLAYER 2 SETUP")

    # creating player's board
    while True:
        boardtype = input("Do you want a random board (yes or no)?\n")
        if boardtype not in ["yes", "no"]:
            print("DAmn  bro")
            continue
        break

    # random player board
    if boardtype == "yes":
        randomboard(reportboard2, shipsizes, shipspoints2)

    # player setting ships
    if boardtype == "no":
        customboard(reportboard2, shipsizes, shipspoints2)

    printboard(reportboard2, "OUR FLEET STATUS")

    input("READY FOR BATTLE?")
    switchuser("PLAYER 1 TURN")


# game loop
while True:

    printboard(reportboard1, "OUR FLEET STATUS")
    if gamemode == 2:
        if shipdown(y, x, bombboard2, shipspoints1):
            print("! OUR SHIP DOWN !")
    if gamemode == 1:
        if shipdown(yrobo, xrobo, bombboard2, shipspoints1):
            print("! OUR SHIP DOWN !")

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

    if shipdown(y, x, bombboard1, shipspoints2):
        print("! ENEMY SHIP DOWN !")

    # checking player's bombing
    if not checkboard(reportboard2):
        print()
        print("YOU HAVE WON THE WAR")
        print()
        printboard(reportboard1)
        break
    print()
    input("ARE YOU WANNA NEXT TURN???")

    # robo bombing
    if gamemode == 1:

        # check in same direction
        if (
            potentialshipspace == 0
            and lastyhit is not None
            and lastydelta is not None
        ):
            try:
                yrobo, xrobo = firstfree(
                    bombboard2,
                    lastyhit, lastxhit,
                    lastydelta, lastxdelta,
                )
            except ValueError:
                pass
            else:
                potentialshipspace = 1

        # check in opposite direction
        if (
            potentialshipspace == 0
            and lastyhit is not None
            and lastydelta is not None
        ):
            try:
                yrobo, xrobo = firstfree(
                    bombboard2,
                    lastyhit, lastxhit,
                    -lastydelta, -lastxdelta,
                )
            except ValueError:
                pass
            else:
                potentialshipspace = 1
                lastydelta = -lastydelta
                lastxdelta = -lastxdelta

        # checking last ship hit position
        if lastyhit is not None and potentialshipspace == 0:
            # making a list of spaces around (list it all)
            randposition = [
                [lastyhit-1, lastxhit],
                [lastyhit+1, lastxhit],
                [lastyhit, lastxhit-1],
                [lastyhit, lastxhit+1],
            ]
            shuffle(randposition)
            # checking each location
            for yrobo, xrobo in randposition:
                if not checkhit(bombboard2, yrobo, xrobo):
                    continue
                potentialshipspace = 1
                lastydelta = yrobo - lastyhit
                lastxdelta = xrobo - lastxhit
                break

        if potentialshipspace == 0:
            # creates new bomb position
            maxscore = max(roboscores.values())
            yrobo, xrobo = choice([
                yx
                for yx, score in roboscores.items()
                if score == maxscore
            ])

        hit(bombboard2, yrobo, xrobo, reportboard1)
        potentialshipspace = 0

        # update scores of surrounding squares
        del roboscores[(yrobo, xrobo)]
        for dy, dx in sidedeltas:
            sy = yrobo + dy
            sx = xrobo + dx
            if (sy, sx) in roboscores:
                roboscores[(sy, sx)] = calculatescore(bombboard2, sy, sx)

        # resets lasty and lastx hit if ship down
        if shipdown(yrobo, xrobo, bombboard2, shipspoints1):
            lastyhit = None
            lastxhit = None
            lastydelta = None
            lastxdelta = None

        # add last ship hit positions
        elif bombboard2[yrobo][xrobo] == 2:
            lastyhit = yrobo
            lastxhit = xrobo

        # checking robo's bombing
        if not checkboard(reportboard1):
            printboard(reportboard2)
            print("YOU HAVE LOST THE WAR")
            print()
            break
        input()


    if gamemode == 2:
        switchuser("PLAYER 2 TURN")

        printboard(reportboard2, "OUR FLEET STATUS")
        if shipdown(y, x, bombboard1, shipspoints2):
            print("! OUR SHIP DOWN !")

        printboard(bombboard2, "WHERE DO YOU WANT TO BOMB?")

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

            if not checkhit(bombboard2, y, x):
                print()
                print("nah bro, bombed already")
                print()
                continue
            break

        hit(bombboard2, y, x, reportboard1)
        printboard(bombboard2, "BOMBING REPORT")

        if shipdown(y, x, bombboard2, shipspoints1):
            print("! ENEMY SHIP DOWN !")

        # checking player's bombing
        if not checkboard(reportboard1):
            printboard(reportboard2)
            print("YOU HAVE WON THE WAR")
            print()
            break

        input("ARE YOU WANNA NEXT TURN???")
        switchuser("PLAYER 1 TURN")
