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
        self.lbtal = tk.Listbox(self.midf, height=20)
        self.lbtal.pack(side="left", expand=1, fill="both")
        # scrollbar??
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
        self.kermod.set("teljes")
        ttk.Radiobutton(self.topf, text="Csak teljes egyezés", variable=self.kermod, value="teljes").grid(
            row=3, column=2, sticky="w")
        ttk.Radiobutton(self.topf, text="Szó eleji egyezés", variable=self.kermod, value="eleje").grid(
            row=3, column=3, sticky="w")
        ttk.Radiobutton(self.topf, text="Bárhol szerepelhet", variable=self.kermod, value="mindegy").grid(
            row=3, column=4, sticky="w")
        ttk.Separator(self.topf, orient="horizontal").grid(row=4, columnspan=5, sticky="ew", pady=5)

        ttk.Label(self.topf, text="Keresett szó:").grid(row=5, column=1, sticky="w")
        self.kerinput = tk.StringVar()
        self.kerinput.set("")
        self.kerent = ttk.Entry(self.topf, textvariable=self.kerinput, validate="key", width=20, justify="left")
        self.kerent["validatecommand"] = (self.kerent.register(self.inputvalid), "%P", "%d")
        self.kerent.grid(row=5, column=2, sticky="w")
        self.taln = tk.StringVar()
        ttk.Label(self.topf, textvariable=self.taln).grid(row=5, column=3, sticky="w")

        # self.opendict()

    def opendict(self):
        if self.kerlang.get() == "ang":  # majd attól függően melyik nyelv kerül kiválasztásra, azt tölti be!!
            # self.tree.delete(*self.tree.get_children())
            # dict = angol: enhu... német: dehu --> (open(data/szotarak/ + dict[német] +.csv)
            ossztal = 0
            with open("data/szotarak/enhu.csv", encoding="ansi") as csvfile:
                csvolv = csv.reader(csvfile, delimiter=";")
                for row in csvolv:
                    self.lbtal.insert(ossztal + 1, row)
                    ossztal += 1
            if ossztal == 0:
                messagebox.showwarning(None, "Hiba: import sikertelen és/vagy üres állomány!")
        # else:
        #    messagebox.showerror(None, "Hiba: import sikertelen és/vagy üres állomány!")

    def inputvalid(self, instr, acttyp):
        if acttyp == "1":
            # if német akkor lang = {"ger": 0, ...}
            lang = {"ang": 0, "hun": 1}
            mod = {"teljes": "row[lang[self.kerlang.get()]] == instr",
                   "eleje": "row[lang[self.kerlang.get()]].find(instr) == 0",
                   "mindegy": "instr in row[lang[self.kerlang.get()]]"}
            szotal = 0
            with open("data/szotarak/enhu.csv", encoding="ansi") as csvfile:
                csvolv = csv.reader(csvfile, delimiter=";")
                self.lbtal.delete(1, "end")
                if self.kermod.get() == "teljes":
                    for row in csvolv:
                        if row[lang[self.kerlang.get()]] == instr:
                            self.lbtal.insert(szotal + 1, row[0] + "   -   " + row[1])
                            szotal += 1
                    return True
                if self.kermod.get() == "eleje":
                    for row in csvolv:
                        if row[lang[self.kerlang.get()]].find(instr) == 0:
                            self.lbtal.insert(szotal + 1, row[0] + "   -   " + row[1])
                            szotal += 1
                    return True
                if self.kermod.get() == "mindegy":
                    for row in csvolv:
                        if instr in row[lang[self.kerlang.get()]]:
                            self.lbtal.insert(szotal + 1, row[0] + "   -   " + row[1])
                            szotal += 1
                    return True
            # if szotal != 0:
        return True


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
    root.title("Dictionary - Szótár")
    appicon = tk.PhotoImage(file="icons/tools-gramm.png")
    root.iconphoto(False, appicon)
    root.geometry("540x420")
    root.resizable(0, 0)
    root.config(background="beige")
    StyleConfig()
    MainFrame(root)
    # gui handler
    root.mainloop()


if __name__ == "__main__":
    main()
