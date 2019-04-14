#!bin/python

#This is a class that represents the top level objects of a simple game engine

import pygame, time, sys
import pygame.gfxdraw
from pygame.math import Vector2
import numpy as np

class Camera:
    def __init__(self, center=0, scale=1,angle = 0):
        self.center = np.array(center)
        self.scale = scale
        self.angle = angle

class Engine:
    entities = {}
    groups = {}
    #what groups to check collision against
    collision_pairs = []
    running = True
    screen = None
    camera = Camera(np.array([0.0,0.0]),1.0)

    def init(self,size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.camera.center=np.array(size)/2

    def run(self):
        t = time.process_time()
        while Engine.running:
            #calculate time delta
            t_prime = time.process_time() 
            dt = t_prime - t
            t = t_prime
            #pump events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: sys.exit()

            collisions = {}


            #check for collision
            #this could possibly be accelerated by using
            #some form of spacial partitioning 
            for (left,right) in self.collision_pairs:
                l = self.groups[left]
                r = self.groups[right]
                for s1 in l.sprites():
                    for s2 in r.sprites():
                        s1.rect.center = s1.pos
                        s2.rect.center = s2.pos
                        if pygame.sprite.collide_rect(s1,s2):
                            if not s1 in collisions:
                                collisions[s1] = set()
                            if not s2 in collisions:
                                collisions[s2] = set()
                            collisions[s1].add(s2)
                            collisions[s2].add(s1)
            

            #update sprites
            for _,g in self.groups.items():
                g.update(dt,events,collisions)

            self.groups["draw"].draw()

            pygame.display.flip()

    def addGroup(self,cls):
        self.groups[cls.name]  = cls()


    def addEntity(self,cls):
        self.entities[cls.name] = cls

    def new(self,name, **vargs):
        if name in self.entities:
            cls = self.entities[name]
            entity = cls(vargs)
            for name, group in self.groups.items():
                if name in getattr(cls,"groups"):
                    group.add(entity)
        else:
            raise Exception("no such Entity: "+name)


Engine = Engine()

#group for sprites to be draw to the screen
#draws sprites in order of layer, testing for visibility and
#applying a transformation based on the camera 
@Engine.addGroup
class DrawGroup(pygame.sprite.LayeredUpdates):
    name = "draw"

    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)

    def draw(self):
        Engine.screen.fill((0,0,0))

        camera = Engine.camera

        view_center = np.array( Engine.screen.get_rect().size )/2

        offset = camera.center - view_center

        buffer = None
        if camera.scale == 1:
            buffer = Engine.screen
        else:
            buffer = pygame.Surface(visible_area.size,Engine.screen.getFlags,Engine.screen)
        blits = []
        for layer in self.layers():
            for sprite in self.get_sprites_from_layer(layer):
                p_orig = sprite.pos
                x,y = sprite.pos-offset-view_center
                p = Vector2(x,y)
                p = p.rotate(-camera.angle)
                image = sprite.image
                if not hasattr(sprite,"angle"):
                    sprite.angle = 0
                if sprite.angle-camera.angle != 0:
                    image = pygame.transform.rotate(image,sprite.angle-camera.angle)
                if hasattr(sprite,"scale") and sprite.scale != 0:
                    r = image.get_rect()
                    image = pygame.transform.scale(image,np.array(r.size)*sprite.scale)
                rect = image.get_rect()
                rect.center = [p.x,p.y] + view_center
                blits.append((image,rect))
        # for _ ,r in blits:
        #     pygame.gfxdraw.rectangle(buffer,r,(255,255,255,255))
        buffer.blits(blits)
        if camera.scale != 1:
            scaled = pygame.transform.smoothscale(buffer,Engine.screen.getRect().size,Engine.screen)

@Engine.addGroup
class BaseGroup(pygame.sprite.Group):
    name = "base"
