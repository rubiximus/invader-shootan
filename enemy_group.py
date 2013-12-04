"""
Invader Shootan v0.6
Created by Andrew Otto 4/19/2011

enemy_group.py
Contains the EnemyGroup class which represents the enemy formation
"""


import random

import pygame
from pygame.sprite import Group

from options import *
from vector import SOUTH
from enemy import Enemy
from bullet import Bullet

class EnemyGroup(Group):
    """Special Group class that handles unison behavior for the enemy waves"""
    
    def __init__(self, bullets):
        """Initializes the group and makes a wave of enemies
        window_size is a tuple with the window dimensions (width, height)
        rows, cols are the height and width resp. of enemies in the waves
        gap is the number of pixels between each sprite
        speed is the number of pixels moved at once
        move_delay is the number of frames waited between movements
        shoot_delay is the number of frames between enemy shots
        bullets is a Group that will hold the enemies' bullets
        sprite_filename is the sprite file for the ships
        """
        
        Group.__init__(self)
        self.window_size = window_size
        self.rows = wave_rows
        self.cols = wave_cols
        self.gap = wave_gap
        self.speed = enemy_speed
        self.move_delay = enemy_delay
        self.shoot_delay = enemy_shoot_delay
        self.bullets = bullets
        self.sprite_filename = enemy_filename
        
        self.build_wave()
        
        
    def build_wave(self):
        """Creates the rectangular formation of enemies
        Enemy sprites are stored in the inherited Group and the instance formation
        """
        
        #build the formation and store in a 2d array indexed col, row
        self.formation = []
        for current_col in range(0, self.cols):
            col_list = []
            for current_row in range(0, self.rows):
                new_enemy = Enemy(self.window_size, self.sprite_filename, self.speed, current_col, current_row)
                
                left_pos = current_col * (self.gap + new_enemy.rect.width) + self.gap
                top_pos = current_row * (self.gap + new_enemy.rect.height) + self.gap
                new_enemy.rect = new_enemy.image.get_rect(left = left_pos, top = top_pos)
                
                col_list.append(new_enemy)
                Group.add(self, new_enemy)
            self.formation.append(col_list)
        
        self.leftmost_col = 0   #the left- and rightmost cols with living enemies
        self.rightmost_col = self.cols - 1
        self.move_delay_step = 0        #counts the frames between moves
        self.shoot_delay_step = 0       #counts the frames between shots
        self.current_vector = (1, 0)    #the wave always starts by moving right
        
    
    def update(self):
        """Instead of updating each sprite independently,
        this method is changed to move the enemies in unison
        movement happens once every <move_delay> frames
        
        New: a random bottom row enemy will shoot once every <shoot_delay> frames
        """
        
        #movement
        self.move_delay_step += 1
        if self.move_delay_step == self.move_delay:
            self.move_delay_step = 0
            movement_vector = self.check_vector()
            for current_sprite in Group.sprites(self):
                current_sprite.move(*movement_vector)

        self.shoot_delay_step += 1
        if self.shoot_delay_step == self.shoot_delay:
            self.shoot_delay_step = 0
            self.shoot()
    
    def check_vector(self):
        """Helper function for update
        Checks whether the formation can move in the current direction
        if border collision will happen, returns a down-pointing vector
        otherwise returns the current direction vector
        """
        
        #returns proper vector for when formation is moving right
        if self.current_vector == (1, 0):
            if self.living_sprite(self.rightmost_col).rect.right >= self.window_size[0]:
                self.current_vector = (-1, 0)
                return (0, 1)
            else:
                return self.current_vector
        
        #returns proper vector for when formation is moving left
        if self.current_vector == (-1, 0):
            if self.living_sprite(self.leftmost_col).rect.left <= 0:
                self.current_vector = (1, 0)
                return (0, 1)
            else:
                return self.current_vector
    
    
    def living_sprite(self, col):
        """Helper function
        returns the first living sprite in the given column index
        if none encountered, return None
        """
        
        for current_sprite in self.formation[col]:
            if current_sprite is not None:
                return current_sprite
        return None
    
    
    def bottom_sprite(self, col):
        """Helper function for shoot
        returns the bottom living sprite in the given column index
        if none encountered, return None
        """
        
        bottom = None
        for current_sprite in self.formation[col]:
            if current_sprite is not None:
                bottom = current_sprite
        return bottom
    
    
    def shoot(self):
        """Chooses a random bottom enemy to shoot
        the bullet is added to the self.bullets group
        """
        
        #pick a random living enemy, then make the bottom living enemy of that column shoot
        r = random.randint(0, len(self)-1)
        ##print ("Random = ", r)
        ##print ("Enemies = ", len(self))
        col = Group.sprites(self)[r].col
        shooter = self.bottom_sprite(col)
        
        new_bullet = Bullet(window_size, bullet_filename, bullet_speed, shooter.rect.center, SOUTH)
        new_bullet.add(self.bullets)
    
    
    def adjust_borders(self):
        """Helper function for remove
        checks and updates the left- and rightmost column markers
        (makes sure that they represent columns with living enemies)
        """
        
        #adjust leftmost_col
        while self.living_sprite(self.leftmost_col) is None:
            if self.leftmost_col == self.rightmost_col:
                return
            self.leftmost_col += 1
            
        #adjust rightmost_col
        while self.living_sprite(self.rightmost_col) is None:
            if self.leftmost_col == self.rightmost_col:
                return
            self.rightmost_col -= 1
    
    
    def add(self, *sprites):
        """EnemyGroup doesn't support adding.
        Enemies are generated by calling build_wave
        """
        
        pass
        
    
    def remove(self, *sprites):
        """Removes as normal but also updates the formation array"""
        
        for current_sprite in sprites:
            Group.remove(self, current_sprite)
            row = current_sprite.row
            col = current_sprite.col
            self.formation[col][row] = None
            if col == self.rightmost_col or col == self.leftmost_col:
                self.adjust_borders()
                
