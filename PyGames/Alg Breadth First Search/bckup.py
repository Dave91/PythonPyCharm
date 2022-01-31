import queue
import tkinter as tk
import time


class MainApp:
    def __init__(self):
        root = tk.Tk()

        # self.btn_map = tk.Button(root, text="load map", command=self.load_map)
        self.btn = tk.Button(root, text="find path", command=self.start_alg)
        self.lab = tk.Text(root)

        # self.btn_map.pack()
        self.btn.pack()
        self.lab.pack()
        self.maze = [["#", "#", "#", "#", "#", "O", "#", "#", "#"],
                     ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
                     ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
                     ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
                     ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
                     ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
                     ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
                     ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
                     ["#", "#", "#", "#", "#", "#", "#", "X", "#"]]

        self.mazeoutp = [["#", "#", "#", "#", "#", "O", "#", "#", "#"],
                         ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
                         ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
                         ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
                         ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
                         ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
                         ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
                         ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
                         ["#", "#", "#", "#", "#", "#", "#", "X", "#"]]

        self.start = 0
        self.opennode = []
        self.closednode = []
        self.path = ""

        root.mainloop()

    def start_alg(self):
        nums = queue.Queue()
        nums.put("")
        add = ""
        maze = self.maze
        for x, pos in enumerate(maze[0]):
            if pos == "O":
                self.start = x

        while not self.find_end(maze, add):
            add = nums.get()
            for j in ["L", "R", "U", "D"]:
                put = add + j
                if self.valid(maze, put):
                    nums.put(put)

    def print_maze(self, maze):
        i = self.start
        j = 0
        pos = set()
        for move in self.path:
            if move == "L":
                i -= 1

            elif move == "R":
                i += 1

            elif move == "U":
                j -= 1

            elif move == "D":
                j += 1
            pos.add((j, i))

        self.lab.delete(1.0, "end")
        for j, row in enumerate(maze):
            for i, col in enumerate(row):
                if (j, i) in pos:
                    self.mazeoutp[j][i] = "+"
                else:
                    self.mazeoutp[j][i] = col

        for j, row in enumerate(self.mazeoutp):
            self.lab.insert("end", "\n")
            for i, col in enumerate(row):
                self.lab.insert("end", col + " ")

        self.lab.update_idletasks()

    def valid(self, maze, moves):
        i = self.start
        j = 0
        for move in moves:
            if move == "L":
                i -= 1

            elif move == "R":
                i += 1

            elif move == "U":
                j -= 1

            elif move == "D":
                j += 1

            if not (0 <= i < len(maze[0]) and 0 <= j < len(maze)):
                return False
            elif maze[j][i] == "#":
                return False

        self.opennode.append([])
        return True

    def find_end(self, maze, moves):
        time.sleep(0.05)
        self.path = moves
        self.print_maze(maze)

        i = self.start
        j = 0
        for move in moves:
            if move == "L":
                i -= 1

            elif move == "R":
                i += 1

            elif move == "U":
                j -= 1

            elif move == "D":
                j += 1

        if maze[j][i] == "X":
            print("Found: " + moves)
            return True

        return False


if __name__ == "__main__":
    MainApp()
