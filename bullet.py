"""
Invader Shootan v0.6
Created by Andrew Otto 4/12/2011

bullet.py
Contains the Bullet class which is just a bullet...
"""


import pygame
from pygame.sprite import Sprite

from asprite import ASprite

class Bullet(ASprite):
    """Simple sprite for a bullet that moves across the screen and
    automatically kills itself when it hits the window borders
    """
    
    def __init__(self, window_size, sprite_filename, speed, position, direction):
        """Creates a bullet that moves vertically
        window_size is a tuple with the window dimensions (width, height)
        sprite_filename is the sprite for the bullet
        speed is the number of pixels moved each frame
        position is a tuple for the coordinates of the center of the bullet
        direction is a vector
        """
        
        ASprite.__init__(self, sprite_filename, speed)
        self.window_size = window_size
        self.direction = direction
        
        self.rect = self.image.get_rect(center = position)
  
  
    def update(self):
        """"Moves the bullet vertically by the speed value givin at construction
        """
        
        self.move(self.direction)
        
        width = self.window_size[0]
        height = self.window_size[1]
        if ( self.rect.bottom >= height or self.rect.top <= 0 or
             self.rect.right >= width or self.rect.left <= 0 ):
            self.kill()
