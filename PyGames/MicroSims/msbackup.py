import random
import tkinter as tk
from sys import exit

import pygame

# dot collections
dtotal = [[], [], [], []]
# dot params/timers
dot_act = [0, 0, 0, 0]
dot_life = [0, 0, 0, 0]
dot_rep = [0, 0, 0, 0]
dot_age = [[], [], [], []]


def init_dots():
    global dtotal, dot_age
    for i in range(20):
        for k in range(4):
            dx = random.randint(0, 500)
            dy = random.randint(0, 500)
            new_dot = [dx, dy]
            dtotal[k].append(new_dot)
            dot_age[k].append(0)


def dot_timers():
    global dot_act, dot_life, dot_rep, dot_age
    for i in range(4):
        dot_act[i] += 1
        dot_life[i] += 1
        dot_rep[i] += 1
        x = 0
        for d in dot_age[i]:
            dot_age[i][x] += 1
            x += 1


def outside_borders(d):
    if 0 > d[0] > 500 or 0 > d[1] > 500:
        return True
    else:
        return False


def move_dots():
    global dtotal
    for i in range(4):
        for d in dtotal[i]:
            dx = random.randint(-3, 3)
            dy = random.randint(-3, 3)
            try:
                d[0] += dx
                d[1] += dy
            except outside_borders(d):
                d[0] += dx * (-1)
                d[1] += dy * (-1)


def decay_reprod_dots():
    global dtotal, dot_life, dot_age
    dlife = {"0": 20, "1": 15, "2": 10, "3": 5}
    drep = {"0": random.randint(0, 5), "1": random.randint(0, 10),  # reprod rates
            "2": random.randint(0, 15), "3": random.randint(0, 20)}
    for i in range(4):
        try:
            if dot_life[i] > dlife[str(i)]:
                for x in range(random.randint(0, 20)):  # decay rate
                    dtotal[i].pop(0)
                    dot_age[i].pop(0)
                dot_life[i] = 0
        except IndexError:
            pass
            # died_out = i vagyis ehhez nincs több repr mozg v decay!!
        # next gen dots
        for k in range(drep[str(i)]):
            dx = random.randint(0, 500)
            dy = random.randint(0, 500)
            new_dot = [dx, dy]
            dtotal[i].append(new_dot)
            dot_age[i].append(0)


def draw(surf):
    surf.fill((255, 255, 255))  # bg
    dcol = {"0": (0, 0, 0), "1": (255, 0, 0), "2": (0, 255, 0), "3": (0, 0, 255)}
    for i in range(4):
        x = 0
        for d in dtotal[i]:
            size = (dot_age[i][x] // 50) + 1  # grow dots over time
            pygame.draw.line(surf, dcol[str(i)], d, d, size)
            x += 1

    pygame.display.flip()


def get_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            print(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
    return False


init_dots()
done = False
speed = 5


def quit_callback():
    global done
    done = True


def apply_sets(fps_scale):
    global speed
    fps_val = fps_scale.get()
    speed = int(fps_val)


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
    # init pygame
    pygame.init()
    screen_size = (500, 500)
    surface = pygame.display.set_mode(screen_size)

    # clock start, fps
    clock = pygame.time.Clock()
    gameframe = 0

    # init tkinter
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", quit_callback)
    main_dialog = tk.Frame(root, height=400, width=200, background="beige")
    main_dialog.pack()
    fps_scale = tk.Spinbox(main_dialog, from_=1, to=100, state="readonly")
    fps_scale.pack()
    apply_btn = tk.Button(main_dialog, text="Apply", command=lambda: apply_sets(fps_scale))
    apply_btn.pack()

    total_pop = tk.Label(main_dialog, text="Total Pop.:")
    d1_pop = tk.Label(main_dialog, text="Black Pop.:")
    d2_pop = tk.Label(main_dialog, text="Red Pop.:")
    d3_pop = tk.Label(main_dialog, text="Green Pop.:")
    d4_pop = tk.Label(main_dialog, text="Blue Pop.:")
    total_pop.pack()
    d1_pop.pack()
    d2_pop.pack()
    d3_pop.pack()
    d4_pop.pack()

    # main loop
    while not done:
        try:
            main_dialog.update()
        except:
            print("dialog error")

        if get_input():  # input event can also come from diaglog
            break
        dot_timers()
        move_dots()
        decay_reprod_dots()
        draw(surface)
        clock.tick(speed)  # slow it to something slightly realistic
        gameframe += 1
        count_pops(total_pop, d1_pop, d2_pop, d3_pop, d4_pop)

    main_dialog.destroy()
    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
