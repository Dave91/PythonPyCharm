import pygame
import os
import bupgrid

width, height = 800, 600
size = (width, height)

pygame.init()
pygame.display.set_caption("Conway's Game of Life")
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 120

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 14, 71)

scale = 10
offset = 1

Grid = grid.Grid(width, height, scale, offset)
Grid.random_array()

running = True
while running:
    clock.tick(fps)
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Grid.conway(white, blue, screen)

    pygame.display.update()
