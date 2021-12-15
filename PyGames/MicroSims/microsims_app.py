import random
import tkinter as tk
# import sys

import pygame
from pygame.locals import *

# dot collections
d1, d2, d3, d4 = [], [], [], []
dtotal = []


def init_dots():
    global dtotal, d1, d2, d3, d4
    dtotal = [d1, d2, d3, d4]
    for i in range(500):
        for k in range(4):
            dx = random.randint(0, 500)
            dy = random.randint(0, 500)
            new_dot = [dx, dy]
            dtotal[k].append(new_dot)


def place_dots(surf):
    dcol = {"0": (0, 0, 0), "1": (255, 0, 0), "2": (0, 255, 0), "3": (0, 0, 255)}
    init_dots()
    for i in range(4):
        for d in dtotal[i]:
            pygame.draw.line(surf, dcol[str(i)], d, d, 2)


def move_dots():
    global dtotal
    for i in range(4):
        for d in dtotal[i]:
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            d[0] += dx
            d[1] += dy


def draw(surf):
    surf.fill((255, 255, 255))  # bg
    dcol = {"0": (0, 0, 0), "1": (255, 0, 0), "2": (0, 255, 0), "3": (0, 0, 255)}
    for i in range(4):
        for d in dtotal[i]:
            pygame.draw.line(surf, dcol[str(i)], d, d, 2)

    pygame.display.flip()


def get_input():

    for event in pygame.event.get():
        if event.type == QUIT:
            return True
        if event.type == KEYDOWN:
            print(event)
        if event.type == MOUSEBUTTONDOWN:
            print(event)
        # sys.stdout.flush()  # get stuff to the console
    return False


done = False
dots_placed = False
speed = 5


def quit_callback():
    global done
    done = True


def apply_sets(fps_scale):
    global speed
    fps_val = fps_scale.get()
    speed = int(fps_val)


def main():
    global dots_placed
    # init pygame
    pygame.init()
    screen_size = (500, 500)
    surface = pygame.display.set_mode(screen_size)

    # place init_dots /once when init/
    if not dots_placed:
        place_dots(surface)
        dots_placed = True

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
    # tk.Label()
    # tk.Label()

    # main loop
    while not done:
        try:
            main_dialog.update()
        except:
            print("dialog error")

        if get_input():  # input event can also come from diaglog
            break
        move_dots()
        draw(surface)
        clock.tick(speed)  # slow it to something slightly realistic
        gameframe += 1

    main_dialog.destroy()


if __name__ == '__main__':
    main()
