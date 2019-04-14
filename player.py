#!bin/python

import sys, pygame, time, math, random

import numpy as np

from sprites import *

from engine import *

from planets import *

Engine.collision_pairs.append(["players","planets"])
Engine.collision_pairs.append(["players","draw"])

@Engine.addGroup
class Players(pygame.sprite.GroupSingle):
    name="players"


class GravitySprite(TSprite):
    name="gravitySprite"
    def __init__(self,kargs):
        TSprite.__init__(self,kargs)
        self.velocity = numpy.array([200.0, 200.0])
        self.mass = kargs["mass"]
        self.dilation = 1

    def calculateGravity(self):
        GRAVITY = 1.0;
        DILATION = 1.0/100.0;
        self.acceleration = np.array([0.0,0.0])
        for planet in Engine.groups["planets"].sprites():
            dist = np.linalg.norm(planet.pos - self.pos)
            mult = 1
            if isinstance(planet,BlackHole):
                mult = 2
            self.acceleration += (planet.pos - self.pos)*self.mass*mult*planet.radius*GRAVITY/dist**2
        self.dilation = np.linalg.norm( self.acceleration ) + 1
        if(len(Engine.groups["players"].sprites())>0):
            self.dilation = self.dilation/Engine.groups["players"].sprites()[0].dilation
        

    def move(self,dt):
        dt = dt/self.dilation
        self.pos += self.velocity * dt + self.acceleration*0.5*dt*dt
        self.velocity += dt*self.acceleration
        return dt

#simple particle
@Engine.addEntity
class Particle(GravitySprite,AnSprite):
    name = "particle"
    groups = [ "draw" ]
    def __init__(self,kargs):
        self.fps = kargs.get("fps",10)
        kargs["animations"] = {"idle":Animation(kargs["image"],
                                                4,4,fps=self.fps,
                                                scale=kargs.get("scale",1))}
        kargs["current_animation"] = "idle"
        GravitySprite.__init__(self,kargs)
        AnSprite.__init__(self,kargs)
        self.velocity = kargs.get("velocity",np.array([0.0,0.0]))
        self.play("idle")
        self.t = 0
        self.layer = kargs.get("layer",0)

    def update(self,dt,evts,cols):
        self.calculateGravity()
        dt = self.move(dt)
        AnSprite.update(self,dt,evts,cols)
        self.t += dt
        if(self.t>=(1/self.fps)*len(self.animations["idle"])):
            self.kill()


blood = pygame.image.load("blood_hit.png")

@Engine.addEntity
class Player(GravitySprite,AnSprite): 
    name="player"
    groups=["draw","players"]
    animations={"walk_-1":Animation(pygame.image.load( "player-walk_-1.png" ),5,2,scale=0.25),
                "walk_1":Animation(pygame.image.load( "player-walk_1.png" ),5,2,scale=0.25)}
    def __init__(self,kargs):
        kargs["mass"]=100
        GravitySprite.__init__(self,kargs)
        AnSprite.__init__(self,{"animations":self.animations,"current_animation":"walk_-1"})
        self.speed = numpy.array([200.0, 200.0])
        self.velocity = numpy.array([0.0,0.0])
        self.planet = None
        self.theta = 0
        self.angVel = 0
        self._angle = 0
        self._flip = 0
        self.alive = True

    def update(self,dt,events,collisions):
        HEIGHT = 0
        GRAVITY = 5
        MAX_SPEED = 100
        ACCELERATION = 500
        JUMP_SPEED = 50
        #TODO:get animation to flip.
        self.calculateGravity()
        #check if getting pulled off of planet
        if self.planet != None:
            d = self.pos - self.planet.pos
            x,y = d
            direction = np.array([-y,x])
            if(d.dot(self.acceleration)>0):
                self.velocity = direction*self.angVel*self.planet.radius/np.linalg.norm(d)
                self.planet = None
        if self.planet == None: #in free space
            self.move(dt)
            dx,dy = self.acceleration
            ang = np.arctan2(dy,dx)
            ang = 360 * (-ang+np.pi/2)/(2*np.pi)
            self._angle = ang 
            if self in collisions:
                for x in collisions[self]:
                    if isinstance(x,Engine.entities["blackhole"]) and pygame.sprite.collide_mask(x,self):
                        self.alive = False
                    elif (isinstance(x,Engine.entities["planet"]) and
                          self.velocity.dot(x.pos-self.pos)>=0):
                        #clip to planet
                        if(pygame.sprite.collide_mask(x,self)):
                            self.planet = x 
                            _x, y = self.pos - x.pos
                            self.theta = np.arctan2(y,_x)
                    
        if self.planet != None: #clipped to planet
            pressed = pygame.key.get_pressed()
            angAccel = 0
            x,y = self.pos - self.planet.pos
            direction = np.array([-y,x])
            angAccel = ACCELERATION/self.planet.radius
            if pressed[pygame.K_a]:
                angAccel = math.copysign(angAccel,direction.dot([-1,0])) 
            elif pressed[pygame.K_d]:
                angAccel = math.copysign(angAccel,direction.dot([1,0])) 
            elif pressed[pygame.K_w]:
                angAccel = math.copysign(angAccel,direction.dot([0,-1])) 
            elif pressed[pygame.K_s]:
                angAccel = math.copysign(angAccel,direction.dot([0,1])) 
            else:
                angAccel = -self.angVel*2
            self.theta += dt*self.angVel + dt*dt*0.5*angAccel
            self.angVel += dt*angAccel
            if abs( self.angVel ) < 0.00001:
                self.angVel = 0
            if abs(self.angVel)*self.planet.radius>MAX_SPEED:
                self.angVel = MAX_SPEED*(abs(self.angVel))/(self.planet.radius*self.angVel)
            self._angle = 360 * -(self.theta + np.pi/2)/(2*np.pi)
            self.pos = self.planet.pos.copy()
            self.pos += np.array([np.cos(self.theta),np.sin(self.theta)])*(self.planet.radius+HEIGHT)
            self._flip = self.angVel < 0
            if pressed[pygame.K_SPACE]:
                #unclip from planet
                d = self.pos - self.planet.pos
                x,y = d
                direction = np.array([-y,x])
                n = np.linalg.norm(direction)
                direction /= n
                self.velocity = self.angVel*self.planet.radius*direction
                self.velocity += numpy.array([x,y])*JUMP_SPEED/n
                self.planet = None
        AnSprite.update(self, dt, events, collisions)
        self.image = pygame.transform.rotate(pygame.transform.flip(self.image,self._flip,False),
                                            self._angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
        if not self.alive:
            #bleed
            for _ in range(0,10):
                d = np.random.random(2)*100 - [50,50]
                p = self.pos + d
                vel = d * random.random()*20/np.linalg.norm(d)
                Engine.new("particle",mass = 2,fps=10,image=blood,
                                      scale=0.5,velocity=vel,layer=2,
                                      pos=self.pos)
            #die
            self.kill()


