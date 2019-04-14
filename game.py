#!bin/python

import sys, pygame, time, numpy

from sprites import *

from engine import *

import player

import planets

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




Engine.init((width,height))
#The first entities added here will be rendered under the latter
Engine.new("planet",image=pygame.image.load( "planet1_1.png" ),radius=400.0, pos = [800.0,400.0] )
Engine.new("planet",image=pygame.image.load( "planet2.png" ),radius=100.0, pos = [120.0,100.0])
Engine.new("blackhole",image=pygame.image.load( "blackhole1.png" ), radius = 500.0, pos=[1400.0, 1000.0])
#Engine.new("demon",pos=[200,300])
Engine.new("player",pos=[100.0,100.0])


#Engine.new("demon",pos=[300.0,300.0])

Engine.run()
