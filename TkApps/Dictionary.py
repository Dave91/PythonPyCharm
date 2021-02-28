import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import csv


class MainFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side="top", expand=1, fill="both")
        self.topf = ttk.Frame(self, borderwidth=10)
        self.topf.pack(side="top", expand=1, fill="both")
        self.midf = ttk.Frame(self)
        self.midf.pack(side="bottom", expand=1, fill="both")
        # MIDF
        self.scrbar = ttk.Scrollbar(self.midf, orient="vertical", command=self.onscrbar)
        self.txtang = tk.Text(self.midf, background="lightgrey", font=("Arial", 8), width=80, height=10,
                              relief="groove", borderwidth=1.5, yscrollcommand=self.scrbar.set)
        self.txthun = tk.Text(self.midf, background="lightgrey", font=("Arial", 8), width=80, height=10,
                              relief="groove", borderwidth=1.5, yscrollcommand=self.scrbar.set)
        self.txtang.configure(state="disabled")
        self.txthun.configure(state="disabled")
        self.scrbar.pack(side="right", expand=1, fill="both")
        self.txtang.pack(side="top", expand=1, fill="both")
        self.txthun.pack(side="bottom", expand=1, fill="both")
        self.txtang.bind("<MouseWheel>", self.onmousewheel)
        self.txthun.bind("<MouseWheel>", self.onmousewheel)
        # TOPF
        self.topf.grid_columnconfigure(4, weight=1)
        ttk.Label(self.topf, text="Keresés nyelve:").grid(row=1, column=1)
        self.kerlang = tk.StringVar()
        self.kerlang.set("ang")
        ttk.Radiobutton(self.topf, text="Angol", variable=self.kerlang, value="ang").grid(row=1, column=2, sticky="w")
        ttk.Radiobutton(self.topf, text="Magyar", variable=self.kerlang, value="hun").grid(row=1, column=2, sticky="e")

        ttk.Separator(self.topf, orient="horizontal").grid(row=2, columnspan=5, sticky="ew", pady=5)
        ttk.Label(self.topf, text="Keresés módja:").grid(row=3, column=1)
        self.kermod = tk.StringVar()
        self.kermod.set("a")
        ttk.Radiobutton(self.topf, text="Csak teljes egyezés", variable=self.kermod, value="a").grid(row=3, column=2,
                                                                                                     sticky="w")
        ttk.Radiobutton(self.topf, text="Ezzel kezdődjön", variable=self.kermod, value="b").grid(row=3, column=3,
                                                                                                 sticky="w")
        ttk.Radiobutton(self.topf, text="Bárhol szerepelhet", variable=self.kermod, value="c").grid(row=3, column=4,
                                                                                                    sticky="w")
        ttk.Separator(self.topf, orient="horizontal").grid(row=4, columnspan=5, sticky="ew", pady=5)

        ttk.Label(self.topf, text="Keresett szó:").grid(row=5, column=1, sticky="w")
        self.kerinput = tk.StringVar()
        self.kerinput.set("")
        self.kerent = ttk.Entry(self.topf, textvariable=self.kerinput, validate="key", width=20, justify="left")
        self.kerent["validatecommand"] = (self.kerent.register(self.inputvalid), "%P", "%d")
        self.kerent.grid(row=5, column=2, sticky="w")
        self.taln = tk.StringVar()
        ttk.Label(self.topf, textvariable=self.taln).grid(row=5, column=3, sticky="w")

    def inputvalid(self, instr, acttyp):
        if acttyp == "1":
            lang = {"ang": 0, "hun": 1}
            with open("data/szotarak/enhu.csv", encoding="ansi") as csvfile:
                csvolv = csv.reader(csvfile, delimiter=";")
                ossztal = 0
                self.txtang.configure(state="normal")
                self.txthun.configure(state="normal")
                self.txtang.delete(1.0, tk.END)
                self.txthun.delete(1.0, tk.END)
                if self.kermod.get() == "a":
                    for row in csvolv:
                        if str(row[lang[self.kerlang.get()]]) == instr:
                            self.taloutput(row)
                            ossztal += 1
                if self.kermod.get() == "b":
                    for row in csvolv:
                        if str(row[lang[self.kerlang.get()]]).find(instr) == 0:
                            self.taloutput(row)
                            ossztal += 1
                if self.kermod.get() == "c":
                    for row in csvolv:
                        if str(row[lang[self.kerlang.get()]]).find(instr) >= 0:
                            self.taloutput(row)
                            ossztal += 1
                self.txtang.configure(state="disabled")
                self.txthun.configure(state="disabled")
            if ossztal != 0:
                self.taln.set(str(ossztal) + " találat")
            else:
                self.taln.set("Nincs találat!")
                # return False
        return True

    def taloutput(self, row):
        taloutputang = row[0] + "\n"
        taloutputhun = row[1] + "\n"
        self.txtang.insert(tk.END, *taloutputang.splitlines(keepends=True))
        self.txthun.insert(tk.END, *taloutputhun.splitlines(keepends=True))

    def onscrbar(self):
        self.txtang.yview()
        self.txthun.yview()

    def onmousewheel(self, event):
        self.txtang.yview("scroll", event.delta, "units")
        self.txthun.yview("scroll", event.delta, "units")
        # dupla görgetés ellen, default bindings
        return "break"


class StyleConfig(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)

        # self.theme_use("classic")
        self.configure("TLabel", background="beige")
        self.configure("TEntry", foreground="blue", background="beige")
        self.configure("TFrame", background="beige", relief="groove")
        self.configure("TRadiobutton", background="beige")
        self.configure("TMenubutton", background="beige")


def main():
    # GUI ROOT WINDOW
    root = tk.Tk()
    root.title("Dictionary")
    appicon = tk.PhotoImage(file="icons/tools-gramm.png")
    root.iconphoto(False, appicon)
    root.geometry("500x420")
    root.resizable(0, 0)
    root.config(background="beige")
    StyleConfig()
    MainFrame(root)
    # gui handler
    root.mainloop()


if __name__ == "__main__":
    main()
