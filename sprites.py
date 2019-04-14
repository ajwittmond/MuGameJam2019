

import os
import numpy as np
from pygame.sprite import Sprite
import pygame

class Animation:
    def __init__(self, path,xtile,ytile,scale=1, fps=20):
        self.frames = []
        self.masks = []
        self.sheet = pygame.image.load(path)
        if scale != 1:
            w,h =  np.array( self.sheet.get_rect().size )*scale
            self.sheet = pygame.transform.scale(self.sheet,(int(w),int(h)))
        w ,h = np.array(self.sheet.get_rect().size)/[xtile,ytile]
        for y in range(0,ytile):
            for x in range(0,xtile):
                f = self.sheet.subsurface(pygame.Rect(x*w,y*h,w,h))
                self.frames.append ( f )
                self.masks.append(pygame.mask.from_surface(f))

        self.fps = fps
        self.playing = True
        self.t = 0
        self.playtime = -1
        self.rate = 1
        self.frame = 0
        self._frame_len = len(self.frames)

    def __len__(self):
        return self._frame_len

    def update(self,dt,sprite):
        if self.playing:
            self.t += dt*self.rate
            self.frame = int ( self.t*self.fps )
            self.frame %= self._frame_len
            sprite.image = self.frames[self.frame]
            sprite.mask = self.masks[self.frame]
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
    def __init__(self, kargs):
        Sprite.__init__(self)
        self.animations = kargs["animations"]
        self.current_animation = self.animations[kargs[ "current_animation" ]]
        self.image = self.current_animation.frames[0]
        self.rect = self.image.get_rect()


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
