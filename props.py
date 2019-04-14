import pygame
import numpy as np
from sprites import *
from Engine import *
from Player import GravitySprite

@Engine.addEntity
class Prop(TSprite):
    name="prop"
    groups=["draw"]
    def __init__(self,kargs):
        TSprite.__init__(self,kargs)
        self.image = kargs["image"]
        self.rect = self.image.get_rect(center=kargs["pos"])


#objects that experience gravity and collide with planets
@Engine.addGroup
class PhysGroup(pygame.sprite.Group):
    name = "phys"

Engine.collision_pairs.append(["phys","planets"])

#expects an animation named "idle" and a lifetime but no current animation
@Engine.addEntity
class PhysObj(GravitySprite,AnSprite):
    name = "phys_obj"
    groups = ["phys","draw"]

    def __init__(self,kwargs):
        kwargs["current_animation"]="idle"
        GravitySprite.__init__(self,kwargs)
        AnSprite.__init__(self,kwargs)
        self.lifetime = kwargs.get("lifetime",float("inf"))
        self.restitution = kwargs.get("restitution",0.5)

    def update(self,dt,events,collision):
        self.lifetime-=dt
        self.calculateGravity()
        if self in collision:
            for x in collision[self]:
                if isinstance(x,Engine.entities["planet"]):
                    p = pygame.sprite.collide_mask(self,x)
                    if p:
                        #bounce off
                        d = x.pos - self.pos
                        d /= np.linalg.norm(d)
                        r = self.velocity.dot(d)*(-1-self.restitution)
                        self.velocity += r
        if self.lifetime < 0:
            self.kill()






