import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as msg


class App(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        # MENU ROW
        self.menu_frame = ttk.Frame(self, padding=4)
        self.menu_frame.pack(side="top", fill="x")
        self.menu_frame.columnconfigure(0, weight=1)
        self.menu_frame.columnconfigure(1, weight=1)
        self.menu_frame.columnconfigure(2, weight=2)

        labd = ttk.Label(self.menu_frame, text="Mines:")
        labd.grid(row=0, column=0, sticky="e")

        self.diff = tk.IntVar()
        self.diff.set(10)
        diff_set = ttk.Spinbox(self.menu_frame, textvariable=self.diff, width=2, increment=5, from_=5, to=25)
        diff_set.grid(row=0, column=1, sticky="w")

        reset_btn = ttk.Button(self.menu_frame, text="New Game",
                               command=self.start_game)
        reset_btn.grid(row=0, column=2, sticky="w")

        # BTN GRID
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(fill="both")

        self.check_dir = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]]
        self.game_grid_val, self.game_grid = None, None
        self.reset_grid()
        self.playing = False
        msg.showinfo("Instructions", "LEFT click to search for mines \n"
                                     "RIGHT click to mark the spot of a possible mine \n"
                                     "Numbers indicate the amount of mines nearby")
        # in case of images not text vals
        self.img_m = tk.PhotoImage(file="mine12.png")
        self.img_f = tk.PhotoImage(file="flag12.png")

    def reset_grid(self):
        self.game_grid_val = [[0 for r in range(10)] for c in range(10)]
        self.game_grid = [[0 for r in range(10)] for c in range(10)]

        for row in range(10):
            for col in range(10):
                self.game_grid[row][col] = ttk.Button(
                    self.grid_frame, width=2, state="disabled")
                self.game_grid[row][col].grid(row=row, column=col)
                self.game_grid[row][col].bind("<Button>", lambda event, r=row, c=col: self.btn_click(event, r, c))

    def start_game(self):
        self.reset_grid()
        self.playing = True

        # GEN MINES
        for m in range(self.diff.get()):
            m_row = random.randint(0, 9)
            m_col = random.randint(0, 9)
            self.game_grid_val[m_row][m_col] = "X"

        # GEN INDICATOR NUMS
        for r in range(10):
            for c in range(10):
                self.game_grid[r][c]["state"] = "normal"
                if self.game_grid_val[r][c] != "X":
                    m_near = 0
                    for d in range(8):
                        if 0 <= r + self.check_dir[d][0] <= 9 and 0 <= c + self.check_dir[d][1] <= 9:
                            if self.game_grid_val[r + self.check_dir[d][0]][c + self.check_dir[d][1]] == "X":
                                m_near += 1
                    self.game_grid_val[r][c] = m_near

    def win_cond(self):
        mine, marked = 0, 0
        for r in range(10):
            for c in range(10):
                if self.game_grid_val[r][c] == "X":
                    mine += 1
                    if self.game_grid[r][c]["image"] == self.img_f:
                        marked += 1
        if marked == mine:  # --- GAME WIN ---
            self.playing = False
            msg.showinfo("Win", "YOU HAVE WON THIS GAME!")

    def btn_click(self, event, r, c):
        # self.win_cond()  # checking before or after func run
        ev_num, row, col = event.num, r, c
        if self.playing and self.game_grid[row][col]["state"] != r'disabled':
            if ev_num == 3:
                if self.game_grid[row][col]["image"] == "":
                    self.game_grid[row][col]["image"] = self.img_f
                else:
                    self.game_grid[row][col]["image"] = ""
            elif ev_num == 1:
                if self.game_grid_val[row][col] == "X":  # --- GAME OVER ---
                    self.game_grid[row][col]["image"] = self.img_m
                    self.playing = False
                    msg.showinfo("Game over", "GAME OVER: STEPPED ON A MINE!")
                    return
                else:
                    self.game_grid[row][col]["text"] = str(self.game_grid_val[row][col])
                    self.game_grid[row][col]["state"] = "disabled"
                    for d in range(8):
                        if 0 <= row + self.check_dir[d][0] <= 9 and 0 <= col + self.check_dir[d][1] <= 9 \
                        and self.game_grid_val[row + self.check_dir[d][0]][col + self.check_dir[d][1]] != "X":
                            self.game_grid[row + self.check_dir[d][0]][col + self.check_dir[d][1]]["text"] = str(
                                self.game_grid_val[row + self.check_dir[d][0]][col + self.check_dir[d][1]])
                            self.game_grid[row + self.check_dir[d][0]][col + self.check_dir[d][1]]["state"] = "disabled"
            else:
                return
            self.win_cond()  # check for winning conds


class Styles(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.configure("TFrame", background="beige")
        self.configure("TButton", foreground="black", background="white", padding=10)
        self.map("TButton", foreground=[("active", "maroon")], background=[("active", "coral")])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mine Game")
    root.geometry("400x480")  # btn width 1: 340x480, btn width 2: 400x480
    root.resizable(False, False)
    Styles()
    App(root)
    root.mainloop()
