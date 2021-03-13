import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import numpy as np


class MainFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side="top", expand=1, fill="both")

        # TOP
        self.top = ttk.Frame(self, borderwidth=10)
        self.top.pack(fill="x")

        self.bimg = tk.PhotoImage(file="icons/key-icon.png")
        ttk.Button(self.top, text="Generálj", command=self.newpwgen, compound="right", image=self.bimg).pack()
        self.pwgenres = tk.StringVar()
        self.pwgenres.set("##PASSWORD##")
        ttk.Entry(self.top, textvariable=self.pwgenres, width=20, justify="center", state="readonly").pack(pady=5)

        # MID
        self.mid = ttk.Frame(self, borderwidth=15)
        self.mid.pack(expand=1, fill="both")

        self.cnum = tk.IntVar()
        self.cnum.set(1)
        self.ckisb = tk.IntVar()
        self.ckisb.set(0)
        self.cnagyb = tk.IntVar()
        self.cnagyb.set(0)
        self.cspec = tk.IntVar()
        self.cspec.set(0)

        ttk.Checkbutton(self.mid, variable=self.cspec, text="Speciális ( -._ )").pack(side="bottom", pady=1)
        ttk.Checkbutton(self.mid, variable=self.cnagyb, text="Nagybetűk (AÁBC)").pack(side="bottom", pady=1)
        ttk.Checkbutton(self.mid, variable=self.ckisb, text="Kisbetűk (aábc)").pack(side="bottom", pady=1)
        ttk.Checkbutton(self.mid, variable=self.cnum, text="Számok (123)").pack(side="bottom", pady=1)
        ttk.Label(self.mid, text="Karakterhossz:").pack(side="left", pady=3)
        self.spinb = ttk.Spinbox(self.mid, from_=3, to=12, increment=1, width=4, justify="center", state="readonly")
        self.spinb.pack(side="right", pady=3)
        self.spinb.set(3)

        # BOTT
        self.bott = ttk.Frame(self, borderwidth=5)
        self.bott.pack(side="bottom", fill="x")

        # ttk.Label(self.bott, text="http://www.fatcow.com/free-icons", font=("Corbel", 7)).pack(side="bottom")
        self.metim1 = tk.PhotoImage(file="icons/key-p-icon.png").zoom(32).subsample(32)
        ttk.Label(self.bott, image=self.metim1).pack(side="left")
        self.metim2 = tk.PhotoImage(file="icons/key-a-icon.png").zoom(32).subsample(32)
        ttk.Label(self.bott, image=self.metim2).pack(side="left")
        self.metim3 = tk.PhotoImage(file="icons/key-s-icon.png").zoom(32).subsample(32)
        ttk.Label(self.bott, image=self.metim3).pack(side="left")
        self.metim4 = tk.PhotoImage(file="icons/key-s-icon.png").zoom(32).subsample(32)
        ttk.Label(self.bott, image=self.metim4).pack(side="left")
        self.metim5 = tk.PhotoImage(file="icons/key-w-icon.png").zoom(32).subsample(32)
        ttk.Label(self.bott, image=self.metim5).pack(side="left")
        self.metim6 = tk.PhotoImage(file="icons/key-o-icon.png").zoom(32).subsample(32)
        ttk.Label(self.bott, image=self.metim6).pack(side="left")
        self.metim7 = tk.PhotoImage(file="icons/key-r-icon.png").zoom(32).subsample(32)
        ttk.Label(self.bott, image=self.metim7).pack(side="left")
        self.metim8 = tk.PhotoImage(file="icons/key-d-icon.png").zoom(32).subsample(32)
        ttk.Label(self.bott, image=self.metim8).pack(side="left")

    def newpwgen(self):
        if self.cnum.get() == 0 and self.ckisb.get() == 0 and self.cnagyb.get() == 0 and self.cspec.get() == 0:
            messagebox.showwarning(None, "Legalább egy opció kiválasztandó!")

        lnum = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        lkisb = ["a", "á", "b", "c", "d", "e", "é", "f", "g", "h", "i", "í", "j", "k", "l", "m", "n", "o", "ó",
                 "ö", "ő", "p", "q", "r", "s", "t", "u", "ú", "ü", "ű", "v", "w", "x", "y", "z"]
        lnagyb = ["A", "Á", "B", "C", "D", "E", "É", "F", "G", "H", "I", "Í", "J", "K", "L", "M", "N", "O", "Ó",
                  "Ö", "Ő", "P", "Q", "R", "S", "T", "U", "Ú", "Ü", "Ű", "V", "W", "X", "Y", "Z"]
        lspec = ["-", ".", "_"]

        ranl = []
        rani = 0
        if self.cnum.get() == 1:
            ranl.extend(lnum)
            rani += len(lnum)
        if self.ckisb.get() == 1:
            ranl.extend(lkisb)
            rani += len(lkisb)
        if self.cnagyb.get() == 1:
            ranl.extend(lnagyb)
            rani += len(lnagyb)
        if self.cspec.get() == 1:
            ranl.extend(lspec)
            rani += len(lspec)

        pwgen = ""
        for i in range(int(self.spinb.get())):
            ranchar = ranl[np.random.randint(rani)]
            pwgen = pwgen + ranchar
            i += 1
        self.pwgenres.set(pwgen)
        self.copytoclipboard(pwgen)
        messagebox.showinfo(None, "Vágólapra másolva!")

    def copytoclipboard(self, pwgen):
        self.top.clipboard_clear()
        self.top.clipboard_append(pwgen)
        self.top.update()  # elvileg ettől vágólapon marad az ablak bezárása után is


class StyleConfig(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)

        # self.theme_use("classic")
        self.configure("TLabel", background="beige")
        self.configure("TEntry", foreground="blue", background="beige")
        self.configure("TButton", foreground="maroon", background="beige")
        self.configure("TFrame", background="beige", relief="groove")
        self.configure("TCheckbutton", background="beige")
        self.configure("TSpinbox", background="beige")


def main():
    root = tk.Tk()
    root.title("PassGen")
    appicon = tk.PhotoImage(file="icons/key-icon.png")
    root.iconphoto(False, appicon)
    root.geometry("170x260")
    root.resizable(0, 0)
    root.config(background="beige")
    StyleConfig()
    MainFrame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
