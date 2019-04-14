#!bin/python

import sys, pygame, time

import numpy as np

from sprites import *

from engine import *

from player import *

Engine.collision_pairs.append(["demons","players"])
Engine.collision_pairs.append(["demons","draw"])

@Engine.addGroup
class Demons(pygame.sprite.Group):
    name="demons"


class GravityDemon(TSprite):
    name="gravityDemon"
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
        dilation = self.dilation/Engine.groups["demons"].sprites()[0].dilation
        dt = dilation*dt
        self.pos += self.velocity * dt + self.acceleration*0.5*dt*dt
        self.velocity += dt*self.acceleration


@Engine.addEntity
class Demon(GravityDemon,AnSprite): 
    name="demon"
    groups=["draw","demons"]
    animations={"idle":Animation("demon_idle.png",5,2,scale=0.25)}
    def __init__(self,kargs):
        kargs["mass"]=50
        GravityDemon.__init__(self,kargs)
        AnSprite.__init__(self,{"animations":self.animations,"current_animation":"idle"})
        self.speed = numpy.array([200.0, 200.0])
        self.velocity = numpy.array([0.0,0.0])
        self.theta = 0
        self.angVel = 0

    def update(self,dt,events,collisions):
        HEIGHT = 1
        GRAVITY = 5
        MAX_SPEED = 100
        ACCELERATION = 500
        AnSprite.update(self,dt,events,collisions)
        self.calculateGravity()
        self.move(dt)
        if self in collisions:
            for x in collisions[self]:
                    if isinstance(x,Engine.entities["player"]):
                        Engine.end()
