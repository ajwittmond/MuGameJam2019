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

@Engine.addEntity
class Demon(GravitySprite,AnSprite):
    name="demon"
    groups=["draw","demons"]
    i_w,i_h =  np.array( pygame.image.load("demon_idle.png").get_rect().size )*0.3
    d_w, d_h = np.array(pygame.image.load("demon_death.png").get_rect().size)*0.3
    animations={"idle":Animation(pygame.transform.scale(pygame.image.load("demon_idle.png"),(int(i_w),int(i_h))),8,1,scale=1),
                "death":Animation(pygame.transform.scale(pygame.image.load("demon_death.png"),(int(d_w),int(d_h))),5,1,scale=0.3)}
    def __init__(self,kargs):
        kargs["mass"]=500
        GravitySprite.__init__(self,kargs)
        AnSprite.__init__(self,{"animations":self.animations,"current_animation":"idle"})
        self.speed = numpy.array([300.0, 300.0])
        self.velocity = numpy.array([0.0,0.0])
        self.theta = 0
        self.angVel = 0
        self.alive = True

    def update(self,dt,events,collisions):
        HEIGHT = 1
        GRAVITY = 5
        MAX_SPEED = 100
        ACCELERATION = 500
        AnSprite.update(self,dt,events,collisions)
        self.calculateGravity()
        #seek player
        mult=5
        if(len(Engine.groups["players"].sprites())>0):
            self.acceleration +=(Engine.groups["players"].sprites()[0].pos - self.pos)*mult*self.speed
        dx,dy = self.acceleration
        ang = np.arctan2(dy,dx)
        ang = 360 * (-ang+np.pi/2)/(2*np.pi)
        self.angle = ang - 90
        self.move(dt)
        #kill player on contact
        if self in collisions:
            for x in collisions[self]:
                    if isinstance(x, Engine.entities["player"]) and pygame.sprite.collide_mask(x, self):
                        x.alive = False
                    if isinstance(x,Engine.entities["bullet"]) and pygame.sprite.collide_mask(x,self):
                        self.alive = False
        if not self.alive:
            #pentagram
            d_w, d_h = np.array(pygame.image.load("demon_death.png").get_rect().size) * 0.3
            death = pygame.transform.scale(pygame.image.load("demon_death.png"), (int(d_w), int(d_h)))
            Engine.new("particle", image = death,xtile = 5,ytile = 1, mass = 100, fps = 10,pos = self.pos)
            self.kill()


