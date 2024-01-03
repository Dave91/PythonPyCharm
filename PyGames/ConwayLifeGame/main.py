import pygame
import numpy as np

color_bg = (255, 255, 255)
color_grid = (0, 0, 0)
color_die_next = (0, 0, 0)
color_alive_next = (0, 0, 0)


def update(screen, cells, size, with_prog=False):
    upd_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row - 1: row * 2, col - 1: col * 2]) - cells[row, col]
        color = color_bg if cells[row, col] == 0 else color_alive_next

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_prog:
                    color = color_die_next
            elif 2 <= alive <= 3:
                upd_cells[row, col] = 1
                if with_prog:
                    color = color_alive_next
        else:
            if alive == 3:
                upd_cells[row, col] = 1
                if with_prog:
                    color = color_alive_next

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return upd_cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    size = 10
    cells = np.zeros((60, 80))
    screen.fill(color_grid)
    update(screen, cells, size)
    pygame.display.flip()
    pygame.display.update()
    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, size)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // size, pos[0] // size] = 1
                update(screen, cells, size)
                pygame.display.update()

        screen.fill(color_grid)
        if running:
            cells = update(screen, cells, size, with_prog=True)
            pygame.display.update()
            clock.tick(30)


if __name__ == '__main__':
    main()
