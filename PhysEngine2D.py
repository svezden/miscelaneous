import math, random
import numpy as np

'''This module creates a 2D physics engine. For the moment I will add just circles. Triangles
and rectangles as possible figures will be added later'''

def dot_prod((x1,y1),(x2,y2)):
    return (x1*x2+y1*y2)

def elastic_col(p1,p2):
    '''Test if two particles collide. First for circles'''
    total_mass = p1.mass + p2.mass
    distance_centers = math.sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)
    center_vec = ((p1.x-p2.x)/distance_centers,(p1.y-p2.y)/distance_centers)
    center_vec_perp = (center_vec[1],-center_vec[0])

    if distance_centers <= p1.radius+p2.radius:  #This prevents particles being in the same place
	p1.x -= 0.5*(distance_centers - (p1.radius+p2.radius))*center_vec[0]
	p1.y -= 0.5*(distance_centers - (p1.radius+p2.radius))*center_vec[1]
	p2.x += 0.5*(distance_centers - (p1.radius+p2.radius))*center_vec[0]
	p2.y += 0.5*(distance_centers - (p1.radius+p2.radius))*center_vec[1]
 	PX = ((p1.mass-p2.mass)*dot_prod(center_vec,p1.vel) + 2*p2.mass*dot_prod(center_vec,p2.vel))/total_mass*np.asarray(center_vec)+dot_prod(center_vec_perp,p1.vel) *np.asarray(center_vec_perp)
        PY = ((p2.mass-p1.mass)*dot_prod(center_vec,p2.vel) + 2*p1.mass*dot_prod(center_vec,p1.vel))/total_mass*np.asarray(center_vec)+dot_prod(center_vec_perp,p2.vel) *np.asarray(center_vec_perp)
	p1.vel = PX
	p2.vel = PY

class Particle:
    '''A particle with mass, velocity and size'''
    def __init__(self,(x,y),colour,mass=1):
        self.x = x
        self.y = y
        self.colour = colour
        self.vel = [0,0]
        self.drag = 0.9
        self.mass = mass

    def move(self,accel,t):
        '''This function determines the movement of the circle based on kinematics. This form is to prevent a fluctuation in the energy, Drag slows the particles'''
        if t%2:
            self.vel[0] += self.drag*accel[0]
            self.vel[1] += self.drag*accel[1]
            self.x += self.vel[0]
            self.y += self.vel[1]
        if not t%2:
            self.x += self.vel[0]
            self.y += self.vel[1]
            self.vel[0] += self.drag*accel[0]
            self.vel[1] += self.drag*accel[1]
        

class Circle(Particle):
    def __init__(self,(x,y),radius,colour,mass=1):
        Particle.__init__(self,(x,y),colour,mass)
        self.radius = radius
    def bounce(self,env):
    	if self.x - self.radius < 0:
            self.vel[0] = - self.vel[0]
	elif self.x + self.radius > env.width:
	    self.vel[0] = - self.vel[0]
        elif self.y - self.radius < 0:
	    self.vel[1] = - self.vel[1]
	elif self.y + self.radius >= env.height:
            self.vel[1] = - self.vel[1]

class Rectangle(Particle):
    '''The vertices of the rectangle are labeled clockwise'''
    def __init__(self,(x,y),(height,width),colour,mass=1):
        Particle.__init__(self,(x,y),colour,mass)
        self.height = height
        self.width = width
        self.x_axis = [width/2,0]
        self.y_axis = [0,height/2]
    def rotate(self,torque):
        self.x_axis += torque*[height/2,0]
        self.y_axis += torque*[0,-width/2]
    def bounce(self,env):
    	if self.x - self.height/2 < 0:
            self.vel[0] = - self.vel[0]
	elif self.x + self.height/2 > env.width:
	    self.vel[0] = - self.vel[0]
        elif self.y - self.width/2 < 0:
	    self.vel[1] = - self.vel[1]
	elif self.y + self.width/2 >= env.height:
            self.vel[1] = - self.vel[1]
        
     

class environment:
    """  Moves particles and tests for collisions with the walls and each other """
    def __init__(self,(width,height),thickness=10):
        self.width = width
        self.height = height
        self.thickness = thickness
        self.circles = []
        self.rectangles = []
        self.particles = [self.circles,self.rectangles]
        self.colour = (0,255,255)
        self.mass_of_air = 0.2
        self.elasticity = 0.75
	self.is_acceleration_on = True
	self.acceleration = [0,.01]
        self.angle_acc = 0


    def update(self,t):
        for i, particle in enumerate(self.circles):
            particle.bounce(self)
            particle.move(self.acceleration,t)
            for particle2 in self.circles[i+1:]:
                elastic_col(particle, particle2)
        for i, particle in enumerate(self.rectangles):
            particle.bounce(self)
            particle.move(self.acceleration,t)
            for particle2 in self.circles[i+1:]:
                elastic_col(particle, particle2)
        

    

