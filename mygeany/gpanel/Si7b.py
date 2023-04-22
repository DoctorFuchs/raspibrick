
from gpanel import *

# function f(z) = 1/z
def f(z):
    if z == 0:
        return 0
    return 1 / z

min = -5.0
max = 5.0
step = 1 / 20
reStep = complex(step, 0)
imStep = complex(0, step)

makeGPanel(min, max, min, max)
title("Conformal mapping for f(z) = 1 / z")
line(min, 0, max, 0)  # Real axis
line(0, min, 0, max) # Imaginary axis

# Transform horizontal line per line
setColor("green")
z = complex(min, min)
while z.imag < max:
    z = complex(min, z.imag) # left
    pos(f(z))
    while z.real < max: # move along horz. line
        draw(f(z))
        z = z + reStep
    z = z + imStep

# Transform vertical line per line
setColor("red")
z = complex(min, min)
while z.real < max:
    z = complex(z.real, min) # bottom
    move(f(z))
    while z.imag < max:  # move along vert. line
        draw(f(z))
        z = z + imStep
    z = z + reStep
keep()
