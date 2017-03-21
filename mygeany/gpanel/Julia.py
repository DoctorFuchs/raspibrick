# Julia.py

from gpanel import *

def putPixel(z, c):
  setColor(c);
  point(z.real, z.imag)


maxIterations = 100
maxNorm = 50.0
step = 0.005
range = 2.0
makeGPanel(-range, range, -range, range)
enableRepaint(False)

c = complex(-0.5, -0.5)
z0 = complex(-range, -range)
while z0.imag < range: # outer loop in imag direction
   z0 = complex(-range, z0.imag + step)
   while z0.real < range: # inner loop in real direction
      z0 = z0 + step
      # Julia iteration
      z = z0;
      it = 0
      while (z.real * z.real + z.imag * z.imag) < maxNorm and it < maxIterations:
         z = z * z + c
         it = it + 1
      if it < 3:
         putPixel(z0, "gray")
      elif it < 5:
         putPixel(z0, "orange")
      elif it < 8:
         putPixel(z0, "red")
      elif it < 12:
         putPixel(z0, "blue")
      elif it < 100:
          putPixel(z0, "yellow")
      else:
         putPixel(z0, "black")
   repaint()
keep()

