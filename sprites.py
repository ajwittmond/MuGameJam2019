

import os
import numpy as np
from pygame.sprite import Sprite
import pygame

class Animation:
    def __init__(self, path,xtile,ytile,  fps=20):
        self.frames = []
        self.sheet = pygame.image.load(path)
        w ,h = np.array(self.sheet.get_rect().size)/[xtile,ytile]
        for y in range(0,ytile):
            for x in range(0,xtile):
                self.frames.append ( self.sheet.subsurface(pygame.Rect(x*w,y*h,w,h)) )
        self.fps = fps
        self.playing = True
        self.t = 0
        self.playtime = -1
        self.rate = 1
        self.frame = 0
        self._frame_len = len(self.frames)

    def __len__():
        return self._frame_len

    def update(self,dt,sprite):
        if self.playing:
            self.t += dt*self.rate
            self.frame = int ( self.t*self.fps )
            self.frame %= self._frame_len
            sprite.image = self.frames[self.frame]
            sprite.rect = sprite.image.get_rect(center = sprite.rect.center)
            if self.playtime > 0 and self.playtime <= self.t :
                self.playing = False

    def play(self,reset=True):
        self.playing = True
        if reset:
            self.t = 0

    def pause(self):
        self.playing = False

    def stop(self):
        self.playing = False
        self.t = 0


class TSprite(Sprite):
    def __init__(self,kargs):
        Sprite.__init__(self)
        self.angle = 0
        self.scale = 1
        self.pos = np.array(kargs["pos"])


class AnSprite(Sprite):
    def __init__(self, animations):
        Sprite.__init__(self)
        self.animations = animations
        self.current_animation = None


    def update(self, dt,events=[],collisions={}):
        if self.current_animation != None:
            self.current_animation.update(dt,self)

    def play(self,animation,reset=True):
        self.current_animation = self.animations[animation]
        self.current_animation.play(reset)

    def pause(self):
        self.current_animation.pause()

    def stop(self):
        self.current_animation.stop()
