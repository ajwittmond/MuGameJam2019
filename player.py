#!bin/python

import sys, pygame, time, numpy

from sprites import *

from engine import *
Engine.collision_pairs.append(["players","planets"])
Engine.collision_pairs.append(["players","draw"])

@Engine.addGroup
class Players(pygame.sprite.GroupSingle):
    name="players"


@Engine.addEntity
class Player(AnSprite,TSprite): 
    name="player"
    groups=["draw","players"]
    animations={"walk":Animation("player-walk.png",5,2,scale=0.25)}
    def __init__(self,kargs):
        AnSprite.__init__(self,self.animations)
        self._image = pygame.image.load("intro_ball.gif")
        self.image = self._image
        self.rect = self.image.get_rect()
        self.speed = numpy.array([200.0, 200.0])
        TSprite.__init__(self,kargs)
        self.play("walk")

    def update(self,dt,events,collisions):
        AnSprite.update(self,dt,events,collisions)
        #print(collisions)