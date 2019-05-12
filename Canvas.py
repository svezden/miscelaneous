import pygame,sys,random, math
import matplotlib.pyplot as plt
from pygame.locals import *
import PhysEngine2D as phys

#Colors (R, G, B)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
array_colors = [red,green,blue]

def random_color():
    return pygame.Color((random.randint(0,255),random.randint(0,255),random.randint(0,255)))

#Initialization of the window
pygame.init()
window = pygame.display.set_mode((1000,600))
window.fill(white)
pygame.display.set_caption("Universe")
env = phys.environment((1000,600))
env.is_acceleration_on = True
p1 = phys.Circle((100,500),20,red)
p1.vel = [0,0]
p2 = phys.Circle((500,250),50,blue)
p2.vel = [-1,0]
p3 = phys.Rectangle((400,100),(30,40),black)
p3.vel = [0,-1]
p3.mass = 10
env.circles = [p1,p2]
env.rectangles = [p3]


#Main Loop        
paused = False
total_e = []
total_kin = []
total_pot = []
time_series = []
time = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = (True, False)[paused]
                if paused:
                    print 'The simulation is Paused. To resume press the spacebar'
                else:
                    print 'The simulation is Resumed'
        elif event.type == pygame.MOUSEBUTTONUP: # Adding a particle using the mouse
            pos = pygame.mouse.get_pos()
            random_color = pygame.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            p = phys.Circle(pos, 15,random_color) 
            env.particles.append(p)

    if not paused:
        time += 1
        env.update(time)
        window.fill(white)
        pygame.draw.rect(window, env.colour, [0, 0, 1000, 600],env.thickness)
        kin = 0
        pot = 0
        for p in env.circles:
            pygame.draw.circle(window, p.colour, (int(p.x), int(p.y)), p.radius)
            kin += 0.5*p.mass*(p.vel[0]**2+p.vel[1]**2)
            pot += p.mass*env.acceleration[1]*(env.height-p.y)
        for p in env.rectangles:
            X = int(p.x)
            Y = int(p.y)
            DX = int(p.width/2)
            DY = int(p.height/2)
            pygame.draw.polygon(window, p.colour, [[X+DX, Y+DY],[X+DX,Y-DY],[X-DX,Y-DY],[X-DX,Y+DY]], 0)
##            kin += 0.5*p.mass*(p.vel[0]**2+p.vel[1]**2)
##            pot += p.mass*env.acceleration[1]*(env.height-p.y)
        time_series.append(time)
        total_e.append(kin+pot)
        total_kin.append(kin)
        total_pot.append(pot)
    elif paused:
        plt.plot(time_series,total_e)
        plt.plot(time_series,total_kin)
        plt.plot(time_series,total_pot)
        plt.show()
        
 
    pygame.display.flip()    

