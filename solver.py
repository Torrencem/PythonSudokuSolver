import numpy as np
import math
class square:
    def __init__(self, solved, value):
        self.value = value
        self.solved = solved
        self.possibilities = list(range(1,10))

    def __repr__(self):
        return str(self)

    def __str__(self):
        if not self.solved:
            return '^' + str(len(self.possibilities))
        return str(self.value) * 2



with open('puzzle.txt', 'r') as file:
    puzzle = str.join('', file.readlines())

puzzle = puzzle.replace(' ','')
print(puzzle)
# Check if is a valid puzzle
if len(puzzle) != 89:
    raise Exception('Make sure the puzzle is formatted correctly!')

puzzle = str.split(puzzle, '\n')
puzzlesqrs = []

for line in puzzle:
    puzzlesqrs.append([square(char != 'x', 0 if char == 'x' else int(char)) for char in line])

data = np.array(puzzlesqrs)
print(data)

# Now should be done loading the data in

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
    return (math.floor(coords[0]/3),math.floor(coords[1]/3))

def sieveLimit(data):
    returndat = data
    for xindex, row in enumerate(data):
        for yindex, sqr in enumerate(row):
            if not sqr.solved:
                continue
            # Knock out all the same numbers in the row and column
            for i in range(0,9):
                modr = returndat[xindex, i]
                if not modr.solved and sqr.value in modr.possibilities:
                    modr.possibilities.remove(sqr.value)
                modc = returndat[i, yindex]
                if not modc.solved and sqr.value in modc.possibilities:
                    modc.possibilities.remove(sqr.value)

            # And also the same minisquare
            minisqr = getblock((xindex,yindex))

            # Might be a better way to do this part
            for x2, row2 in enumerate(data):
                for y2, sqr2 in enumerate(row2):
                    if getblock((x2,y2)) == minisqr and not sqr2.solved:
                        b = sqr2
                        if sqr.value in b.possibilities:
                            b.possibilities.remove(sqr.value)
                            returndat[x2,y2] = b
            # Now we have removed the impossible possibilities for this square
    return returndat

while True:
    data = sieveLimit(data)
    print(data)
    b = sieveCorrect(data)
    if b is None:
        break
    data = b
    print(data)
print(data)
# experiment = []
# for x in range(9):
#     print(x)
#     temprow = []
#     for y in range(9):
#         temprow.append(getblock((x,y)))
#     experiment.append(temprow)
# print(np.array(experiment))