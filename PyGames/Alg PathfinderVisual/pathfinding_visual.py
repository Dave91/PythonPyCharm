import random
from sys import exit

import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
# from pathfinding.core.diagonal_movement import DiagonalMovement


class Pathfinder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.path = []

    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1] // 10
        col = mouse_pos[0] // 10
        cur_cell_val = self.matrix[row][col]
        if cur_cell_val == 1:
            rect = pygame.Rect((col * 10, row * 10), (10, 10))
            pygame.draw.rect(screen, (255, 255, 255), rect)

    def draw_start_end(self):
        if startx is not None:
            startrect = pygame.Rect((startx * 10, starty * 10), (10, 10))
            pygame.draw.rect(screen, (0, 255, 0), startrect)
        if endx is not None:
            endrect = pygame.Rect((endx * 10, endy * 10), (10, 10))
            pygame.draw.rect(screen, (255, 0, 0), endrect)

    def create_path(self):
        if startx is not None and endx is not None:
            start = self.grid.node(startx, starty)
            end = self.grid.node(endx, endy)

            finder = AStarFinder(diagonal_movement=allow_diag)
            self.path = finder.find_path(start, end, self.grid)
            self.grid.cleanup()

    def draw_path(self):
        if self.path and startx is not None and endx is not None:
            steps = self.path[0]
            nodes = []
            for step in range(len(steps)):
                # +5 for circle, line / not for rect
                nx = (steps[step][0] * 10) + 5
                ny = (steps[step][1] * 10) + 5
                nodes.append((nx, ny))
            try:
                pygame.draw.lines(screen, (255, 155, 55), False, nodes, 5)
            except ValueError:
                return

    def update(self):
        self.draw_active_cell()
        self.draw_start_end()
        self.draw_path()


pygame.init()
screen = pygame.display.set_mode((600, 600))
ant = pygame.image.load("Ant-icon.png")
pygame.display.set_icon(ant)
clock = pygame.time.Clock()
matrix_done = False


def init_matrix():
    global matrix_done
    if not matrix_done:
        matrix = [[1 for col in range(60)] for row in range(60)]
        for w in range(1500):
            wr, wc = random.randint(0, 59), random.randint(0, 59)
            matrix[wr][wc] = 0
        matrix_done = True
    return matrix


def draw_walls():
    for rw in range(60):
        for cl in range(60):
            if matrix[rw][cl] == 0:
                rectwall = pygame.Rect((cl * 10, rw * 10), (10, 10))
                pygame.draw.rect(screen, (0, 0, 0), rectwall)


matrix = init_matrix()
pathfinder = Pathfinder(matrix)
allow_diag = 0
has_start = False
startx, starty = None, None
endx, endy = None, None


def get_act_cell_val():
    mouse_pos = pygame.mouse.get_pos()
    row = mouse_pos[1] // 10
    col = mouse_pos[0] // 10
    cur_cell_val = matrix[row][col]
    return cur_cell_val


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_d:
                if allow_diag == 0:
                    allow_diag = 1
                else:
                    allow_diag = 0
                pathfinder.create_path()
            if event.key == pygame.K_SPACE:
                startx, endx = None, None
                has_start = False
                matrix_done = False
                matrix = init_matrix()
                pathfinder = Pathfinder(matrix)
                draw_walls()
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            if event.button == 3 and get_act_cell_val() != 0:
                endx = None
                startx, starty = m_pos[0] // 10, m_pos[1] // 10
                has_start = True
            if event.button == 1 and has_start and get_act_cell_val() != 0:
                endx, endy = m_pos[0] // 10, m_pos[1] // 10
                pathfinder.create_path()

    screen.fill((155, 155, 255))
    draw_walls()

    pathfinder.update()
    pygame.display.update()
    clock.tick(60)
