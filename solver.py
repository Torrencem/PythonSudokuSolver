import numpy as np
import math
from copy import deepcopy


class square:
    def __init__(self, solved, value):
        self.value = value
        self.solved = solved
        self.possibilities = list(range(1, 10))

    def __repr__(self):
        return str(self)

    def __str__(self):
        if not self.solved:
            return '^' + str(len(self.possibilities))
        return str(self.value) + '&'

# Returns None if nothing can be done
def sieveCorrect(data):
    doneanything = False
    returndat = []
    for row in data:
        retrow = []
        for sqr in row:
            if not sqr.solved and len(sqr.possibilities) == 1:
                doneanything = True
                retrow.append(square(True, sqr.possibilities[0]))
            else:
                retrow.append(sqr)
        returndat.append(retrow)
    if not doneanything:
        return None
    return np.array(returndat)


def getblock(coords):
    return (math.floor(coords[0] / 3), math.floor(coords[1] / 3))


def sieveLimit(data):
    returndat = data
    for xindex, row in enumerate(data):
        for yindex, sqr in enumerate(row):
            if not sqr.solved:
                continue
            # Knock out all the same numbers in the row and column
            for i in range(0, 9):
                modr = returndat[xindex, i]
                if not modr.solved and sqr.value in modr.possibilities:
                    modr.possibilities.remove(sqr.value)
                elif modr.solved and modr.value == sqr.value and i != yindex:
                    # There is a contradiction!!
                    return False
                modc = returndat[i, yindex]
                if not modc.solved and sqr.value in modc.possibilities:
                    modc.possibilities.remove(sqr.value)
                elif modc.solved and modc.value == sqr.value and i != xindex:
                    return False

            # And also the same minisquare
            minisqr = getblock((xindex, yindex))

            # Might be a better way to do this part
            for x2, row2 in enumerate(data):
                for y2, sqr2 in enumerate(row2):
                    if getblock((x2, y2)) == minisqr and not sqr2.solved:
                        b = sqr2
                        if sqr.value in b.possibilities:
                            b.possibilities.remove(sqr.value)
                            returndat[x2, y2] = b
                    elif getblock((x2, y2)) == minisqr and sqr2.solved and sqr.value == sqr2.value \
                            and (x2 != xindex or y2 != yindex):
                        # Contradiction!
                        return False
                        # Now we have removed the impossible possibilities for this square
    return returndat


# Check if is entirely complete
def checkComplete(data):
    for row in data:
        for sqr in row:
            if not sqr.solved:
                return False
    return True

# Checks for contradictions (zero possibilities)
def checkContr(data):
    for row in data:
        for sqr in row:
            if len(sqr.possibilities) == 0:
                return True

    # We need to check for another kind of contradiction:
    # Where there are two squares in the same row/col that want to
    # be the same thing
    # Sievelimit offers this thing
    a = sieveLimit(data)
    if a is False:
        return True
    return False


def solve(data):
    while True:
        data = sieveLimit(data)
        print(data)
        b = sieveCorrect(data)
        if b is None:
            break
        data = b
    print(data)

    if checkComplete(data):
        print('Done!')
        return data

    # Now we've gotta start branching

    # Doesn't really act as a dictionary, but as a list
    alreadyTried = {}

    # A list of 'undo's
    stack = []

    # What guess we are currently trying
    trying = None

    while not checkComplete(data):
        # print(data)
        if checkContr(data):
            # We've reached a contradiction
            # Restore last stack
            # print(stack)
            data = stack.pop()
            # Add trying to the alreadyTried
            alreadyTried[str(data)] = trying
            trying = None
            # print(data)
            print('Reverting!')
            continue

        data = sieveLimit(data)
        # print(data)
        reduce = sieveCorrect(data)
        if reduce is not None:
            # No branching needed, just reducing
            print('Reducing!')
            data = reduce
            continue

        # Reducing doesn't work, need to branch

        # Find all of the coordinates of ^2's in the puzzle (guessing points)
        guessingpoints = []
        for xin, row in enumerate(data):
            for yin, sqr in enumerate(row):
                if not sqr.solved and len(sqr.possibilities) == 2:
                    guessingpoints.append((xin, yin))

        if len(guessingpoints) == 0:
            # We've got a problem
            print('BAD')
            pass

        if str(data) in alreadyTried:
            p = guessingpoints[0]  # We really only have to work with the first guessing point
            # We've tried p's first guess, so it has to be the second one
            fill = data[p[0], p[1]].possibilities[1]
            data[p[0], p[1]].solved = True
            data[p[0], p[1]].value = fill
            print('Doing Second Guess')
            continue
        else:
            p = guessingpoints[0]
            # We're just gonna try p's first guess
            trying = (p[0], p[1])
            stack.append(deepcopy(data))
            fill = data[p[0], p[1]].possibilities[0]
            data[p[0], p[1]].solved = True
            data[p[0], p[1]].value = fill
            print('Doing First Guess')
            continue

    return data

def datfromtext(text):
    text = text.replace(' ','')
    if len(text) == 90:
        # Probably a newline at the end...
        text = text[:-1]
    if len(text) != 89:
        raise Exception('Make sure the puzzle is formatted correctly!')

    text = str.split(text,'\n')

    sqrs = []

    for line in text:
        sqrs.append([square(char != 'x', 0 if char == 'x' else int(char)) for char in line])

    data = np.array(sqrs)
    return data

def formatNicely(data):
    outstr = ''
    for y, line in enumerate(data):
        for x, sqr in enumerate(line):
            if not sqr.solved:
                repstring = '?'
            else:
                repstring = str(sqr.value)
            outstr += repstring
            if x % 3 == 2:
                outstr += ' '
        if y % 3 == 2:
            outstr += '\n'
        outstr += '\n'
    return outstr


if __name__ == '__main__':
    with open('puzzle.txt', 'r') as file:
        puzzle = str.join('', file.readlines())

    data = datfromtext(puzzle)
    print(formatNicely(solve(data)))