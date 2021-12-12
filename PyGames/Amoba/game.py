import pygame
from grid import Grid

window = pygame.display.set_mode((500, 600))
pygame.display.set_caption("amőba")

pygame.font.init()
winner_font = pygame.font.SysFont("Comic Sans MS", 32)
restart_font = pygame.font.SysFont("Comic Sans MS", 18)

grid = Grid(pygame)
# grid.set_cell_value(0, 1, "X")
# grid.set_cell_value(1, 2, "O")
# grid.show_grid()  # print testing

running = True
letter = "X"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and grid.game_over:  # is true
                grid.clear_grid()
                grid.game_over = False
                grid.tie_game = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:  # not true
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[1] < 500:  # if inside game grid
                    x = mouse_pos[0] // 50
                    y = mouse_pos[1] // 50
                    print(mouse_pos)  # test
                    print(x, y)  # test
                    grid.mouse_click(x, y, letter)
                    if grid.switch_letter:  # if true
                        if letter == "X":
                            letter = "O"
                        else:
                            letter = "X"

    window.fill("lightblue3")

    grid.draw(window)

    if grid.game_over and not grid.tie_game:
        color = (0, 255, 0) if grid.winner_letter == "X" else (255, 0, 0)
        won_surface = winner_font.render(f"{grid.winner_letter} wins!", False, color)
        window.blit(won_surface, (50, 520))
        restart_surface = restart_font.render("Press Space to restart!", False, color)
        window.blit(restart_surface, (50, 550))
    if grid.tie_game:
        black = (0, 0, 0)
        tie_game_surface = winner_font.render("No winner!", False, black)
        window.blit(tie_game_surface, (50, 520))
        restart_surface = restart_font.render("Press Space to restart!", False, black)
        window.blit(restart_surface, (50, 550))

    points_surface = restart_font.render(f"(X) {grid.pointsX} - {grid.pointsO} (O)", False, (0, 0, 0))
    window.blit(points_surface, (350, 535))

    pygame.display.flip()
