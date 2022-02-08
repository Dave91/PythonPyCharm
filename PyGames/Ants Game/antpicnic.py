import random
from sys import exit

import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Pathfinder:
    def __init__(self, matrix, surface):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.screen = surface
        self.path = []

    def create_path(self, dx, dy):
        if dx is not None:
            start = self.grid.node(400 // 50, 350 // 50)
            end = self.grid.node(dx // 50, dy // 50)

            finder = AStarFinder(diagonal_movement=False)
            self.path = finder.find_path(start, end, self.grid)
            self.grid.cleanup()

    def draw_path(self):
        if self.path:
            steps = self.path[0]
            nodes = []
            for step in range(len(steps)):
                nx = steps[step][0] * 50
                ny = steps[step][1] * 50
                nodes.append((nx, ny))
            return nodes

    def update(self):
        self.draw_path()


class Ants(pygame.sprite.Sprite):
    def __init__(self, dx, dy, nodes=None):
        super().__init__()

        walk_1 = pygame.image.load('assets/ant1.png').convert_alpha()
        walk_2 = pygame.image.load('assets/ant2.png').convert_alpha()
        walk_3 = pygame.image.load('assets/ant3.png').convert_alpha()
        walk_4 = pygame.image.load('assets/ant4.png').convert_alpha()

        self.ant_walk_anim = [walk_1, walk_2, walk_3, walk_4]
        self.frame_index = 0

        self.image = self.ant_walk_anim[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(50, 50))

        self.rect.x = dx
        self.rect.y = dy

        self.node_index = 0
        self.nodes_to_go = nodes
        self.has_end = False
        self.coll_food = None

    def animation_state(self):
        self.frame_index += 0.5
        if self.frame_index >= len(self.ant_walk_anim):
            self.frame_index = 0
        self.image = self.ant_walk_anim[int(self.frame_index)]

        if self.nodes_to_go:
            if not self.has_end:
                try:
                    self.node_index += 2
                    if (self.node_index // 10) == len(self.nodes_to_go) + 1:
                        self.has_end = True
                        self.node_index = 0
                        self.nodes_to_go.reverse()
                    else:
                        nind = self.node_index // 10
                        node = self.nodes_to_go[nind]
                        self.rotate_ant(nind + 1)
                        self.rect.x = node[0]
                        self.rect.y = node[1]
                except IndexError:
                    return
            else:
                try:
                    self.node_index += 2
                    if (self.node_index // 10) == len(self.nodes_to_go) + 1:
                        self.has_end = False
                        self.node_index = 0
                        self.kill()
                        try:
                            self.coll_food[self][0].kill()
                            self.coll_food = None
                        except KeyError:
                            pass
                    else:
                        nind = self.node_index // 10
                        node = self.nodes_to_go[nind]
                        self.rotate_ant(nind + 1)
                        self.rect.x = node[0]
                        self.rect.y = node[1]
                except IndexError:
                    return
        else:
            return

    def rotate_ant(self, ni):
        mdirs = {(0, 0): "N", (-1, 0): "L", (1, 0): "R", (0, -1): "U", (0, 1): "D"}
        try:
            node = self.nodes_to_go[ni]
            mdir = mdirs[((node[0] - self.rect.x) // 50, (node[1] - self.rect.y) // 50)]
            if mdir != "N":
                if mdir == "L":
                    pass
                elif mdir == "R":
                    self.image = pygame.transform.rotate(self.image, 180)
                elif mdir == "U":
                    self.image = pygame.transform.rotate(self.image, 90)
                else:
                    self.image = pygame.transform.rotate(self.image, -90)
        except KeyError:
            return

    def update(self):
        self.animation_state()
        self.within_bounds()
        if collision_sprite():
            self.coll_food = pygame.sprite.groupcollide(ants_group, food_group, False, False)
        if self.coll_food:
            try:
                self.coll_food[self][0].rect.x = self.rect.x
                self.coll_food[self][0].rect.y = self.rect.y
            except KeyError:
                pass

    def within_bounds(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 780:
            self.rect.x = 780
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 680:
            self.rect.y = 680


class Food(pygame.sprite.Sprite):
    def __init__(self, dx, dy):
        super().__init__()

        self.image = pygame.image.load('assets/icons8-bread-48.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(50, 50))

        self.rect.x = dx
        self.rect.y = dy

    def update(self):
        if collision_sprite():
            pass


def collision_sprite():
    if pygame.sprite.groupcollide(ants_group, food_group, False, False):
        return True
    else:
        return False


def init_dots():
    for ant in range(80):
        ants_group.add(Ants(400, 350))
    for food in range(20):
        dx = random.randint(200, 750)
        dy = random.randint(200, 650)
        food_group.add(Food(dx, dy))


def get_input(pathfinder):
    global intro
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if intro:
                    intro = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                m_pos = pygame.mouse.get_pos()
                dx = m_pos[0]
                dy = m_pos[1]
                food_group.add(Food(dx, dy))
                pathfinder.create_path(dx, dy)
                nodes = pathfinder.draw_path()
                ants_group.add(Ants(400, 350, nodes))


def display_intro(surface):
    surface.fill((255, 255, 255))
    logo = pygame.image.load("assets/logo.png").convert_alpha()
    logo_rect = logo.get_rect(center=(400, 250))
    surface.blit(logo, logo_rect)
    intro_font = pygame.font.SysFont('Calibri', 32)
    intro_surf = intro_font.render("Press Space to begin...", False, (64, 64, 64))
    intro_rect = intro_surf.get_rect(center=(400, 350))
    surface.blit(intro_surf, intro_rect)
    pygame.display.update()


ants_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()

running = True
intro = True


def main():
    pygame.init()
    screen_size = (800, 700)
    surface = pygame.display.set_mode(screen_size)
    bg = pygame.transform.scale(pygame.image.load("assets/bgimg.jpg"), screen_size)
    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    init_done = False
    if not init_done:
        # init_dots()  # when a starting num of stuff needed
        init_done = True

    matrix_done = False
    if not matrix_done:
        matrix = [[1 for col in range(16)] for row in range(14)]
        matrix_done = True

    pathfinder = Pathfinder(matrix, surface)

    while intro:
        get_input(pathfinder)
        display_intro(surface)

    while running:
        surface.blit(bg, (0, 0))
        pygame.draw.circle(surface, (0, 0, 0), (425, 375), 25)
        get_input(pathfinder)
        ants_group.draw(surface)
        ants_group.update()
        food_group.draw(surface)
        food_group.update()

        collision_sprite()
        pathfinder.update()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
