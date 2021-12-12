
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
        return 0 <= x < 5 and 0 <= y < 5

    def check_grid(self, x, y, letter):
        count = 1
        for index, (dirx, diry) in enumerate(self.search_dirs):
            # print(dirx, diry)
            if self.is_within_bounds(x + dirx, y + diry) \
            and self.get_cell_value(x + dirx, y + diry) == letter:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.is_within_bounds(xx + dirx, yy + diry) \
                and self.get_cell_value(xx + dirx, yy + diry) == letter:
                    count += 1
                    if count == 5:
                        break
                if count < 5:
                    new_dir = 0
                    if index == 0:  # N to S
                        new_dir = self.search_dirs[4]
                    elif index == 1:  # NW to SE
                        new_dir = self.search_dirs[5]
                    elif index == 2:  # W to E
                        new_dir = self.search_dirs[6]
                    elif index == 3:  # SW to NE
                        new_dir = self.search_dirs[7]
                    elif index == 4:  # S to N
                        new_dir = self.search_dirs[0]
                    elif index == 5:  # SE to NW
                        new_dir = self.search_dirs[1]
                    elif index == 6:  # E to W
                        new_dir = self.search_dirs[2]
                    elif index == 7:  # NE to SW
                        new_dir = self.search_dirs[3]

                    if self.is_within_bounds(x + new_dir[0], y + new_dir[1]) \
                    and self.get_cell_value(x + new_dir[0], y + new_dir[1]) == letter:
                        count += 1
                        if count == 5:
                            break
                    else:
                        count = 1
        # win cond
        if count == 5:
            self.winner_letter = letter
            self.game_over = True
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
