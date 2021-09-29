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

water_density = 997

w_vec_vel = [0, 0, 0]
w_total_velocity = 0

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
        '\nX Vel: ' + str(round(w_vec_vel[0], 2)) + \
        '\nY Vel: ' + str(round(w_vec_vel[1], 2)) + \
        '\nZ Vel: ' + str(round(w_vec_vel[2], 2)) + \
        '\nTotal Vel.: ' + str(round(w_total_velocity, 2)) + \
        '\nX Pos: ' + str(round(w_vec_pos[0], 2)) + \
        '\nY Pos: ' + str(round(w_vec_pos[1], 2)) + \
        '\nZ Pos: ' + str(round(w_vec_pos[2], 2)) + \
        '\nHDG: ' + str(round(Convert_Angle_Rad_To_Deg(s_hdg), 2))
    
    s_hdg = Limit_Angle(s_hdg, 0, 2*math.pi)

    w_vec_vel[0] = w_total_velocity * math.cos(s_hdg)
    w_vec_vel[1] = w_total_velocity * math.sin(s_hdg)

    w_vec_pos[0] = w_vec_pos[0] + w_vec_vel[0] * dt
    w_vec_pos[1] = w_vec_pos[1] + w_vec_vel[1] * dt

    keys=pygame.key.get_pressed()

    if keys[pygame.K_w]:
        w_total_velocity = w_total_velocity + 0.01

    if keys[pygame.K_s]:
        w_total_velocity = w_total_velocity - 0.01

    if keys[pygame.K_a]:
        s_hdg = s_hdg - 0.01

    if keys[pygame.K_d]:
        s_hdg = s_hdg + 0.01

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill(pygame.Color('black'))
    blit_text(screen, debug_text, (20, 20), font)
    pygame.display.update()
