import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
# from tkinter import filedialog  # , simpledialog
# from os import curdir
import csv


class TabMenu(ttk.Notebook):
    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent)
        self.parent = parent
        self.pack(expand=1, fill="both")
        BottomBar().pack(side="bottom", expand=0, fill="x")

        TabNapiAlap(self)
        TabEvesReszl(self)
        TabTeszt(self)

        # sumrestxtbox
        self.sumrestxtbox = tk.Text(
            self, background="lightgrey", font=("Arial", 8), width=50, height=28, relief="groove",
            borderwidth=2.5,  # yscrollcommand=scrollbar.set
        )
        self.sumrestxtbox.configure(state="disabled")
        self.sumrestxtbox.lift()
        self.sumresonoff = tk.IntVar()
        self.sumresonoff.set(0)


class TabNapiAlap(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        parent.add(self, text="Napi alapadatok")

        self.toprow = ttk.Frame(self)
        self.toprow.pack(side="top", expand=1, fill="x")
        self.bottrow = ttk.Frame(self)
        self.bottrow.pack(side="bottom", expand=1, fill="x")
        self.leftcol = ttk.Frame(self)
        self.leftcol.pack(side="left", expand=1, fill="both")
        self.rightcol = ttk.Frame(self)
        self.rightcol.pack(side="right", expand=1, fill="both")

        # top row
        ttk.Label(self.toprow, text="(Budapest, Debrecen, Keszthely, Szombathely)").pack()
        ttk.Label(self.toprow, text="(1901.01.01 - 2019.12.31)").pack()

        self.optmenu = tk.StringVar()
        ttk.OptionMenu(
            self.toprow, self.optmenu, "<állomáshely>", "Budapest", "Debrecen", "Keszthely", "Szombathely"
        ).pack(side="left", padx=4)

        self.evkerinput = tk.StringVar()
        self.evkerinput.set("ÉÉÉÉ")
        self.yearent = ttk.Entry(self.toprow, textvariable=self.evkerinput, validate="key",
                                 width=5, justify="center")
        self.yearent["validatecommand"] = (self.yearent.register(self.yearentvalid), "%P", "%d")
        self.yearent.pack(side="left")

        self.honapkerinput = tk.StringVar()
        self.honapkerinput.set("HH")
        self.monthent = ttk.Entry(self.toprow, textvariable=self.honapkerinput, validate="key",
                                  width=3, justify="center")
        self.monthent["validatecommand"] = (self.monthent.register(self.mmentvalid), "%P", "%d")
        self.monthent.pack(side="left")

        self.napkerinput = tk.StringVar()
        self.napkerinput.set("NN")
        self.dayent = ttk.Entry(self.toprow, textvariable=self.napkerinput, validate="key",
                                width=3, justify="center")
        self.dayent["validatecommand"] = (self.dayent.register(self.ddentvalid), "%P", "%d")
        self.dayent.pack(side="left")

        ttk.Button(
            self.toprow, text="Keresés", command=lambda: self.searchdata(parent)
        ).pack(side="left", padx=2)

        # left & right cols
        ttk.Label(self.leftcol, text="idő\tr\ttn\tt\ttx").pack(side="top")
        ttk.Label(self.rightcol).pack(side="top")

        self.scrollbar = ttk.Scrollbar(self.rightcol)
        self.scrollbar.pack(side="right", expand=1, fill="both")
        self.txtbox = tk.Text(
            self.leftcol, background="lightgrey", font=("Arial", 8), width=45, height=20, relief="groove",
            borderwidth=1.5, yscrollcommand=self.scrollbar.set
        )
        self.txtbox.configure(state="disabled")
        self.txtbox.pack(side="left", expand=1, fill="both")
        self.scrollbar.config(command=self.txtbox.yview)

        # bottom row
        self.sumbuttlab = tk.StringVar()
        self.sumbuttlab.set("Összesít")
        ttk.Button(
            self.bottrow, textvariable=self.sumbuttlab, command=lambda: self.sumdatares(parent)
        ).pack(anchor="center")

    def searchdata(self, parent):
        if self.evkerinput.get().isnumeric() or (
                self.evkerinput.get().isnumeric() and self.honapkerinput.get().isnumeric()
        ) or (
                self.evkerinput.get().isnumeric() and self.honapkerinput.get().isnumeric() and
                self.napkerinput.get().isnumeric()):
            if str(self.optmenu.get()) != "<állomáshely>":
                evker = str(self.evkerinput.get())
                if self.honapkerinput.get().isnumeric() and len(self.honapkerinput.get()) == 1:
                    honapker = "0" + str(self.honapkerinput.get())
                elif self.honapkerinput.get().isnumeric() and len(self.honapkerinput.get()) == 2:
                    honapker = str(self.honapkerinput.get())
                else:
                    honapker = ""
                if self.napkerinput.get().isnumeric() and len(self.napkerinput.get()) == 1:
                    napker = "0" + str(self.napkerinput.get())
                elif self.napkerinput.get().isnumeric() and len(self.napkerinput.get()) == 2:
                    napker = str(self.napkerinput.get())
                else:
                    napker = ""
                kerinput = evker + honapker + napker
                helyker = "data/" + str(self.optmenu.get()) + "_19012019.csv"
                with open(helyker) as csvfile:
                    csvolv = csv.reader(csvfile, delimiter=';')
                    self.txtbox.configure(state="normal")
                    self.txtbox.delete(1.0, tk.END)
                    ossznap = 0
                    esonap = 0
                    osszcsapm = 0.0
                    sumtn = 0.0
                    sumt = 0.0
                    sumtx = 0.0
                    mintnap = 0
                    abstn = 30.0
                    abstx = -10.0
                    for row in csvolv:
                        if str(row[0]).find(kerinput) == 0:
                            napialapoutput = "\t".join(row) + "\n"
                            self.txtbox.insert(tk.END, *napialapoutput.splitlines(keepends=True))
                            ossznap += 1
                            if float(row[1]) > 0.0:
                                esonap += 1
                            osszcsapm += float(row[1])
                            sumtn += float(row[2])
                            sumt += float(row[3])
                            sumtx += float(row[4])
                            if float(row[3]) < 0.0:
                                mintnap += 1
                            if float(row[2]) < abstn:
                                abstn = float(row[2])
                            if float(row[4]) > abstx:
                                abstx = float(row[4])
                    self.txtbox.configure(state="disabled")
                    if ossznap == 0:
                        messagebox.showwarning(None, "Hiba: A keresés eredménytelen volt!")
                    else:
                        parent.sumrestxtbox.configure(state="normal")
                        parent.sumrestxtbox.delete(1.0, tk.END)
                        esoosszrat = float(format(esonap / ossznap, "10.1f"))
                        csapmatl = format(osszcsapm / float(esonap), "10.1f")
                        tnatl = format(sumtn / float(ossznap), "10.1f")
                        tatl = format(sumt / float(ossznap), "10.1f")
                        txatl = format(sumtx / float(ossznap), "10.1f")
                        parent.sumrestxtbox.insert(
                            tk.END, "Napok összesen:\t" + str(ossznap)
                                    + "\nEbből csapadékos:\t" + str(esonap)
                                    + "\nArányuk:\t" + str(esoosszrat)
                                    + "\n\nÖsszes csapadékm.:\t" + str(format(osszcsapm, "10.1f"))
                                    + "\nÁtl. (napi) csapadékm.:\t" + str(csapmatl)
                                    + "\n\nNapi min. hőm. átlaga:\t" + str(tnatl)
                                    + "\nNapi átl. hőm. átlaga:\t" + str(tatl)
                                    + "\nNapi max. hőm. átlaga:\t" + str(txatl)
                                    + "\nNegatív középhőm. napok:\t" + str(mintnap)
                                    + "\n\nAbsz. napi min. hőm.:\t" + str(abstn)
                                    + "\nAbsz. napi max. hőm.:\t" + str(abstx)
                        )
                        parent.sumrestxtbox.configure(state="disabled")
                    #    messagebox.showinfo(None, "Talált rekordok száma: " + str(ossznap))
            else:
                messagebox.showerror(None, "Nem megfelelő input!! \n(Kötelező: Állomáshely kiválasztása!)")
        else:
            messagebox.showerror(None, "Nem megfelelő input!! \n(Megfelelő: Év, Év + Hónap, Év + Hónap + Nap)")

    @staticmethod
    def yearentvalid(instr, acttyp):
        if acttyp == '1':
            if not instr.isdigit() or len(instr) > 4:
                return False
            elif len(instr) == 1 and int(instr) not in range(1, 3):
                return False
            elif len(instr) == 2 and int(instr) not in range(19, 21):
                return False
            elif len(instr) == 3 and int(instr) not in range(190, 202):
                return False
            elif len(instr) == 4 and int(instr) not in range(1901, 2020):
                return False
        return True

    @staticmethod
    def mmentvalid(instr, acttyp):
        if acttyp == '1':
            if not instr.isdigit() or len(instr) > 2 or int(instr) not in range(1, 13):
                return False
        return True

    @staticmethod
    def ddentvalid(instr, acttyp):
        if acttyp == '1':
            if not instr.isdigit() or len(instr) > 2 or int(instr) not in range(1, 32):
                return False
        return True

    def sumdatares(self, parent):
        self.txtbox.configure(state="normal")
        if len(self.txtbox.get(1.0, tk.END)) <= 5 or (
                self.evkerinput.get().isnumeric() and self.honapkerinput.get().isnumeric() and
                self.napkerinput.get().isnumeric()
        ):
            self.txtbox.configure(state="disabled")
            messagebox.showwarning(None, "Hiányzó vagy nem elegendő adatsorok!!")
        else:
            if parent.sumresonoff.get() == 0:
                parent.sumrestxtbox.pack()
                self.sumbuttlab.set("Vissza")
                parent.sumresonoff.set(1)
            else:
                parent.sumrestxtbox.forget()
                self.sumbuttlab.set("Összesít")
                parent.sumresonoff.set(0)


class TabEvesReszl(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        parent.add(self, text="Éves részletes")
        # éves/havi/napi lenyíló menüvel (mint napinál Bp, Khely, Szhely)!!
        # külön fülek: ??
        # százéves összesített
        # abszolút rekordok

        # block control
        self.toprow = ttk.Frame(self)
        self.toprow.pack(side="top", expand=1, fill="x")
        self.bottrow = ttk.Frame(self)
        self.bottrow.pack(side="bottom", expand=1, fill="x")
        self.leftcol = ttk.Frame(self)
        self.leftcol.pack(side="left", expand=1, fill="both")
        self.rightcol = ttk.Frame(self)
        self.rightcol.pack(side="right", expand=1, fill="both")

        # top row
        ttk.Label(self.toprow, text="(Debrecen)").pack()
        ttk.Label(self.toprow, text="(1901 - 2010)").pack()

        self.optmenu = tk.StringVar()
        ttk.OptionMenu(
            self.toprow, self.optmenu, "<állomáshely>", "éves", "havi"
        ).pack(side="left", padx=4)

        self.evkerinput = tk.StringVar()
        self.evkerinput.set("ÉÉÉÉ")
        self.yearent = ttk.Entry(self.toprow, textvariable=self.evkerinput, validate="key",
                                 width=5, justify="center")
        self.yearent["validatecommand"] = (self.yearent.register(self.yearentvalid), "%P", "%d")
        self.yearent.pack(side="left", padx=2)

        ttk.Button(self.toprow, text="Keresés", command=lambda: self.searchdata()).pack(side="right", padx=4)

        # left & right cols
        ttk.Label(self.leftcol, text="idő\tr\ttn\tt\ttx").pack(side="top")
        ttk.Label(self.rightcol).pack(side="top")

        self.scrollbar = ttk.Scrollbar(self.rightcol)
        self.scrollbar.pack(side="right", expand=1, fill="both")
        self.txtbox = tk.Text(
            self.leftcol, background="lightgrey", font=("Arial", 8), width=45, height=20, relief="groove",
            borderwidth=1.5, yscrollcommand=self.scrollbar.set
        )
        self.txtbox.configure(state="disabled")
        self.txtbox.pack(side="left", expand=1, fill="both")
        self.scrollbar.config(command=self.txtbox.yview)

        # bottom row
        ttk.Label(self.bottrow).pack()

    def searchdata(self):
        if self.evkerinput.get().isnumeric():
            if str(self.optmenu.get()) != "<állomáshely>":
                evker = str(self.evkerinput.get())
                helyker = "data/" + str(self.optmenu.get()) + "_19012019.csv"
                with open(helyker) as csvfile:
                    csvolv = csv.reader(csvfile, delimiter=';')
                    self.txtbox.configure(state="normal")
                    self.txtbox.delete(1.0, tk.END)
                    evtal = 0
                    for row in csvolv:
                        if evker in str(row[0]):
                            napialapoutput = "\t".join(row) + "\n"
                            self.txtbox.insert(tk.END, *napialapoutput.splitlines(keepends=True))
                            evtal += 1
                    self.txtbox.configure(state="disabled")
                    if evtal == 0:
                        messagebox.showwarning(None, "Hiba: A keresés eredménytelen volt!")
            else:
                messagebox.showerror(None, "Nem megfelelő input!! \n(Kötelező: Állomáshely kiválasztása!)")
        else:
            messagebox.showerror(None, "Nem megfelelő input!! \n(Megfelelő: Év, Év + Hónap, Év + Hónap + Nap)")

    @staticmethod
    def yearentvalid(instr, acttyp):
        if acttyp == '1':
            if not instr.isdigit() or len(instr) > 4:
                return False
            elif len(instr) == 1 and int(instr) not in range(1, 3):
                return False
            elif len(instr) == 2 and int(instr) not in range(19, 21):
                return False
            elif len(instr) == 3 and int(instr) not in range(190, 202):
                return False
            elif len(instr) == 4 and int(instr) not in range(1901, 2011):
                return False
        return True


class TabTeszt(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        parent.add(self, text="tesztfül")

        # diagram?? v inkább vmi treeview!! az szűrhető?? átlagok számítása, stb!

        ttk.Label(self).pack()


class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.parent = parent

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label='Fájl', menu=menu_file)
        # menu_file.add_command(label='Létrehoz', command=None)
        menu_file.add_command(label='Import', command=None)
        menu_file.add_command(label='Export', command=None)
        menu_file.add_separator()
        menu_file.add_command(label='Kilépés', command=parent.destroy)

        menu_options = tk.Menu(self, tearoff=0)
        self.add_cascade(label='Opciók', menu=menu_options)
        menu_options.add_command(label='Beállítások', command=None)

        menu_help = tk.Menu(self, tearoff=0)
        self.add_cascade(label='Súgó', menu=menu_help)
        menu_help.add_command(label='Névjegy', command=None)

        parent.config(menu=self)


class BottomBar(ttk.Frame):
    def __init__(self):
        ttk.Frame.__init__(self)

        self.metim1 = tk.PhotoImage(file="icons/meteo1sunny.png").zoom(25).subsample(32)
        ttk.Label(self, image=self.metim1).pack(side="left")
        self.metim2 = tk.PhotoImage(file="icons/meteo2cloudy-partly.png").zoom(25).subsample(32)
        ttk.Label(self, image=self.metim2).pack(side="left", padx=5)
        self.metim3 = tk.PhotoImage(file="icons/meteo3cloudy.png").zoom(25).subsample(32)
        ttk.Label(self, image=self.metim3).pack(side="left")
        self.metim4 = tk.PhotoImage(file="icons/meteo4thunder-lightning-storm.png").zoom(25).subsample(32)
        ttk.Label(self, image=self.metim4).pack(side="left", padx=5)
        self.metim5 = tk.PhotoImage(file="icons/meteo5rain.png").zoom(25).subsample(32)
        ttk.Label(self, image=self.metim5).pack(side="left")


class StyleConfig(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)

        # style.theme_use("winnative")
        self.configure("TLabel", background="beige")
        self.configure("TEntry", foreground="blue")
        self.configure("TButton", foreground="maroon")
        self.configure("TNotebook", background="#DAF7A6")
        self.configure("TNotebook.Tab", foreground="blue", padding=(10, 2, 10, 2))
        self.configure("TFrame", background="beige")
        self.configure("TMenubutton", background="#D7DDDC", foreground="blue")
        self.configure("TScrollbar", background="beige")


def main():
    # GUI ROOT WINDOW
    root = tk.Tk()
    root.title("MeteoLog")
    appicon = tk.PhotoImage(file="icons/umbrella-icon-small.png")
    root.iconphoto(False, appicon)
    root.geometry("300x500")
    root.resizable(0, 0)
    root.config(background="beige", cursor="cross")
    StyleConfig()
    MenuBar(root)
    TabMenu(root)
    # gui handler
    root.mainloop()


if __name__ == "__main__":
    main()
