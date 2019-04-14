#!bin/python

import sys, pygame, time, numpy

from sprites import *

from engine import *

import player

import planets

import demon

size = width, height = 1280, 720
black = 0, 0, 0

Engine.init((width,height))
#The first entities added here will be rendered under the latter
Engine.new("planet",image=pygame.image.load( "planet1_1.png" ),radius=400.0, pos = [800.0,400.0] )
Engine.new("planet",image=pygame.image.load( "planet2.png" ),radius=100.0, pos = [120.0,100.0])
Engine.new("blackhole",image=pygame.image.load( "blackhole1.png" ), radius = 500.0, pos=[1400.0, 1000.0])
for i in range(0,100):
    x = numpy.random.uniform(-400,-20)
    y = numpy.random.uniform(0,200)
    Engine.new("demon",pos=[x,y])
Engine.new("player",pos=[100.0,100.0])


#Engine.new("demon",pos=[300.0,300.0])

Engine.run()
