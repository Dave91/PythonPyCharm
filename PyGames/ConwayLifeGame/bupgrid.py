import pygame
import numpy as np
import random


class Grid:
    def __init__(self, width, height, scale, offset):
        self.rows = width // scale
        self.cols = height // scale
        self.size = (self.rows, self.cols)
        self.grid_array = np.ndarray(shape=self.size)
        self.scale = scale
        self.offset = offset

    def random_array(self):
        for x in range(self.rows):
            for y in range(self.cols):
                self.grid_array[x][y] = random.randint(0, 1)

    def conway(self, off_color, on_color, surface):
        for x in range(self.rows):
            for y in range(self.cols):
                x_pos = x * self.scale
                y_pos = y * self.scale
                if self.grid_array[x][y] == 1:
                    pygame.draw.rect(surface, on_color,
                                     [x_pos, y_pos, self.scale - self.offset, self.scale - self.offset])
                else:
                    pygame.draw.rect(surface, off_color,
                                     [x_pos, y_pos, self.scale - self.offset, self.scale - self.offset])
        cnext = np.ndarray(shape=self.size)
        for x in range(self.rows):
            for y in range(self.cols):
                state = self.grid_array[x][y]
                neighbors = self.get_neighbors(x, y)
                if state == 0 and neighbors == 1:
                    cnext[x][y] = 1
                elif state == 1 and (neighbors < 2 or neighbors > 3):
                    cnext[x][y] = 0
                else:
                    cnext[x][y] = state
        self.grid_array = cnext

    def get_neighbors(self, x, y):
        total = 0
        for n in range(-1, 2):
            for m in range(-1, 2):
                x_edge = (x + n + self.rows) % self.rows
                y_edge = (y + m + self.cols) % self.cols
                total += self.grid_array[x_edge][y_edge]
        total -= self.grid_array[x][y]
        return total
