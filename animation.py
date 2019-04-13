import os
from pygame.sprite import Sprite
import numpy as np

class Animation:
    def __init__(self,frames,fps):
        self.frames = frames
 
class AnimatedSprite(Sprite):
 
    def __init__(self, path,xtile,ytile, pos, fps=20):
        Sprite.__init__(self)
        self.frames = []
        self.sheet = pygame.image.load(path)
        w ,h = np.array(self.sheet.get_rect().size)/[xtile,ytile]
        for y in range(0,ytile):
            for x in range(0,xtile):
                frame[x+y] = self.sheet.subsurface(pygame.Rect(x*w,y*h,w,h))
        self.image = frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.current = 0         # current image of the animation
        self.t = 0
        self.playing = 0         # to know if it is playing
        self._next_update = 0    # next time it has to be updated in ms
        self._inv_period = 1/fps  # 1./period of the animation in ms
        self._frames_len = len(self.frames)

    @property
    def fps():
        return self._inv_period

    @fps.setter
    def fps(self,fps):
        self._inv_period = 1/fps

    def update(self, dt):     
        # dt: time that has passed in last pass through main loop,  t: current time
        if self.playing:
            self.t += dt
            # period is duration of one frame, so dividing the time the animation
            # is running by the period of one frame on gets the number of frames
            self.current = int(self.t*self._inv_period)
            self.current %= self._frames_len
            # update image
            self.image = self.frames[self.current]
            # only needed if size changes between frames
            self.rect = self.image.get_rect(center=self.rect.center)
