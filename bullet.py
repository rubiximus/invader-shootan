"""
Invader Shootan v0.6
Created by Andrew Otto 4/12/2011

bullet.py
Contains the Bullet class which is just a bullet...
"""


import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Simple sprite for a bullet that moves vertically across the screen and
    automatically kills itself when it hits the window borders
    """
    
    def __init__(self, window_size, sprite_filename, speed, position):
        """Creates a bullet that moves vertically
        window_size is a tuple with the window dimensions (width, height)
        sprite_filename is the sprite for the bullet
        speed is the number of pixels moved each frame -- negative value moves up
        position is a tuple for the coordinates of the center of the bullet
        """
        
        Sprite.__init__(self)
        self.window_size = window_size
        self.image = pygame.image.load(sprite_filename).convert_alpha()
        self.speed = speed
        
        self.rect = self.image.get_rect(center = position)
  
  
    def update(self):
        """"Moves the bullet vertically by the speed value givin at construction
        """
        
        self.rect = self.rect.move(0, self.speed)
        
        height = self.window_size[1]
        if  self.rect.bottom >= height or self.rect.top <= 0:
            self.kill()