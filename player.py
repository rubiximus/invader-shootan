"""
Invader Shootan v0.6
Created by Andrew Otto 4/12/2011

player.py
Contains the Player class which is the player-controlled sprite
"""


import pygame
from pygame.sprite import Sprite

class Player(Sprite):
    """The sprite for the player-controlled ship
    Has capability for 8-directional movement
    """
    
    def __init__(self, window_size, sprite_filename, speed):
        """Creates the player's ship
        window_size is a tuple with the window dimensions (width, height)
        sprite_filename is the sprite for the ship
        speed is the number of pixels per frame that can be moved
        """
        
        Sprite.__init__(self)
        self.window_size = window_size
        self.image = pygame.image.load(sprite_filename).convert_alpha()
        self.speed = speed
        
        #The ship always starts at the bottom center of the screen
        bottom_pos = window_size[1] - 10
        x_pos = window_size[0] / 2
        self.rect = self.image.get_rect(bottom = bottom_pos, centerx = x_pos)
 
 
    def move(self, horizontal, vertical):
        """Moves the ship in the specified directions unless stopped by borders
        horizontal should be -1 to move left, 1 to move right, 0 otherwise
        vertical should be -1 to move up, 1 to move down, 0 otherwise
        Note: Crazy things happen if other values entered!
        """
        
        width, height = self.window_size
        speed = self.speed
        next_left = self.rect.left + horizontal * speed
        next_right = next_left + self.rect.width
        next_top = self.rect.top + vertical * speed
        next_bottom = next_top + self.rect.height
        
        if next_left >= 0 and next_right <= width:
            self.rect = self.rect.move(horizontal * speed, 0)
        if next_top >= 0 and next_bottom <= height:
            self.rect = self.rect.move(0, vertical * speed)