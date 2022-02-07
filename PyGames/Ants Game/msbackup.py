import random
from sys import exit

import pygame


class BlackDot(pygame.sprite.Sprite):
    def __init__(self, dx, dy):
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

    def animation_state(self):
        self.frame_index += 0.5
        if self.frame_index >= len(self.ant_walk_anim):
            self.frame_index = 0
        self.image = self.ant_walk_anim[int(self.frame_index)]

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
        self.destroy()

    def destroy(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > 780:
            self.rect.x = 780
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 680:
            self.rect.y = 680
            # self.remove()


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
            # self.kill()
        self.destroy()

    def destroy(self):
        pass
        # self.remove()


def display_score():

    '''score_surf = game_font.render(
        f'Time: {current_time} secs, stars: {stars}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)'''


def collision_sprite():

    if pygame.sprite.groupcollide(blackdot_group, food_group, False, True):
        return True
    else:
        return False


dtotal = [[], [], [], []]
dot_act = [0, 0, 0, 0]
dot_life = [0, 0, 0, 0]
dot_rep = [0, 0, 0, 0]
dot_age = [[], [], [], []]

blackdot_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()


def init_dots():
    for ant in range(80):
        blackdot_group.add(BlackDot(150, 150))
    for food in range(20):
        dx = random.randint(200, 750)
        dy = random.randint(200, 650)
        food_group.add(Food(dx, dy))


def get_input():
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


running = True
fps = 30


def count_pops(total_pop, d1_pop, d2_pop, d3_pop, d4_pop):
    dp = [0, 0, 0, 0]
    for i in range(4):
        for d in dtotal[i]:
            dp[i] += 1
    tp = dp[0] + dp[1] + dp[2] + dp[3]
    total_pop.configure(text="Total Pop.: " + str(tp))
    d1_pop.configure(text="Black Pop.: " + str(dp[0]))
    d2_pop.configure(text="Red Pop.: " + str(dp[1]))
    d3_pop.configure(text="Green Pop.: " + str(dp[2]))
    d4_pop.configure(text="Blue Pop.: " + str(dp[3]))


def main():
    pygame.init()
    screen_size = (800, 700)
    surface = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    init_done = False
    if not init_done:
        init_dots()
        init_done = True

    while running:
        surface.fill((255, 255, 255))
        get_input()
        blackdot_group.draw(surface)
        blackdot_group.update()
        food_group.draw(surface)
        food_group.update()

        game_active = collision_sprite()
        pygame.display.update()
        clock.tick(fps)
        # count_pops(total_pop, d1_pop, d2_pop, d3_pop, d4_pop)

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
