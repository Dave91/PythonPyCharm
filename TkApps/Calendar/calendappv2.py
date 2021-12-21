import tkinter as tk
from tkcalendar import Calendar
from datetime import date, datetime
from calendar import TextCalendar


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(fill="both")

        # btn, lab, etc
        self.gotoday_btn = tk.Button(self, text="Go to Today", background="lightblue", command=self.go_today)
        self.addev_btn = tk.Button(self, text="Add Event", background="lightblue", command=self.add_event)
        self.dispcal = Calendar(self, selectmode="day")
        self.dispcal.bind("<Button-1>", self.color_date)
        self.labev = tk.Label(self, text="Upcoming Events:")
        self.dispnote = tk.Listbox(self, height=10, background="beige")
        self.statbar = tk.Label(self, text="ready")

        self.gotoday_btn.pack(fill="x", pady=5)
        self.addev_btn.pack(fill="x")
        self.dispcal.pack(fill="x", pady=5)
        self.labev.pack(anchor="w")
        self.dispnote.pack(fill="x", pady=5)
        self.statbar.pack(anchor="w")

        self.events = self.get_events()
        self.today = date.today()
        self.disp_notif()
        self.go_today()

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

    def go_today(self):
        self.dispcal.selection_set(self.today)

    def disp_notif(self):
        # self.dispnote.configure(state="normal")
        self.dispnote.delete(0, "end")
        for event in self.events:
            en = event[1]
            du = self.diff(event[0], self.today)  # .strip("days, 0:00:00")
            display = f"It's {du} days until: {en}!\n"
            self.dispnote.insert("end", display)
            # self.mark_event(event)
        # self.dispnote.configure(state="disabled")

    @staticmethod
    def diff(d1, d2):
        nod = str(d1 - d2).strip("days, 0:00:00")
        return nod

    def mark_event(self, d):
        # d = str(d[0])
        day = datetime.date(d)
        self.dispcal.tag_add("evn", 5.35)  # febr pl. 5.25 és 5.40 között kb itt keresse a napot: pl. "15", helye x, színezze x-től x+1ig
        self.dispcal.tag_configure("evn", underline=True, background="lightgrey")

    def add_event(self):
        # dselnew = str(self.dispcal.get_date()).split("/")  # in case of Calendar instead of TextCalendar
        # m, d, y = dselnew[0], dselnew[1], dselnew[2]
        # day = datetime.date(datetime(int(y), int(m), int(d)))
        # self.dispcal.calevent_create(day, "", tags="ev")
        # self.dispcal.tag_config("ev", font="bold")
        pass

    def color_date(self, event):
        # print(self.dispcal.index(f"@{event.x},{event.y}"), self.dispcal.index("current"))
        ind = float(self.dispcal.index("current"))
        if self.dispcal.get(ind).isnumeric() is False or self.dispcal.get(ind) == " ":
            pass
        else:
            indleft = ind - 0.1 if self.dispcal.get(ind - 0.1) != " " else ind
            indright = ind + 0.1 if self.dispcal.get(ind + 0.1) != " " else ind
            print(float(indleft), float(indright))
            self.dispcal.tag_add("evn", float(indleft), float(indright))
            self.dispcal.tag_configure("evn", underline=True, background="lightgrey")


if __name__ == "__main__":
    gui = tk.Tk()
    gui.config(background="beige")
    gui.title("My Event Calendar")
    gui.geometry("300x500")
    App(gui)
    gui.mainloop()
