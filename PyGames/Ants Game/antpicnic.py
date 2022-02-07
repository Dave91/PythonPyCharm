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
        if has_end and dx is not None:
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
                nx = (steps[step][0] * 50) + 25
                ny = (steps[step][1] * 50) + 25
                nodes.append((nx, ny))
            return nodes

    def update(self):
        self.draw_path()


class Ants(pygame.sprite.Sprite):
    def __init__(self, dx, dy, nodes=None):
        super().__init__()

        walk_1 = pygame.image.load('ant1.png').convert_alpha()
        walk_2 = pygame.image.load('ant2.png').convert_alpha()
        walk_3 = pygame.image.load('ant3.png').convert_alpha()
        walk_4 = pygame.image.load('ant4.png').convert_alpha()

        self.ant_walk_anim = [walk_1, walk_2, walk_3, walk_4]
        self.frame_index = 0

        self.image = self.ant_walk_anim[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(50, 50))

        self.rect.x = dx
        self.rect.y = dy

        self.node_index = 0
        self.nodes_to_go = nodes
        self.can_go = False
        if self.nodes_to_go:
            self.can_go = True

    def animation_state(self):
        self.frame_index += 0.5
        if self.frame_index >= len(self.ant_walk_anim):
            self.frame_index = 0
        self.image = self.ant_walk_anim[int(self.frame_index)]

        if self.nodes_to_go:
            try:
                self.node_index += 2
                if (self.node_index // 10) > len(self.nodes_to_go):
                    return
                else:
                    node = self.nodes_to_go[self.node_index // 10]
                    self.rect.x = node[0]
                    self.rect.y = node[1]
            except IndexError:
                return
        else:
            return
            mdir = random.choice(["L", "R", "U", "D"])
            if mdir == "L":
                for m in range(4):
                    self.rect.x -= 2
            elif mdir == "R":
                self.image = pygame.transform.rotate(self.image, 180)
                for m in range(4):
                    self.rect.x += 2
            elif mdir == "U":
                self.image = pygame.transform.rotate(self.image, 90)
                for m in range(4):
                    self.rect.y -= 2
            else:
                self.image = pygame.transform.rotate(self.image, -90)
                for m in range(4):
                    self.rect.y += 2

    def update(self):
        self.animation_state()
        self.within_bounds()

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

        self.image = pygame.image.load('icons8-bread-48.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(50, 50))

        self.rect.x = dx
        self.rect.y = dy

    def update(self):
        if collision_sprite():
            pass


def display_score():

    '''score_surf = game_font.render(
        f'Time: {current_time} secs, stars: {stars}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)'''


def collision_sprite():

    if pygame.sprite.groupcollide(ants_group, food_group, False, True):
        return True
    else:
        return False


def init_dots():
    return
    for ant in range(80):
        ants_group.add(Ants(400, 350))
    for food in range(20):
        dx = random.randint(200, 750)
        dy = random.randint(200, 650)
        food_group.add(Food(dx, dy))


def get_input(pathfinder):
    global has_end
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            print(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                m_pos = pygame.mouse.get_pos()
                dx = m_pos[0]
                dy = m_pos[1]
                food_group.add(Food(dx, dy))
                has_end = True
                pathfinder.create_path(dx, dy)
                nodes = pathfinder.draw_path()
                ants_group.add(Ants(400, 350, nodes))


ants_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()

running = True
has_end = False


def main():
    pygame.init()
    screen_size = (800, 700)
    surface = pygame.display.set_mode(screen_size)
    bg = pygame.transform.scale(pygame.image.load("bgimg.jpg"), screen_size)
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    init_done = False
    if not init_done:
        init_dots()
        init_done = True

    matrix_done = False
    if not matrix_done:
        matrix = [[1 for col in range(16)] for row in range(14)]
        matrix_done = True

    pathfinder = Pathfinder(matrix, surface)

    while running:
        # surface.fill((255, 255, 255))
        surface.blit(bg, (0, 0))
        pygame.draw.circle(surface, (0, 0, 0), (425, 375), 25)
        get_input(pathfinder)
        ants_group.draw(surface)
        ants_group.update()
        food_group.draw(surface)
        food_group.update()

        game_active = collision_sprite()
        pathfinder.update()
        pygame.display.update()
        clock.tick(30)
        # count_pops(total_pop, d1_pop, d2_pop, d3_pop, d4_pop)

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
