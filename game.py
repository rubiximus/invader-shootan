"""
Invader Shootan v0.6
Created by Andrew Otto 4/12/2011

game.py
The game driver; handles graphics, keyboard input, collision detection, etc
"""


import sys

import pygame
from pygame.locals import *
from pygame.time import Clock
from pygame import key
from pygame.font import Font, get_default_font
from pygame.sprite import Sprite, Group

from options import *
from player import Player
from bullet import Bullet
from enemy_group import EnemyGroup
from enemy import Enemy

#initialize global sprites and groups -- player and enemy_wave are placeholders
#Sprite groups: all_sprites contains all sprites to draw
#               evil_bullets contains the enemy bullets
#               good_bullets contains the players bullets
#               enemy_wave will be an EnemyGroup containing the current wave
evil_bullets = Group()
good_bullets = Group()
enemy_wave = Group()

player = Sprite()

#global score and lives counters
score = 0
lives = starting_lives

def keyboard():
    """Checks for relevent keypresses and either
    moves the player, shoots, or quits the game"""
    
    key_states = key.get_pressed()
    if key_states[K_ESCAPE]:
        sys.exit()
    if key_states[K_LEFT]:
        player.move(-1, 0)
    elif key_states[K_RIGHT]:
        player.move(1, 0)
    if key_states[K_z] or key_states[K_SPACE] or key_states[K_LCTRL]:
        shoot()


def shoot():
    """Creates a new friendly bullet at the player's location if too many don't exist already
    """
    if len(good_bullets) < max_player_bullets:
        new_bullet = Bullet(window_size, bullet_filename, -bullet_speed, player.rect.center)
        new_bullet.add(good_bullets)
            

def collisions():
    """Does collision detection for all sprites.
    Currently handles: player/bullet, enemy/bullet, bullet/bullet
    """
    
    global lives, score, player
    
    #player with enemy bullets
    for current_bullet in evil_bullets.sprites():
        if pygame.sprite.collide_mask(player, current_bullet):
            current_bullet.kill()
            lives -= 1
            player = Player(window_size, ship_filename, ship_speed)
            
    #enemies with player bullets
    for current_enemy in enemy_wave.sprites():
        for current_bullet in good_bullets.sprites():
            if pygame.sprite.collide_mask(current_enemy, current_bullet):
                current_enemy.kill()
                current_bullet.kill()
                score += enemy_kill_pts
                
    #enemy bullets with player bullets
    for current_up in good_bullets.sprites():
        for current_down in evil_bullets.sprites():
            if pygame.sprite.collide_mask(current_up, current_down):
                current_up.kill()
                current_down.kill()
                score += bullet_kill_pts
    
 
def check_gameover():
    """Checks for gameover conditions and enters gameover loop
    current gameover conditions: no living enemies; bottom enemies reach player
    """
    
    if len(enemy_wave) == 0 or lives == -1:
        gameover()
    for current_enemy in enemy_wave.sprites():
        if current_enemy.rect.bottom >= player.rect.top:
            gameover()


def gameover():
    """The gameover loop
    Shows static image until the window is closed
    """
    
    sys_font = Font(get_default_font(), font_size)
    message = sys_font.render("GAME OVER", False, white)
    screen = pygame.display.get_surface()
    screen.blit(message, message.get_rect(centerx = width/2, top = 20))
    pygame.display.update()
    while 1:
        keyboard()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    
    
def main():
    """The main function of the game.
    Initializes PyGame objects and then enters the game loop
    """
    
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    
    sys_font = Font(get_default_font(), font_size)
    clock = Clock()
    
    #now that pygame is initialized, initialize inherited classes properly
    global enemy_wave, player
    enemy_wave = EnemyGroup(evil_bullets)
    
    player = Player(window_size, ship_filename, ship_speed)
    
    while 1:
        #limit framerate and prepare FPS display text
        clock.tick(max_framerate)
        fps = clock.get_fps()
        fps_text = sys_font.render("FPS: {0:.1f}".format(fps), False, white)
        
        score_text = sys_font.render("SCORE: {}".format(score), False, white)
        lives_text = sys_font.render("MANS: {}".format(lives), False, white)
    
        #check for QUIT event to prevent endless loopage
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            
        #call the game's thinking functions
        check_gameover()
        keyboard()
        evil_bullets.update()
        good_bullets.update()
        enemy_wave.update()
        collisions()
            
        #draw the stuff
        screen.fill(black)
        good_bullets.draw(screen)
        evil_bullets.draw(screen)
        enemy_wave.draw(screen)
        screen.blit(player.image, player.rect)
        screen.blit(score_text, score_text.get_rect(top = 0, left = 0))
        screen.blit(lives_text, lives_text.get_rect(top = 0, centerx = width / 2))
        screen.blit(fps_text, fps_text.get_rect(top = 0, right = width))
        pygame.display.update()
    

if __name__ == '__main__':
    main()
