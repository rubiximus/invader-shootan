"""
Invader Shootan v0.6
Created by Andrew Otto 4/12/2011

player.py
Contains the Player class which is the player-controlled sprite
"""


import pygame
from pygame.sprite import Sprite

from asprite import ASprite

class Player(ASprite):
    """The sprite for the player-controlled ship
    Has capability for 8-directional movement
    """
    
    def __init__(self, window_size, sprite_filename, speed):
        """Creates the player's ship
        window_size is a tuple with the window dimensions (width, height)
        sprite_filename is the sprite for the ship
        speed is the number of pixels per frame that can be moved
        """
        
        ASprite.__init__(self, sprite_filename, speed)
        self.window_size = window_size
        
        #The ship always starts at the bottom center of the screen
        bottom_pos = window_size[1] - 10
        x_pos = window_size[0] / 2
        self.rect = self.image.get_rect(bottom = bottom_pos, centerx = x_pos)
 
 
    def move(self, direction):
        """Moves the ship in the specified direction unless stopped by borders
        direction is a vector
        """
        
        ASprite.move(self, direction)
        
        width, height = self.window_size
        
        #if ship is off top or bottom edges, nudge back to the edge
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        
        #if ship is off left or right edges, nudge back to the edge
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
