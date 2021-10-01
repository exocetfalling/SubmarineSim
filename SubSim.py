# Imports

import math
from typing import cast
import pygame
from pygame import image
import pygame.freetype  # Import the freetype module.
from pygame.math import disable_swizzling

# Variables
# Axes are defined as:
# For vehicle:
# X: left -ve, right +ve
# Y: aft -ve, forward +ve
# Z: down -ve, up +ve

# For world:
# X: west -ve, east +ve
# Y: south -ve, north +ve
# Z: down -ve, up +ve

c_sub_dimensions = [4, 5, 2]
c_sub_mass = 10000
c_sub_vol = 40
c_sub_drag_area = [8, 10, 8]
c_ballast_vol_max = 20
c_sub_prop_radius = 1
c_sub_max_exit_vel = 20

s_hdg = 0
s_ballast = 0 # vol filled with water.

s_vec_acc = [0, 0, 0]

water_density = 1000

w_vec_acc = [0, 0, 0]
w_vec_vel = [0, 0, 0]
w_total_velocity = 0

w_vec_pos = [0, 0, -100]

d_screen_size = [0, 0]
d_screen_ctr = [0, 0]
toggle_debug = 1

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

i_compass = ''
i_size = [0, 0]

pygame.init()
SIZE = WIDTH, HEIGHT = (1024, 720)
FPS = 60
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()
i_compass = pygame.image.load('compass.png')
i_size = pygame.Surface.get_size(i_compass)
pygame.Surface.set_colorkey(i_compass, white)
# Functions
def Convert_Angle_Rad_To_Deg(angle_rad):
    return angle_rad * 57.2958

def Convert_Angle_Deg_To_Rad(angle_deg):
    return angle_deg / 57.2958

def Calc_Force_Thrust(fluid_density, prop_radius, entry_vel, exit_vel):
    return 0.5 * fluid_density * math.pi * pow(prop_radius, 2) * (pow(exit_vel, 2) - pow(entry_vel, 2))

def Calc_Force_Drag(fluid_density, obj_velocity, surface_area, drag_coeff):
    return -0.5 * fluid_density * obj_velocity * obj_velocity * surface_area * drag_coeff

def Calc_Acc(force, mass):
    return force / mass

def Limit_Angle(angle_rad, angle_min, angle_max):
    if (angle_rad < angle_min):
        return angle_max
    elif (angle_rad > angle_max):
        return angle_min
    else:
        return angle_rad

def Calc_Fluid_Density(current_depth):
    return -0.004 * current_depth + 1030

def Calc_Buoyant_force(vol_sub, vol_ballast, fluid_density):
    if (w_vec_pos[2] < 0):
        return (vol_sub - vol_ballast) * fluid_density * 9.81
    else:
        return 0

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
    
    s_vec_acc[1] = \
        Calc_Acc(Calc_Force_Thrust(water_density, c_sub_prop_radius, w_total_velocity, c_sub_max_exit_vel), c_sub_mass) + \
        Calc_Acc(Calc_Force_Drag(water_density, w_total_velocity, c_sub_drag_area[1], 1.0))
    w_vec_acc[2] = \
        ((Calc_Buoyant_force(c_sub_vol, s_ballast, water_density)) / c_sub_mass - 9.81) + \
        -10 * w_vec_vel[2]

    w_vec_vel[0] = w_total_velocity * math.cos(s_hdg)
    w_vec_vel[1] = w_total_velocity * math.sin(s_hdg)
    w_vec_vel[2] = w_vec_vel[2] + w_vec_acc[2] * dt

    w_vec_pos[0] = w_vec_pos[0] + w_vec_vel[0] * dt
    w_vec_pos[1] = w_vec_pos[1] + w_vec_vel[1] * dt
    w_vec_pos[2] = w_vec_pos[2] + w_vec_vel[2] * dt

    keys=pygame.key.get_pressed()

    if keys[pygame.K_w]:
        w_total_velocity = w_total_velocity + 0.01

    if keys[pygame.K_s]:
        w_total_velocity = w_total_velocity - 0.01

    if keys[pygame.K_a]:
        s_hdg = s_hdg - 0.01

    if keys[pygame.K_d]:
        s_hdg = s_hdg + 0.01

    if keys[pygame.K_u]:
        s_ballast = s_ballast - 0.2

    if keys[pygame.K_j]:
        s_ballast = s_ballast + 0.2

    
    if keys[pygame.K_o]:
        toggle_debug = 1
    
    if keys[pygame.K_p]:
        toggle_debug = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    
    d_screen_size = pygame.display.get_window_size()
    d_screen_ctr = [(d_screen_size[0] / 2), (d_screen_size[1] / 2)]
    #pygame.draw.rect(screen, red, (400,400,50,25))
    #pygame.draw.circle(screen, white, (d_screen_ctr[0],d_screen_ctr[1]), 75)
    pygame.transform.rotate(i_compass, -Convert_Angle_Rad_To_Deg(s_hdg))
    screen.blit(i_compass, (d_screen_ctr[0] - i_size[0] / 2, d_screen_ctr[1] - i_size[1] / 2))

    if (toggle_debug == 1):
        screen.fill(pygame.Color('black'))
        blit_text(screen, debug_text, (20, 20), font)
    
    pygame.display.flip()
