#!bin/python

#This is a class that represents the top level objects of a simple game engine

import pygame, time
import numpy as np

class Camera:
    def __init__(self, center, scale):
        self.center = center
        self.scale = scale



class Engine:
    entities = {}
    groups = {}
    #what groups to check collision against
    collisionPairs = []
    running = True
    screen = None
    camera = Camera(np.array([0.0,0.0]),1.0)

    def init(self,size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

    def run(self):
        t = time.process_time()
        while Engine.running:
            #calculate time delta
            t_prime = time.process_time() 
            dt = t - t_prime
            t = t_prime
            #pump events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: sys.exit()

            collisions = {}

            #check for collision
            #this could possibly be accelerated by using
            #some form of spacial partitioning 
            for (left,right) in self.collisionPairs:
                l = self.groups[left]
                r = self.groups[right]
                for s1 in l.sprites():
                    for s2 in r.sprites():
                        if pygame.sprite.collide_rect(s1,s2):
                            if not s1 in collisions:
                                collisions[s1] = []
                            if not s2 in collisions:
                                collisions[s2] = []
                            collisions[s1].append(s2)
                            collisions[s2].append(s1)


            #update sprites
            for _,g in self.groups.items():
                g.update(dt,events,collisions)

            self.groups["draw"].draw()

            pygame.display.flip()

    def addGroup(self,cls):
        self.groups[cls.name]  = cls()


    def addEntity(self,cls):
        self.entities[cls.name] = cls

    def new(self,name, **kwargs):
        if name in self.entities:
            cls = self.entities[name]
            entity = cls()
            for name, group in self.groups.items():
                if name in getattr(cls,"groups"):
                    group.add(entity)
        else:
            raise Exception("no such Entity: "+name)

    #returns rect representing the visible screen space
    @property
    def visibleArea(self):
        w,h = self.screen.get_rect().size
        area = pygame.Rect(0,0,0,0)
        camera = self.camera
        area.center = camera.center
        area.size = (w*camera.scale,h*camera.scale)
        return area

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
        visible_area = Engine.visibleArea
        scale = Engine.camera.scale
        Engine.screen.fill((0,0,0))
        buffer = None
        if scale == 1:
            buffer = Engine.screen
        else:
            buffer = pygame.Surface(visible_area.size,Engine.screen.getFlags,Engine.screen)
        blits = []
        for layer in self.layers():
            for sprite in self.get_sprites_from_layer(layer):
                rect_prime = sprite.rect.copy()
                rect_prime.center -= Engine.camera.center
                blits.append((sprite.image,rect_prime))
        buffer.blits(blits)
        if scale != 1:
            scaled = pygame.transform.smoothscale(buffer,Engine.screen.getRect().size,Engine.screen)

@Engine.addGroup
class BaseGroup(pygame.sprite.Group):
    name = "base"
