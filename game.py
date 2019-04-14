#!bin/python

import sys, pygame, time, numpy

from sprites import *

from engine import *

import player

import planets

import demon

size = width, height = 1280,720
black = 0, 0, 0

Engine.init((width,height))
#The first entities added here will be rendered under the latter
Engine.new("planet",image=pygame.image.load( "planet1_1.png" ),radius=400.0, pos = [800.0,400.0] )
Engine.new("planet",image=pygame.image.load( "sol07.png" ),radius=400.0, pos = [-800.0,-400.0] )
Engine.new("blackhole",image=pygame.image.load( "non_spinning_blackhole.png" ),radius=600.0, pos = [2800.0,-1400.0] )
Engine.new("planet",image=pygame.image.load( "planet1_1.png" ),radius=400.0, pos = [2800.0,3400.0] )
Engine.new("planet",image=pygame.image.load( "planet2.png" ),radius=100.0, pos = [120.0,100.0])
Engine.new("blackhole",image=pygame.image.load( "blackhole1.png" ), radius = 500.0, pos=[1800.0, 1500.0])
<<<<<<< HEAD
for i in range(0,40):
    x = numpy.random.uniform(-3000,-20)
    y = numpy.random.uniform(0,1900)
    Engine.new("demon",pos=[x,y])

Engine.new("player",pos=[100.0,100.0])

Engine.camera.scale = 1

Engine.run()
