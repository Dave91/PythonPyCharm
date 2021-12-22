import tkinter as tk
from datetime import date
from tkinter import messagebox as msg, simpledialog as dia

from tkcalendar import Calendar


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(fill="both")
        gui.protocol("WM_DELETE_WINDOW", self.on_closing)

        # btn, lab, etc
        self.gotoday_btn = tk.Button(self, text="Show Today", background="lightblue", command=self.go_today)
        self.dispcal = Calendar(self, selectmode="day")
        self.addev_btn = tk.Button(self, text="Add Event", background="lightblue", command=self.add_event)
        self.delev_btn = tk.Button(self, text="Delete Event", background="lightblue", command=self.del_event)
        self.dispnote = tk.Listbox(self, height=12, background="beige", selectmode="single", activestyle="dotbox")
        self.dispnote.bind("<<ListboxSelect>>", self.mark_event)
        self.statbar = tk.Label(self, text="ready")

        self.gotoday_btn.pack(fill="x")
        self.dispcal.pack(fill="x", pady=4)
        self.addev_btn.pack(fill="x")
        self.delev_btn.pack(fill="x")
        self.dispnote.pack(fill="x", pady=4)
        self.statbar.pack(anchor="w")

        self.today = date.today()
        self.events = self.get_events(self.today)
        self.disp_notif()

    def get_events(self, tod):
        events_list = []
        try:
            with open("data/events.txt") as file:
                for line in file:
                    line = line.rstrip("\n")
                    col = line.split(";")
                    ed = col[0].split(".")
                    edy, edm, edd = int(ed[0]), int(ed[1]), int(ed[2])
                    du = self.diff(date(edy, edm, edd), date(tod.year, tod.month, tod.day))
                    events_list.append([du, col[1], col[0]])  # days until, event name, date
                    # print(du)
        except IOError:
            msg.showerror("Error", "File error")
        events_list.sort(key=self.ev_sort)
        # print(events_list)
        return events_list

    @staticmethod
    def diff(d1, d2):
        dd = str(d1 - d2).strip(", 0:00:00")
        return dd

    @staticmethod
    def ev_sort(x):
        return int(x[0].strip(" days"))

    def go_today(self):
        self.dispnote.selection_clear(0, "end")
        self.dispcal.selection_set(self.today)

    def disp_notif(self):
        self.dispnote.delete(0, "end")
        for event in self.events:
            du, en, ed = event[0], event[1], event[2]  # days until, event name, date
            display = f"{du} until: {en} ({ed})!"
            self.dispnote.insert("end", display)

    def mark_event(self, event):
        selid = int(event.widget.curselection()[0])
        selevd = self.events[selid][2].split(".")
        # print(selevd)
        sely, selm, seld = int(selevd[0]), int(selevd[1]), int(selevd[2])
        self.dispcal.selection_set(date(sely, selm, seld))
        # self.dispcal.tag_add("evn", 5.35)
        # self.dispcal.tag_configure("evn", underline=True, background="lightgrey")

    def add_event(self):
        tod = self.today
        if msg.askyesno("Selection", "Continue with selected day in calendar?"):
            dselnew = str(self.dispcal.get_date()).split("/")
            m, d, y = dselnew[0], dselnew[1], dselnew[2]
            ed = "20" + str(y) + "." + str(m) + "." + str(d)
            du = self.diff(date(int("20" + y), int(m), int(d)), date(tod.year, tod.month, tod.day))
            en = dia.askstring("Event Name", "Enter name for the event:", initialvalue="max. 25 chars")
            while self.inp_valid(en) is False:
                en = dia.askstring("Event Name", "Enter name for the event:", initialvalue="max. 25 chars")
            # print([du, en, ed])
            self.events.append([du, en, ed])
            self.save_events()
            self.get_events(tod)
            self.disp_notif()

        # self.dispcal.calevent_create(day, "", tags="ev")
        # self.dispcal.tag_config("ev", font="bold")

    @staticmethod
    def inp_valid(en):
        if len(en) < 2 or len(en) > 25 or en == "max. 25 chars" or en == "":
            return False
        else:
            return True

    def del_event(self):
        tod = self.today
        if msg.askyesno("Selection", "Are you sure to delete selected event in list?"):
            selid = int(self.dispnote.curselection()[0])
            self.events.pop(selid)
            # print(selid)
            self.save_events()
            self.get_events(tod)
            self.disp_notif()

    def save_events(self):
        try:
            with open("data/events.txt", "w") as file:
                file.writelines(str(event[2]) + ";" + str(event[1]) + "\n" for event in self.events)
        except IOError:
            msg.showerror("Error", "File error")

    def on_closing(self):
        if msg.askyesno("Quit", "Quit program?"):
            self.save_events()
            gui.destroy()


if __name__ == "__main__":
    gui = tk.Tk()
    gui.title("My Event Calendar")
    gui.geometry("300x500")
    App(gui)
    gui.mainloop()
