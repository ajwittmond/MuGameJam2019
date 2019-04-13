#!bin/python

import sys, pygame, time, numpy

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
        self.speed = numpy.array([100.0, 100.0])
        self.angle = 0
    def update(self,dt,evt,cols):
        self.pos = self.pos + dt*self.speed
        self.rect.center = self.pos
        self.angle += dt * numpy.pi*5
        self.image = pygame.transform.rotate(self._image,self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.left < Engine.visibleArea.left or self.rect.right > Engine.visibleArea.width:
            self.speed[0] = -self.speed[0]
            self.rect = self.rect.clamp(Engine.visibleArea)
            self.pos = numpy.array(self.rect.center)
        if self.rect.top < Engine.visibleArea.top or self.rect.bottom > Engine.visibleArea.height:
            self.speed[1] = -self.speed[1]
            self.rect = self.rect.clamp(Engine.visibleArea)
            self.pos = numpy.array(self.rect.center)
        self.rect.left = 0
        self.rect.top = 0 

Engine.init((width,height))

Engine.new("ball")


Engine.run()
