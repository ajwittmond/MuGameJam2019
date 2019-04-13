

import os
import numpy as np
from pygame.sprite import Sprite

class Animation:
    def __init__(self,frames,fps):
        self.frames = frames
        self._inv_period = 1/fps
        self.playing = True
        self.t = 0
        self.playtime = -1
        self.rate = 1
        self.frame = 0
        self._frame_len = len(frames)

    def __len__():
        return self._frame_len

    def update(self,dt,sprite):
        if self.playing:
            self.t += dt*rate
            self.frame = int ( self.t*self._inv_period )
            self.frame %= self._frame_len
            sprite.image = self.frames[self.frame]
            sprite.rect = sprite.image.get_rect(center = sprite.rect.center)
            if self.playtime > 0 and self.playtime >= self.t :
                self.playing = False
    @property
    def fps():
        return self._inv_period

    @fps.setter
    def fps(self,fps):
        self._inv_period = 1/fps

    def play(reset=True):
        self.playing = True
        if reset:
            self.t = 0

    def pause():
        self.playing = False

    def stop():
        self.playing = False
        self.t = 0


class TSprite(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.angle = 0
        self.scale = 1
        self.pos = np.array( self.rect.center )


class AnSprite(Sprite):
    def __init__(self, animations):
        Sprite.__init__(self)
        self.animations = animations
        self.current_animation = None


    def update(self, dt):
        if self.current_animation != None:
            self.current_animation.update(dt,self)
