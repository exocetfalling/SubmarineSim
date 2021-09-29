# Imports

import math
from typing import cast
import pygame
import pygame.freetype  # Import the freetype module.

# Variables
# Axes are defined as:
# For aircraft:
# X: left -ve, right +ve
# Y: aft -ve, forward +ve
# Z: down -ve, up +ve

# For world:
# X: west -ve, east +ve
# Y: south -ve, north +ve
# Z: down -ve, up +ve

s_hdg = 0
s_depth = 0

w_x_velocity = 0
w_y_velocity = 0
w_z_velocity = 0

w_total_velocity = 0

w_x_pos = 0
w_y_pos = 0
w_z_pos = 0

w_vec_pos = [0, 0, 0]

pygame.init()
SIZE = WIDTH, HEIGHT = (1024, 720)
FPS = 60
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()

# Functions
def Convert_Angle_Rad_To_Deg(angle_rad):
    return angle_rad * 57.2958

def Convert_Angle_Deg_To_Rad(angle_deg):
    return angle_deg / 57.2958

def Limit_Angle(angle_rad, angle_min, angle_max):
    if (angle_rad < angle_min):
        return angle_max
    elif (angle_rad > angle_max):
        return angle_min
    else:
        return angle_rad

def blit_text(surface, text, pos, font, color=pygame.Color('green')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.



font = pygame.font.SysFont('Courier', 16)

while True:

    dt = clock.tick(FPS) / 1000
    debug_text = \
        '\nX Vel: ' + str(round(w_x_velocity, 2)) + \
        '\nY Vel: ' + str(round(w_y_velocity, 2)) + \
        '\nZ Vel: ' + str(round(w_z_velocity, 2)) + \
        '\nTotal: ' + str(round(w_total_velocity, 2)) + \
        '\nDEPTH: ' + str(round(s_depth, 2)) + \
        '\nHDG: ' + str(round(Convert_Angle_Rad_To_Deg(s_hdg), 2))

    keys=pygame.key.get_pressed()

    if keys[pygame.K_w]:
        s_depth = s_depth - 0.1

    if keys[pygame.K_s]:
        s_depth = s_depth + 0.1

    if keys[pygame.K_a]:
        s_hdg = s_hdg - 0.1

    if keys[pygame.K_d]:
        s_hdg = s_hdg + 0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(pygame.Color('black'))
    blit_text(screen, debug_text, (20, 20), font)
    pygame.display.update()
