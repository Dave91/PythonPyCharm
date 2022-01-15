import random
import tkinter as tk
import tkinter.ttk as ttk


class App(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        # MENU ROW
        self.menu_frame = ttk.Frame(self, padding=4)
        self.menu_frame.pack(side="top", fill="x")

        self.lab_btn = tk.StringVar()
        self.lab_btn.set("Start game")
        reset_btn = ttk.Button(self.menu_frame, textvariable=self.lab_btn,
                               command=self.start_game)
        reset_btn.pack()

        # BTN GRID
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(fill="both")

        self.game_grid_val = [[0 for r in range(10)] for c in range(10)]
        self.game_grid = [[0 for r in range(10)] for c in range(10)]
        self.check_dir = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]]

        for row in range(10):
            for col in range(10):
                self.game_grid[row][col] = ttk.Button(
                    self.grid_frame, text="", width=1,
                    command=lambda r=row, c=col: self.btn_click(r, c))
                self.game_grid[row][col].grid(row=row, column=col)

        self.exp = ""
        self.input_text = tk.StringVar()

    def start_game(self):
        self.lab_btn.set("Restart")
        # timer start

        # option: num of mines (difficulty lvl)
        m_num = 10
        for m in range(m_num):
            m_row = random.randint(0, 9)
            m_col = random.randint(0, 9)
            self.game_grid_val[m_row][m_col] = "X"

        for r in range(10):
            for c in range(10):
                if self.game_grid_val[r][c] != "X":
                    m_near = 0
                    for d in range(8):
                        if 0 <= r + self.check_dir[d][0] <= 9 and 0 <= c + self.check_dir[d][1] <= 9:
                            if self.game_grid_val[r + self.check_dir[d][0]][c + self.check_dir[d][1]] == "X":
                                m_near += 1
                    self.game_grid_val[r][c] = m_near
        print(self.game_grid_val)

    def btn_click(self, r, c):
        print(self.game_grid_val)
        # jobb click csak megjelöl, val="?" style: pl más bg szín
        row, col = r, c
        if self.game_grid_val[row][col] == "X":
            self.game_grid[row][col]["text"] = "X"
            # GAME OVER
        else:
            self.game_grid[row][col]["text"] = str(self.game_grid_val[row][col])
            for d in range(8):
                if 0 <= row + self.check_dir[d][0] <= 9 and 0 <= col + self.check_dir[d][1] <= 9 \
                and self.game_grid_val[row + self.check_dir[d][0]][col + self.check_dir[d][1]] != "X":
                    self.game_grid[row + self.check_dir[d][0]][col + self.check_dir[d][1]]["text"] = str(
                        self.game_grid_val[row + self.check_dir[d][0]][col + self.check_dir[d][1]])
        # vmi
        print(self.game_grid_val)


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
