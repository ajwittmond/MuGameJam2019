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
        self._image = pygame.transform.scale(kwargs["image"],(1024,1024))
        self.image = self._image
        self.rect = self.image.get_rect()
        self.pos = numpy.array(kwargs["pos"])
        self.angle = 0
        pxarray = pygame.PixelArray(self.image)
        ymax = 0
        for x in range(0,self.rect.right):
            min = -1
            max = -1
            for y in range(0,self.rect.bottom):
               if(min < 0 and pxarray[x,y]&0x000000FF != 0):
                   min = y
               elif(min >= 0 and  pxarray[x,y]&0x000000FF == 0):
                   max = y
                   break
            if(max > 0):
                ymax = math.max(ymax,max-min)
            else:
                ymax = math.max(ymax,rect.bottom-ymin)
        xmax = 0
        for y in range(0,self.rect.right):
            min = -1
            max = -1
            for x in range(0,self.rect.bottom):
               if(min < 0 and pxarray[x,y]&0x000000FF >= 200):
                   min = x
               elif(min >= 0 and  pxarray[x,y]&0x000000FF >= 200):
                   max = x
                   break
            if(max > 0):
                xmax = math.max(xmax,max-min)
            else:
                xmax = math.max(xmax,rect.bottom-xmin)
        r = math.min(xmax,ymax)
        if "radius" in kwargs:
            s = float(r)/kwargs["radius"]
            self.image = pygame.transform.scale(self.image,np.array(self.rect.size)*s)
            self.rect = self.image.get_rect()
            self.radius = float(kwargs["radius"])
        else:
            self.radius = r




        
