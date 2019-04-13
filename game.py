#!bin/python

import sys, pygame, time, numpy

from sprites import *

from engine import *

size = width, height = 1280, 720
black = 0, 0, 0

@Engine.addEntity
class Ball(pygame.sprite.Sprite):
    name = "ball"
    groups = ["base","draw"]
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.image.load("intro_ball.gif")
        self.image = self._image
        self.rect = self.image.get_rect()
        self.pos = numpy.array([0.0,0.0])
        self.speed = numpy.array([200.0, 200.0])
        self.angle = 0

    def update(self,dt,evt,cols):
        self.pos = self.pos + dt*self.speed
        self.rect.center = self.pos
        self.angle += dt * numpy.pi*5
        width, height = Engine.screen.get_rect().size
        area = pygame.Rect(0,0,width,height)
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0]
            self.rect = self.rect.clamp(area)
            self.pos = numpy.array(self.rect.center)
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1]
            self.rect = self.rect.clamp(area)
            self.pos = numpy.array(self.rect.center)
        self.rect.left = 0
        self.rect.top = 0

@Engine.addGroup
class Planets(pygame.sprite.Group):
    name = "planets"

@Engine.addEntity
class Planet(pygame.sprite.Sprite):
    name="planet"
    groups=["planets","draw"]
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.transform.scale(pygame.image.load("intro_ball.gif"),(1024,1024))
        self.image = self._image
        self.rect = self.image.get_rect()
        self.pos = numpy.array(pos)
        self.angle = 0

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


@Engine.addEntity
class Prop(TSprite):
    name="prop"
    groups=["draw"]
    def __init__(self,kargs):
        TSprite.__init__(self,kargs)
        self.image = kargs["image"]
        self.rect = self.image.get_rect(center=kargs["pos"])



Engine.init((width,height))


Engine.new("prop",pos=[600,600],image=pygame.image.load("blackhole1.png"))

Engine.new("player",pos=[300,300])
Engine.run()
