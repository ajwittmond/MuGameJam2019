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


Engine.collision_pairs.append(("demons","planets"))
@Engine.addEntity
class Demon(GravitySprite,AnSprite):
    name="demon"
    groups=["draw","demons"]
    i_w,i_h =  np.array( pygame.image.load("demon_idle.png").get_rect().size )*0.3
    d_w, d_h = np.array(pygame.image.load("demon_death.png").get_rect().size)*0.3
    animations={"idle":Animation(pygame.transform.scale(pygame.image.load("demon_idle.png"),(int(i_w),int(i_h))),8,1,scale=1),
                "death":Animation(pygame.transform.scale(pygame.image.load("demon_death.png"),(int(d_w),int(d_h))),5,1,scale=0.3)}
    def __init__(self,kargs):
        kargs["mass"]=50
        GravitySprite.__init__(self,kargs)
        AnSprite.__init__(self,{"animations":self.animations,"current_animation":"idle"})
        self.speed = numpy.array([1.0, 1.0])
        self.velocity = numpy.array([0.0,0.0])
        self.theta = 0
        self.angVel = 0
        self.alive = True
        self.restitution=0.5

    def update(self,dt,events,collisions):
        HEIGHT = 1
        GRAVITY = 5
        max_speed = 250
        ACCELERATION = 10
        AnSprite.update(self,dt,events,collisions)
        self.calculateGravity()
        #seek player
        mult=0.1
        if(len(Engine.groups["players"].sprites())>0):
            self.acceleration +=(Engine.groups["players"].sprites()[0].pos - self.pos)*mult*self.speed
        dx,dy = self.acceleration
        ang = np.arctan2(dy,dx)
        ang = 360 * (-ang+np.pi/2)/(2*np.pi)
        self.angle = ang - 90
        #max speed
        if(np.linalg.norm(self.velocity) > max_speed):
            self.velocity = self.velocity/np.linalg.norm(self.velocity)*max_speed
        #kill player on contact
        if self in collisions:
            for x in collisions[self]:
                    if isinstance(x, Engine.entities["player"]) and pygame.sprite.collide_mask(x, self):
                        x.alive = False
                    if isinstance(x,Engine.entities["bullet"]) and pygame.sprite.collide_mask(x,self):
                        self.alive = False
                    if isinstance(x,Planet):
                        if isinstance(x,BlackHole):
                            self.alive = False
                        elif((x.pos-self.pos).dot(self.velocity)>0): 
                            p = pygame.sprite.collide_mask(self,x)
                            if p:
                                #bounce off
                                d = x.pos - self.pos
                                d /= np.linalg.norm(d)
                                r = self.velocity.dot(d)*(-1-self.restitution)
                                self.velocity +=d*r
        speed= np.linalg.norm( self.velocity )
        if speed> max_speed:
            self.velocity *= max_speed/speed
        self.move(dt)
        if not self.alive:
            #pentagram
            d_w, d_h = np.array(pygame.image.load("demon_death.png").get_rect().size) * 0.1
            death = pygame.transform.scale(pygame.image.load("demon_death.png"), (int(d_w), int(d_h)))
            Engine.new("particle", image = death,xtile = 5,ytile = 1, mass = 10, fps = 10,pos = self.pos)
            self.kill()



@Engine.addEntity
class DemonSpawner(pygame.sprite.Sprite):
    name="spawner"
    groups = ["base"]
    num_demons = 5
    t = 0
    t2 = 0
    def update(self,dt,events,col):
        self.t2 += dt
        if ( self.t2>=5):
            self.t2 = 0
            for i in range(0, 10):
                if (len(Engine.groups["players"].sprites()) > 0):
                    x, y = Engine.groups["players"].sprites()[0].pos
                    r = numpy.random.uniform(1300,3000)
                    theta = numpy.random.uniform(90,200)
                    x += r*numpy.cos(theta)
                    y += r*numpy.sin(theta)
                    Engine.new("demon", pos=[x, y])
        self.t += dt


