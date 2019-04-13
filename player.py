#!bin/python

import sys, pygame, time

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
            self.acceleration += (planet.pos - self.pos)*self.mass*planet.radius*GRAVITY/dist**2
        self.dilation = np.linalg.norm( self.acceleration ) + 1

    def move(self,dt):
        dilation = self.dilation/Engine.groups["players"].sprites()[0].dilation
        dt = dilation*dt
        self.pos += self.velocity * dt + self.acceleration*0.5*dt*dt
        self.velocity += dt*self.acceleration


@Engine.addEntity
class Player(GravitySprite,AnSprite): 
    name="player"
    groups=["draw","players"]
    animations={"walk":Animation("player-walk.png",5,2,scale=0.25)}
    def __init__(self,kargs):
        kargs["mass"]=100
        GravitySprite.__init__(self,kargs)
        AnSprite.__init__(self,{"animations":self.animations,"current_animation":"walk"})
        self.speed = numpy.array([200.0, 200.0])
        self.velocity = numpy.array([0.0,0.0])
        self.planet = None
        self.theta = 0
        self.angVel = 0

    def update(self,dt,events,collisions):
        HEIGHT = 20
        GRAVITY = 5;
        MAX_SPEED = 200
        ACCELERATION = 500
        JUMP_SPEED = 800
        AnSprite.update(self,dt,events,collisions)
        self.calculateGravity()
        if self.planet == None: #in free space
            self.move(dt)
            if self in collisions:
                for x in collisions[self]:
                    if isinstance(x,Engine.entities["planet"]) and self.velocity.dot(x.pos-self.pos)>0:
                        #clip to planet
                        if(pygame.sprite.collide_mask(x,self)):
                            self.planet = x 
                            x, y = self.pos - x.pos
                            self.theta = np.arctan2(y,x)
        # if self.planet != None: #clipped to planet
        #     for evt in events:
        #         pressed = pygame.key.get_pressed()
        #         angAccel = 0
        #         if pressed[pygame.K_a]:
        #            angAccel = ACCELERATION/self.planet.radius
        #         if pressed[pygame.K_d]:
        #            angAccel = ACCELERATION/self.planet.radius
        #         if pressed[pygame.K_SPACE]:
        #             #unclip from planet
        #             x,y = self.pos - self.planet.pos
        #             direction = np.array([-y,x])
        #             direction /= np.linalg.norm(direction)
        #             self.velocity = self.angVel*self.planet.radius*direction
        #             self.velocity += np.array([x,y])*JUMP_SPEED 
        #             self.planet = None
        #         self.angle += dt*self.angVel + dt*dt*0.5*angAccel
        #         self.angVel += dt*angAccel

