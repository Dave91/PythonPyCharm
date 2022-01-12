
class Grid:
    def __init__(self, pygame):
        self.grid = [[0 for x in range(10)] for y in range(10)]

        # line coords (line[0], line[1])
        self.grid_lines = [((0, 50), (500, 50)),  # 1. hori line
                           ((0, 100), (500, 100)),  # 2. hori line
                           ((0, 150), (500, 150)),
                           ((0, 200), (500, 200)),
                           ((0, 250), (500, 250)),
                           ((0, 300), (500, 300)),
                           ((0, 350), (500, 350)),
                           ((0, 400), (500, 400)),
                           ((0, 450), (500, 450)),
                           ((0, 500), (500, 500)),  # grid bot end line
                           ((50, 0), (50, 500)),  # 1. verti line
                           ((100, 0), (100, 500)),  # 2. verti line
                           ((150, 0), (150, 500)),
                           ((200, 0), (200, 500)),
                           ((250, 0), (250, 500)),
                           ((300, 0), (300, 500)),
                           ((350, 0), (350, 500)),
                           ((400, 0), (400, 500)),
                           ((450, 0), (450, 500))]

        self.pygame = pygame

        self.letterX = pygame.image.load("images/letter-x.png")
        self.letterO = pygame.image.load("images/letter-o.png")

        self.switch_letter = True

        # wind conds, search dirs as:
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0), (-1, 1),  # N,NW,W,SW
                            (0, 1), (1, 1), (1, 0), (1, -1)]  # S,SE,E,NE

        self.game_over = False
        self.winner_letter = ""
        self.pointsX = 0
        self.pointsO = 0
        self.tie_game = False

    def draw(self, win):
        for line in self.grid_lines:
            self.pygame.draw.line(win, (200, 200, 200), line[0], line[1], 2)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    win.blit(self.letterX, (x * 50, y * 50))
                elif self.get_cell_value(x, y) == "O":
                    win.blit(self.letterO, (x * 50, y * 50))

    # x és y ford mivel egér koord, utána y, x oszl, sor a gridben
    def get_cell_value(self, x, y):
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def mouse_click(self, x, y, letter):
        if self.get_cell_value(x, y) == 0:
            self.switch_letter = True
            self.set_cell_value(x, y, letter)
            self.check_grid(x, y, letter)
        else:
            self.switch_letter = False

    def clear_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                self.set_cell_value(x, y, 0)

    def is_grid_full(self):
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True

    def is_within_bounds(self, x, y):
        return 0 <= x < 10 and 0 <= y < 10  # grid row and col nums

    def win_cond_hori(self, y, letter):
        # hori: x 0-9 y val pl. 2 2 --> 0 2, 1 2, 2 2, 3 2, 4 2, 5 2, stb. x+1, y+0
        count = 0
        for i in range(10):
            if self.get_cell_value(i, y) == letter:
                count += 1
            else:
                count = 0
            if count == 5:
                return True
        return False

    def win_cond_verti(self, x, letter):
        # verti: x val y 0-9 pl. 2 2 --> 2 0, 2 1, 2 2, 2 3, 2 4, 2 5, stb. x+0, y+1
        count = 0
        for i in range(10):
            if self.get_cell_value(x, i) == letter:
                count += 1
            else:
                count = 0
            if count == 5:
                return True
        return False

    def win_cond_diag(self, x, y, letter):
        # right-to-down
        if y - x >= 0:
            y = y - x
            count = 0
            for i in range(10):
                if self.is_within_bounds(i, y + i) and self.get_cell_value(i, y + i) == letter:  # x=0
                    count += 1
                else:
                    count = 0
                if count == 5:
                    return True
        else:
            x = x - y
            count = 0
            for i in range(10):
                if self.is_within_bounds(x + i, i) and self.get_cell_value(x + i, i) == letter:  # y=0
                    count += 1
                else:
                    count = 0
                if count == 5:
                    return True

        # right-to-up
        count = 0
        for i in range(10):
            for d in range(10):
                if self.is_within_bounds(d, i - d) and self.get_cell_value(d, i - d) == letter:  # x=0
                    count += 1
                else:
                    count = 0
                if count == 5:
                    return True

        count = 0
        for i in range(10):
            for d in range(10):
                if self.is_within_bounds(i + d, 9 - d) and self.get_cell_value(i + d, 9 - d) == letter:  # y=9
                    count += 1
                else:
                    count = 0
                if count == 5:
                    return True

        # default and if none True
        return False

    def check_grid(self, x, y, letter):
        if self.win_cond_hori(y, letter) or self.win_cond_verti(x, letter) or self.win_cond_diag(x, y, letter):
            self.winner_letter = letter
            self.game_over = True
            if letter == "X":
                self.pointsX += 1
            else:
                self.pointsO += 1
        else:
            self.game_over = self.is_grid_full()
            if self.game_over:
                self.tie_game = True

    # for testing in console
    def show_grid(self):
        for row in self.grid:
            print(row)


if __name__ == "__main__":
    g = Grid()
    g.show_grid()
