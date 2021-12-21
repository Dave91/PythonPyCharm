import tkinter as tk
from datetime import date, datetime
from calendar import TextCalendar
from tkinter import messagebox as msg, simpledialog as dia


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg="beige")
        self.pack(fill="both")

        # btn, lab, etc
        self.showupc_btn = tk.Button(self, text="Show Upcoming Events", command=self.disp_notif)
        self.showupc_btn.pack(pady=10, anchor="w")
        self.addev_btn = tk.Button(self, text="Add Event", command=self.add_event)
        self.addev_btn.pack(pady=4, anchor="w")
        self.dispcal = tk.Text(self, height=20, state="disabled", relief="groove")
        self.dispcal.bind("<Button-1>", self.color_date)
        self.dispcal.pack(fill="x", pady=4)
        self.dispnote = tk.Text(self, height=10, state="disabled", relief="groove")
        self.dispnote.pack(fill="x", pady=4)
        self.statbar = tk.Label(text="status")
        self.statbar.pack(anchor="w")

        self.events = self.get_events()
        self.today = date.today()

        year = self.today.year
        col = 6
        width = 2
        lines = 1
        space = 1

        self.caltxt = TextCalendar().formatyear(year, width, lines, space, col)
        self.dispcal.configure(state="normal")
        self.dispcal.insert("end", self.caltxt)
        self.dispcal.configure(state="disabled")

    @staticmethod
    def get_events():
        events_list = []
        with open("data/events.txt") as file:
            for line in file:
                line = line.rstrip("\n")
                col = line.split(";")
                ed = datetime.strptime(col[0], "%y/%m/%d").date()
                events_list.append([ed, col[1]])
        return events_list

    def disp_notif(self):
        self.dispnote.configure(state="normal")
        self.dispnote.delete(0.1, "end")
        for event in self.events:
            en = event[1]
            du = self.diff(event[0], self.today)  # .strip("days, 0:00:00")
            display = f"It is {du} days until {en}!\n"
            self.dispnote.insert("end", display)
            # self.mark_event(event)
        self.dispnote.configure(state="disabled")

    @staticmethod
    def diff(d1, d2):
        nod = str(d1 - d2).strip("days, 0:00:00")
        return nod

    def mark_event(self, d):
        # d = str(d[0])
        day = datetime.date(d)
        self.dispcal.tag_add("evn", 5.35)  # febr pl. 5.25 és 5.40 között kb itt keresse a napot: pl. "15", helye x, színezze x-től x+1ig
        self.dispcal.tag_configure("evn", underline=True, background="lightgrey")

    def add_event(self, ind):
        # dselnew = str(self.dispcal.get_date()).split("/")  # in case of Calendar instead of TextCalendar
        # m, d, y = dselnew[0], dselnew[1], dselnew[2]
        # day = datetime.date(datetime(int(y), int(m), int(d)))
        # self.dispcal.calevent_create(day, "", tags="ev")
        # self.dispcal.tag_config("ev", font="bold")
        print(ind.find("0."))
        if self.dispcal.get(ind).isnumeric() and self.dispcal.get(ind) != " " and float(ind) > 2.0:

            return True
        else:
            return False

    def color_date(self, event):
        # print(self.dispcal.index(f"@{event.x},{event.y}"), self.dispcal.index("current"))
        ind = self.dispcal.index("current")
        if self.add_event(ind):
            indleft, indright = f"{ind}", f"{ind} + 1 chars"
            if self.dispcal.get(f"{ind} - 1 chars").isnumeric():
                indleft = f"{ind} - 1 chars"
                indright = f"{ind} + 1 chars"
            if self.dispcal.get(f"{ind} + 1 chars").isnumeric():
                indright = f"{ind} + 2 chars"
                indleft = f"{ind}"
            # print(indleft, indright)
            self.dispcal.tag_add("evn", indleft, indright)
            self.dispcal.tag_configure("evn", underline=True, background="lightgrey")
        else:
            pass


if __name__ == "__main__":
    gui = tk.Tk()
    gui.config(background="beige")
    gui.title("My Event Calendar")
    gui.geometry("1050x600")
    App(gui)
    gui.mainloop()
