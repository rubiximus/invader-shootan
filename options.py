"""
Invader Shootan v0.6
Created by Andrew Otto 4/23/2011

options.py
Contains all the global parameters controlling game behavior

Note: This file may be imported by multiple classes -- alter with caution.
"""


#screen constants
window_size = (width, height) = (800, 600)
max_framerate = 60
black = (0, 0, 0)
white = (255, 255, 255)

#player ship options
ship_filename = "graphics/ship.png"
starting_lives = 2
ship_speed = 5
max_player_bullets = 1

#enemy ship/wave options
enemy_filename = "graphics/enemy.png"
enemy_speed = 15
enemy_delay = 20
enemy_shoot_delay = 60
wave_rows = 5
wave_cols = 11
wave_gap = 15

#bullet options
bullet_filename = "graphics/bullet.png"
bullet_speed = 5

#font options
font_size = 15

#scoring options
enemy_kill_pts = 100
bullet_kill_pts = 50