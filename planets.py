#!bin/python
import pygame.pixelarray

import sys, pygame, time, numpy, math

from sprites import *

from engine import *

@Engine.addGroup
class Planets(pygame.sprite.Group):
    name = "planets"

@Engine.addEntity
class Planet(pygame.sprite.Sprite):
    name="planet"
    groups=["planets","draw"]

    def __init__(self,kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = kwargs["image"]
        self.rect = self.image.get_rect()
        self.pos = numpy.array(kwargs["pos"])
        self.angle = 0
        pxarray = pygame.PixelArray(self.image)
        ymax = 0
        for x in range(0,self.rect.right):
            _min = -1
            _max = -1
            for y in range(0,self.rect.bottom):
               if(_min < 0 and pxarray[x,y]&0x000000FF == 255):
                   _min = y
               elif(_min >= 0 and  pxarray[x,y]&0x000000FF != 255):
                   _max = y
                   break
            if(_max > 0):
                ymax = max(ymax,_max-_min)
            else:
                ymax = max(ymax,self.rect.bottom-_min)
        xmax = 0
        for y in range(0,self.rect.bottom):
            _min = -1
            _max = -1
            for x in range(0,self.rect.right):
               if(_min < 0 and pxarray[x,y]&0x000000FF == 255):
                   _min = x
               elif(_min >= 0 and  pxarray[x,y]&0x000000FF != 255):
                   _max = x
                   break
            if(_max > 0):
                xmax = max(xmax,_max-_min)
            else:
                xmax = max(xmax,self.rect.bottom-_min)
        r = min(xmax,ymax)/2
        if "radius" in kwargs:
            s = kwargs["radius"]/float(r)
            a,b = self.rect.size
            self.image = pygame.transform.scale(self.image,(int(a*s),int(b*s)))
            self.rect = self.image.get_rect()
            self.radius = float(kwargs["radius"])
        else:
            self.radius = r
        self.mask = pygame.mask.from_surface(self.image,1)
        px = pygame.PixelArray(self.image)
        
 
