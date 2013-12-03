"""
Invader Shootan v0.6
Created by Andrew Otto 4/19/2011

enemy.py
Contains the Enemy class which is controlled by the EnemyGroup
"""


import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    """The Enemy sprite is essentially a placeholder
    All actual behavior for the sprites is determined in the EnemyGroup class
    """
    
    def __init__(self, window_size, sprite_filename, speed, x, y):
        """Creates the enemy and places in the default upper left position
        window_size is a tuple with the window dimensions (width, height)
        sprite_filename is the sprite for the ship
        speed is the number of pixels it can move at once
        x, y are the sprite's column and row (resp.) in the formation
        """
        
        Sprite.__init__(self)
        self.window_size = window_size
        #self.image = pygame.image.load(sprite_filename).convert_alpha() #duplicate line?
        self.speed = speed
        self.col = x
        self.row = y
        
        self.image = pygame.image.load(sprite_filename).convert_alpha()
        self.rect = self.image.get_rect()
        
        
    def move(self, horizontal, vertical):
        """Moves the ship in the specified directions
        horizontal should be -1 to move left, 1 to move right, 0 otherwise
        vertical should be -1 to move up, 1 to move down, 0 otherwise
        Note: Crazy things happen if other values entered!
        """
        
        self.rect = self.rect.move(horizontal * self.speed, 0)
        self.rect = self.rect.move(0, vertical * self.speed)
        
    
    def kill(self):
        """Overridden kill function
        just calls the EnemyGroup function that handles proper removal
        """
        
        for current_group in self.groups():
            current_group.remove(self)
