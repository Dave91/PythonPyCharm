import tkinter as tk
import tkinter.ttk as ttk
# from tkinter import messagebox


class Top(ttk.Frame):
    def __init__(self):
        ttk.Frame.__init__(self)
        self.pack(side="top", expand=1, fill="x")


class Mid(ttk.Frame):
    def __init__(self):
        ttk.Frame.__init__(self)
        self.pack(expand=1, fill="both")

        self.leftcol = ttk.Frame(self)
        self.leftcol.pack(side="left", expand=1, fill="both")
        self.rightcol = ttk.Frame(self)
        self.rightcol.pack(side="right", expand=1, fill="both")


class Bott(ttk.Frame):
    def __init__(self):
        ttk.Frame.__init__(self)
        self.pack(side="bottom", expand=1, fill="x")

        self.metim1 = tk.PhotoImage(file="icons/meteo1sunny.png").zoom(25).subsample(32)
        ttk.Label(self, image=self.metim1).pack(side="left")


class StyleConfig(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)

        # style.theme_use("winnative")
        self.configure("TLabel", background="beige")
        self.configure("TEntry", foreground="blue")
        self.configure("TButton", foreground="maroon")
        self.configure("TFrame", background="beige")
        self.configure("TMenubutton", background="#D7DDDC", foreground="blue")


def main():
    # GUI ROOT WINDOW
    root = tk.Tk()
    root.title("MeteoLog")
    # appicon = tk.PhotoImage(file="icons/umbrella-icon-small.png")
    # root.iconphoto(False, appicon)
    root.geometry("400x400")
    root.resizable(0, 0)
    root.config(background="beige", cursor="cross")
    StyleConfig()
    Top()
    Mid()
    Bott()
    # gui handler
    root.mainloop()


if __name__ == "__main__":
    main()
