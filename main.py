import pygame
from pygame.locals import *

import keyboard

import math

import random

pygame.init()


r1,g1,b1 = 0,0,255


fps = 60
fpsClock = pygame.time.Clock()

width, height = 1080, 720
screen = pygame.display.set_mode((width, height))

pixel_with_margin = 4
margin = 0
brush = 10

grid = []
for y in range(math.ceil(width/pixel_with_margin)+2):
    grid.append([])
    for x in range(math.ceil(height/pixel_with_margin)+2):
        grid[y].append([255,255,255])

# Game loop.
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    if keyboard.is_pressed("l"):
        r1 = random.randint(0,255)
        g1 = random.randint(0,255)
        b1 = random.randint(0,255)


    if keyboard.is_pressed("q"):
        r1 = 255
        g1 = 0
        b1 = 0
    if keyboard.is_pressed("w"):
        r1 = 0
        g1 = 255
        b1 = 0
    if keyboard.is_pressed("e"):
        r1 = 0
        g1 = 0
        b1 = 255


    ycounter = 0

    if pygame.mouse.get_pressed()[0]:
        clickpos = pygame.mouse.get_pos()
        ecks = math.floor(clickpos[0]/pixel_with_margin)
        why = math.floor(clickpos[1]/pixel_with_margin)

        if not ecks > len(grid)-2:
            if not why > len(grid[1])-2:
                for x in range(brush):
                    for y in range(brush):
                        if not keyboard.is_pressed('b'):
                            grid[ecks+(x-1)][why+(y-math.ceil(brush/2))] = [r1,g1,b1]
                        else:
                            grid[ecks+(x-1)][why+(y-math.ceil(brush/2))] = [0,0,0]



    if keyboard.is_pressed("space"):
        for wh in range(len(grid)-1):
            for ex in range(len(grid[wh])-1):
                lolr = 0
                lolg = 0
                lolb = 0
                for x in range(3):
                    for y in range(3):
                        lolr += grid[wh+(x-1)][ex+(y-1)][0]
                        lolg += grid[wh+(x-1)][ex+(y-1)][1]
                        lolb += grid[wh+(x-1)][ex+(y-1)][2]
                lolr /= 9
                lolg /= 9
                lolb /= 9
                grid[wh][ex][0] = lolr
                grid[wh][ex][1] = lolg
                grid[wh][ex][2] = lolb





    for y in range(math.ceil(width/pixel_with_margin)):
        xcounter = 0
        for x in range(math.ceil(height/pixel_with_margin)):
            pygame.draw.rect(screen,grid[ycounter][xcounter],(1+(pixel_with_margin*y),(1+(x*pixel_with_margin)),pixel_with_margin-margin,pixel_with_margin-margin))
            xcounter += 1
        ycounter += 1

    pygame.draw.circle(screen, (r1,g1,b1), (20,20), 10)

    pygame.display.flip()
    fpsClock.tick(fps)
