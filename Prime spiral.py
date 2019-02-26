#This program draws an Ulam spiral. The Ulan spiral is created by putting
#numbers in an spiral, starting from 1 and going outwards counterclockwise.
# The first numbers are
#                             5 4 3
#                             6 1 2
#                             7 8 9 ...
#In this spiral the prime numbers are highlighted, creating interesting patterns

#I attack this problem by building layers. Note that each complete square in
#the spiral with 1 in its center has area (2N+1)^2. The perimeter is then 
#(2N+1)^2-(2N-1)^2= 8N. The angle where each number along the perimeter is
#located increases in each level by \pi/(4N),
#The last step is to note that if we use L^1 metric, everithing simplifies.

import pygame
import math,sys
from pygame.locals import *

# Definition of colors
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)

pi = 3.1415

#Initialization of the window
pygame.init()
window = pygame.display.set_mode((1200,800))
window.fill(white)
pygame.display.set_caption("Primes Spiral")

#Maximum number
N_max = 3000

perimeters = [1]
total_numbers = 1
i = 1
level = 1

# routine that computes the prime factors of n
def prime_factors(n):
    i = 2
    factors, b = [],{}
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    for item in factors:
        b[item] = b.get(item, 0) + 1
    return factors

# routine to compute the number of levels and creates an array with the value
# of the perimeters
while i < math.sqrt(N_max)-1:
    perimeters.append(8*i)
    i += 1

print(perimeters)

#This subroutine draws the spiral
X0,Y0 = 600,400 # coordinates of the center of the canvas
delta = 0
counter =1
for level in perimeters:
    for number in range(0,perimeters[delta]):
        # This X and Y is the usual euclidean norm coordinates
        X =  math.cos(-2*number*pi/perimeters[delta])
        Y =  math.sin(-2*number*pi/perimeters[delta])
        # Here R, x, y are coordinates in L^1 metric, rotated by pi/4 to have the
        # usual look 
        R = level/(abs(X)+abs(Y))
        x = R*(X*math.cos(pi/4)+Y*math.sin(pi/4))
        y = R*(-X*math.sin(pi/4)+Y*math.cos(pi/4))
        if len(prime_factors(counter)) == 1:
            pygame.draw.rect(window,red,(X0+x,Y0+y,5,5),0)
            print(counter)
        # else:
        #    pygame.draw.rect(window,blue,(X0+x,Y0+y,5,5),0)
        
        #pygame.display.update()
        #pygame.time.delay(1)
        counter += 1
    delta += 1

#Main Loop        
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.MOUSEBUTTONUP:
          window.fill(white)
        
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

        pygame.display.update()  
