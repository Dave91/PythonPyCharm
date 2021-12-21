import queue
import tkinter as tk


class MainApp(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # gui stuff
        # self.btn_map = tk.Button(root, text="load map", command=self.load_map)
        self.btn = tk.Button(root, text="find path", command=self.start_alg)
        self.lab = tk.Text(root)

        # self.btn_map.pack()
        self.btn.pack()
        self.lab.pack()

        # alg stuff
        self.maze = self.create_maze()
        self.nums = queue.Queue()
        self.nums.put("")
        self.add = ""
        self.moves = ["L", "R", "U", "D"]

    def start_alg(self):
        while not self.find_end():
            add = self.nums.get()
            for j in self.moves:
                put = add + j
                if self.valid(put):
                    self.nums.put(put)

    def create_maze(self):
        maze = []
        maze.append(["#", "#", "#", "#", "#", "O", "#", "#", "#"])
        maze.append(["#", " ", " ", " ", " ", " ", " ", " ", "#"])
        maze.append(["#", " ", "#", "#", " ", "#", "#", " ", "#"])
        maze.append(["#", " ", "#", " ", " ", " ", "#", " ", "#"])
        maze.append(["#", " ", "#", " ", "#", " ", "#", " ", "#"])
        maze.append(["#", " ", "#", " ", "#", " ", "#", " ", "#"])
        maze.append(["#", " ", "#", " ", "#", " ", "#", "#", "#"])
        maze.append(["#", " ", " ", " ", " ", " ", " ", " ", "#"])
        maze.append(["#", "#", "#", "#", "#", "#", "#", "X", "#"])

        for j, row in enumerate(maze):
            self.lab.insert("end", "\n")
            for i, col in enumerate(row):
                self.lab.insert("end", col)

        return maze

    def print_maze(self, path=""):
        for x, pos in enumerate(self.maze[0]):
            if pos == "O":
                start = x

        i = start
        j = 0
        pos = set()
        for move in path:
            if move == "L":
                i -= 1
            elif move == "R":
                i += 1
            elif move == "U":
                j -= 1
            elif move == "D":
                j += 1
            pos.add((j, i))

        for j, row in enumerate(self.maze):
            for i, col in enumerate(row):
                if (j, i) in pos:
                    self.maze[j][i] = "+ "
                else:
                    self.maze[j][i] = col + " "
            print()

    def valid(self, put):
        for x, pos in enumerate(self.maze[0]):
            if pos == "O":
                start = x

        i = start
        j = 0
        for move in self.moves:
            if move == "L":
                i -= 1
            elif move == "R":
                i += 1
            elif move == "U":
                j -= 1
            elif move == "D":
                j += 1

            if not (0 <= i < len(self.maze[0]) and 0 <= j < len(self.maze)):
                return False
            elif self.maze[j][i] == "#":
                return False

        return True

    def find_end(self):
        for x, pos in enumerate(self.maze[0]):
            if pos == "O":
                start = x

        i = start
        j = 0
        for move in self.moves:
            if move == "L":
                i -= 1
            elif move == "R":
                i += 1
            elif move == "U":
                j -= 1
            elif move == "D":
                j += 1
        if self.maze[j][i] == "X":
            print("Found: " + str(self.moves))
            self.print_maze()
            return True

        return False


if __name__ == "__main__":
    root = tk.Tk()
    MainApp(root)
    root.mainloop()
