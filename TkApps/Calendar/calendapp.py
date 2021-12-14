import tkinter as tk
from tkcalendar import Calendar
from datetime import date, datetime


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(width=400, height=600, bg="beige")
        self.pack()

        self.calbg = Calendar(self, selectmode="day", year=2021, month=12, day=10)
        self.calbg.pack(pady=10)

        # btn, lab, etc
        self.showupc_btn = tk.Button(self, text="Show Upcoming Events")
        self.showupc_btn.pack(pady=10)
        self.addev_btn = tk.Button(self, text="Add Event")
        self.addev_btn.pack(pady=10)
        self.disptext = tk.Text(self)
        self.disptext.pack(pady=10)

        self.events = self.get_events()
        self.today = date.today()
        self.disp_notif()

    @staticmethod
    def get_events():
        events_list = []
        with open("data/events.txt") as file:
            for line in file:
                line = line.rstrip("\n")
                ce = line.split(";")
                ed = datetime.strptime(ce, "%y/%m/%d").date()
                ce[1] = ed
                events_list.append(ce)
            return events_list

    def disp_notif(self):
        for event in self.events:
            en = event[0]
            du = self.diff(event[1], self.today)
            display = f"It is {du} days until {en} !\n"
            self.disptext.insert(display, tk.END)

    @staticmethod
    def diff(d1, d2):
        tb = str(d1, d2)
        nod = tb.split(" ")
        return nod[0]

    def grad_date(self):
        dateselnew = self.calbg.get_date()


if __name__ == "__main__":
    gui = tk.Tk()
    gui.config(background="beige")
    gui.title("My Event Calendar")
    gui.geometry("400x600")
    App(gui)
    gui.mainloop()
