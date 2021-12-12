import tkinter as tk
from tkcalendar import Calendar


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.calbg = Calendar(self, selectmode="day", year=2021, month=12, day=10)
        self.calbg.pack(pady=20)

        # btn, lab, etc
        tk.Button(self, text="Add Event")
        tk.Button(self, text="Get Date", command=self.grad_date).pack(pady=20)
        self.datesel = tk.Label(self, text="")
        self.datesel.pack(pady=20)

    def grad_date(self):
        dateselnew = self.calbg.get_date()
        self.datesel.config(text="Selected Date is: " + dateselnew)


if __name__ == "__main__":
    gui = tk.Tk()
    gui.config(background="beige")
    gui.title("CALENDAR")
    gui.geometry("400x400")
    App(gui)
    gui.mainloop()
