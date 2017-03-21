from gamegrid import *

def onReset(): 
    for x in range(s):
        for y in range(s):
            a[x][y] = 0  # All cells dead
    for n in range(z):
        loc = getRandomEmptyLocation()
        a[loc.x][loc.y] = 1
    showPopulation()
        
def showPopulation():
    for x in range(s):
        for y in range(s):
            loc = Location(x, y)
            if a[x][y] == 1:
                getBg().fillCell(loc, Color.green, False)
            else:
                getBg().fillCell(loc, Color.black, False)
    refresh()
    
def getNumberOfNeighbours(x, y):
    nb = 0
    for i in range(max(0, x - 1), min(s, x + 2)):
        for k in range(max(0, y - 1), min(s, y + 2)):
            if not (i == x and k == y): 
                if a[i][k] == 1:
                    nb = nb + 1
    return nb

def onAct():
    global a
    # Don't use the current, but a new population
    b  = [[0 for x in range(s)] for y in range(s)]
    for x in range(s):
        for y in range(s):
            nb = getNumberOfNeighbours(x, y)
            if a[x][y] == 1:  # living cell
                if nb < 2:
                    b[x][y] = 0
                elif nb > 3:
                    b[x][y] = 0
                else:
                    b[x][y] = 1
            else:             # dead cell
                if nb == 3:
                    b[x][y] = 1
                else:
                    b[x][y] = 0
    a = b # Use new population as current
    showPopulation()
    
# =================== global section ==================
s = 50   # Number of cells in each direction
z = 1000 # Size of population at start
a  = [[0 for x in range(s)] for y in range(s)]
makeGameGrid(s, s, 800 // s, Color.red)
registerAct(onAct)
registerNavigation(resetted = onReset)
setTitle("Conway's Game Of Life")
onReset()
show()

