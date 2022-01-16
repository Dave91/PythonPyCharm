import random
import time
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
        diff_set = ttk.Spinbox(self.menu_frame, textvariable=self.diff, width=2, increment=1, from_=5, to=20)
        diff_set.grid(row=0, column=1, sticky="w")

        reset_btn = ttk.Button(self.menu_frame, text="New Game",
                               command=self.start_game)
        reset_btn.grid(row=0, column=2, sticky="w")

        self.time_start = ""
        self.time_end = ""

        # BTN GRID
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(fill="both")

        self.game_grid_val = [[0 for r in range(10)] for c in range(10)]
        self.game_grid = [[0 for r in range(10)] for c in range(10)]
        self.check_dir = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]]

        for row in range(10):
            for col in range(10):
                self.game_grid[row][col] = ttk.Button(
                    self.grid_frame, text="", width=1, state="disabled",
                    command=lambda r=row, c=col: self.btn_click(r, c))
                self.game_grid[row][col].grid(row=row, column=col)

    def start_game(self):
        self.time_start = time.time()
        m_num = self.diff.get()
        for m in range(m_num):
            m_row = random.randint(0, 9)
            m_col = random.randint(0, 9)
            self.game_grid_val[m_row][m_col] = "X"

        for r in range(10):
            for c in range(10):
                self.game_grid[r][c]["state"] = "normal"
                self.game_grid[r][c]["text"] = ""
                if self.game_grid_val[r][c] != "X":
                    m_near = 0
                    for d in range(8):
                        if 0 <= r + self.check_dir[d][0] <= 9 and 0 <= c + self.check_dir[d][1] <= 9:
                            if self.game_grid_val[r + self.check_dir[d][0]][c + self.check_dir[d][1]] == "X":
                                m_near += 1
                    self.game_grid_val[r][c] = m_near

    def win_cond(self):
        pass

    def btn_click(self, r, c):

        # jobb click csak megjelöl, val="?" style: pl más bg szín
        row, col = r, c
        if self.game_grid_val[row][col] == "X":  # GAME OVER
            self.game_grid[row][col]["text"] = "X"
            self.time_end = time.time()
            time_elap = round(float(self.time_end) - float(self.time_start))
            print(time_elap)
            msg.showinfo("Game over", "GAME OVER: STEPPED ON A MINE!")
        else:
            self.game_grid[row][col]["text"] = str(self.game_grid_val[row][col])
            self.game_grid[row][col]["state"] = "disabled"
            for d in range(8):
                if 0 <= row + self.check_dir[d][0] <= 9 and 0 <= col + self.check_dir[d][1] <= 9 \
                        and self.game_grid_val[row + self.check_dir[d][0]][col + self.check_dir[d][1]] != "X":
                    self.game_grid[row + self.check_dir[d][0]][col + self.check_dir[d][1]]["text"] = str(
                        self.game_grid_val[row + self.check_dir[d][0]][col + self.check_dir[d][1]])
                    self.game_grid[row + self.check_dir[d][0]][col + self.check_dir[d][1]]["state"] = "disabled"


class Styles(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.configure("TFrame", background="beige")
        self.configure("TButton", foreground="black", background="white", padding=10, cursor="hand1")
        self.map("TButton", foreground=[("active", "maroon")], background=[("active", "coral")])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mine Game")
    root.geometry("340x480")
    root.resizable(False, False)
    Styles()
    App(root)
    root.mainloop()
