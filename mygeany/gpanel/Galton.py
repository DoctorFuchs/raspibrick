# Galton.py

from gpanel import *
import random

NB_GAMES = 100
NB_BOXES = 9
DELAY_TIME = 100
D = 10
H = 7

def layer(n):
   list = []
   y = 100 - H * n
   for i in range(n):
      pt = [-(n - 1) * D + i * 2 * D, y]
      list.append(pt)
   return list 

def drawLayer(n):
   for i in range(n):
      pt = layer(n)[i]
      move(pt)
      if i < n - 1:
         move(pt[0] + D, pt[1])
         setColor("brown")
         fillCircle(4)

def drawBoard():
   setColor("black")
   line(pA, pC)
   line(pB, pC)
   line(pA, pB)

   for n in range(NB_BOXES + 1):
     drawLayer(n)

   setColor("black")
   lineWidth(2)
   for pt in layer(NB_BOXES):
      move(pt[0], 15)
      rectangle(20, 30)
#      text(pt[0], 10, "0")
   setColor("white")
   line(pA1, pB1)

def play():
   del path[:]
   setColor("red")
   pt = layer(1)[0]
   path.append(pt)
   move(pt)
   index = 0
   for i in range(1, NB_BOXES):
      rand = random.randint(0, 1)
      if rand == 1:
        index += 1
      pt = layer(i + 1)[index]  
      path.append(pt)
      draw(pt)
      delay(DELAY_TIME)
   results[index] += 1
   pt = [-80 + 2 * D * index, 10]
   move(pt)
   setColor("white")
   fillRectangle(15 , 10)   
   setColor("black")
#   text(pt, str(results[index]))
     

def remove():
   setColor("white")
   for i in range(NB_BOXES):
      if i == 0:
         move(path[0])
      else:
         draw(path[i])

makeGPanel(-100, 100, 0, 100)

pA = [-100, 30]
pA1 = [-90, 30]
pB = [100, 30]
pB1 = [90, 30]
pC = [0, 100]

drawBoard()

path = []
results = [0] * NB_BOXES

n = 0
while n < NB_GAMES:
   n += 1
   title("Game #: " + str(n))
   play()
   delay(2 * DELAY_TIME)
   remove()

setColor("green")
for n in range(NB_BOXES):
   y = results[n] / NB_GAMES * 100
   if n == 0:
      move(-80 + 2 * D * n, y)
   else:
      draw(-80 + 2 * D * n, y)
   
keep()
