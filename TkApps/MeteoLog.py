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
                helyker = "data/napialap/" + str(self.optmenu.get()) + "_19012019.csv"
                with open(helyker) as csvfile:
                    csvolv = csv.reader(csvfile, delimiter=';')
                    self.txtbox.configure(state="normal")
                    self.txtbox.delete(1.0, tk.END)
                    ossznap, esonap, mintnap = 0, 0, 0
                    osszcsapm, sumtn, sumt, sumtx = 0.0, 0.0, 0.0, 0.0
                    abstn, abstx = 30.0, -10.0
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

        # block control
        self.toprow = ttk.Frame(self)
        self.toprow.pack(side="top", expand=1, fill="x")
        self.bottrow = ttk.Frame(self)
        self.bottrow.pack(side="bottom", expand=1, fill="both")

        # top row
        ttk.Label(self.toprow, text="(Debrecen)").pack()
        ttk.Label(self.toprow, text="(1901 - 2010)").pack()

        self.optmenu = tk.StringVar()
        ttk.OptionMenu(
            self.toprow, self.optmenu, "<keresett tényező>", "csap.össz.", "naps. órák", "átlaghőm."
        ).pack(side="left", padx=2)

        self.evkerinput = tk.StringVar()
        self.evkerinput.set("ÉÉÉÉ")
        self.yearent = ttk.Entry(self.toprow, textvariable=self.evkerinput, validate="key",
                                 width=5, justify="center")
        self.yearent["validatecommand"] = (self.yearent.register(self.yearentvalid), "%P", "%d")
        self.yearent.pack(side="left", padx=2)

        ttk.Button(self.toprow, text="Keresés", command=lambda: self.searchdata()).pack(side="left", padx=2)

        # bottom row
        self.tree = ttk.Treeview(self.bottrow, columns=('Évszám', 'Érték'), height=15)
        self.tree.column('#0', width=110, stretch=tk.YES)
        self.tree.column('#1', width=85, stretch=tk.YES)
        self.tree.column('#2', width=95, stretch=tk.YES)
        self.tree.heading('#0', text='Tényező')
        self.tree.heading('#1', text='Évszám')
        self.tree.heading('#2', text='Érték')
        self.tree.pack(side="bottom")

        self.id, self.iid = 0, 2

    def searchdata(self):
        if self.evkerinput.get().isnumeric():
            for item in self.tree.get_children():
                self.tree.delete(item)
            # vagy egy sorban.. self.tree.delete(*self.tree.get_children())
            rtip = {
                0: "#ev", 1: "y_rs", 2: "y_rsh", 3: "y_rx", 4: "y_rxd", 5: "y_dr01", 6: "y_dr1", 7: "y_dr5",
                8: "y_dr10", 9: "y_dr20", 10: "y_dr30", 11: "y_dr50", 12: "y_drho", 13: "y_drjeg", 14: "y_drziv",
                15: "y_dron"
            }
            stip = {0: "#ev", 1: "y_ss", 2: "y_sx", 3: "y_sxd", 4: "y_dsf20", 5: "y_dsf80"}
            tatip = {0: "#ev", 1: "y_ta", 2: "y_tax", 3: "y_taxd", 4: "y_tan", 5: "y_tand"}
            tenyezo = str(self.optmenu.get())
            evker = str(self.evkerinput.get())
            idotal = 0
            if tenyezo == "csap.össz.":
                rfold = self.tree.insert("", 1, 1, text=tenyezo)
                with open("data/evesreszl/DE_Y_r.txt") as csvfile:
                    csvolv = csv.reader(csvfile, delimiter=';')
                    for row in csvolv:
                        if evker in str(row[0]):
                            for i, v in enumerate(row):
                                self.tree.insert(
                                    rfold, self.id, self.iid, text="",
                                    values=(rtip[i], v)
                                )
                                self.iid += 1
                                self.id += 1
                            idotal += 1
            elif tenyezo == "naps. órák":
                sfold = self.tree.insert("", 1, 1, text=tenyezo)
                with open("data/evesreszl/DE_Y_s.txt") as csvfile:
                    csvolv = csv.reader(csvfile, delimiter=';')
                    for row in csvolv:
                        if evker in str(row[0]):
                            for i, v in enumerate(row):
                                self.tree.insert(
                                    sfold, self.id, self.iid, text="",
                                    values=(stip[i], v)
                                )
                                self.iid += 1
                                self.id += 1
                            idotal += 1
            elif tenyezo == "átlaghőm.":
                tafold = self.tree.insert("", 1, 1, text=tenyezo)
                with open("data/evesreszl/DE_Y_ta.txt") as csvfile:
                    csvolv = csv.reader(csvfile, delimiter=';')
                    for row in csvolv:
                        if evker in str(row[0]):
                            for i, v in enumerate(row):
                                self.tree.insert(
                                    tafold, self.id, self.iid, text="",
                                    values=(tatip[i], v)
                                )
                                self.iid += 1
                                self.id += 1
                            idotal += 1
            else:
                messagebox.showerror(None, "Hiányzó vagy nem megfelelő input!!")
            if idotal == 0:
                messagebox.showwarning(None, "Hiba: A keresés eredménytelen volt!")
        else:
            messagebox.showerror(None, "Hiányzó vagy nem megfelelő input!!")

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

    @staticmethod
    def mmentvalid(instr, acttyp):
        if acttyp == '1':
            if not instr.isdigit() or len(instr) > 2 or int(instr) not in range(1, 13):
                return False
        return True


class TabTeszt(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        parent.add(self, text="tesztfül")

        # block control
        self.toprow = ttk.Frame(self)
        self.toprow.pack(side="top", expand=1, fill="x")
        self.bottrow = ttk.Frame(self)
        self.bottrow.pack(side="bottom", expand=1, fill="both")

        # top row
        ttk.Label(self.toprow, text="(Debrecen)").pack()
        ttk.Label(self.toprow, text="(1901.01 - 2010.12)").pack()

        self.optmenu = tk.StringVar()
        ttk.OptionMenu(
            self.toprow, self.optmenu, "<keresett tényező>", "csapadékösszeg", "napsütéses órák", "átl. hőmérséklet"
        ).pack(side="left", padx=2)

        self.evkerinput = tk.StringVar()
        self.evkerinput.set("ÉÉÉÉ")
        self.yearent = ttk.Entry(self.toprow, textvariable=self.evkerinput, validate="key",
                                 width=5, justify="center")
        self.yearent["validatecommand"] = (self.yearent.register(self.yearentvalid), "%P", "%d")
        self.yearent.pack(side="left", padx=2)

        self.honapkerinput = tk.StringVar()
        self.honapkerinput.set("HH")
        self.monthent = ttk.Entry(self.toprow, textvariable=self.honapkerinput, validate="key",
                                  width=3, justify="center")
        self.monthent["validatecommand"] = (self.monthent.register(self.mmentvalid), "%P", "%d")
        self.monthent.pack(side="left")

        ttk.Button(self.toprow, text="Keresés", command=lambda: self.searchdata()).pack(side="left", padx=2)

        # bottom row
        self.tree = ttk.Treeview(self.bottrow, columns=('Érték', 'Magyarázat'), height=15)
        self.tree.column('#0', width=100, stretch=tk.YES)
        self.tree.column('#1', width=90, stretch=tk.YES)
        self.tree.column('#2', width=100, stretch=tk.YES)
        self.tree.heading('#0', text='Adattípus')
        self.tree.heading('#1', text='Érték.')
        self.tree.heading('#2', text='Magyarázat')
        self.tree.pack(side="bottom")

        self.rfold = self.tree.insert("", 1, 1, text="csap.össz.")
        self.tree.insert("", 2, 2, text="naps. órák")
        self.tree.insert("", 3, 3, text="átl. hőm.")

        self.id, self.iid = 0, 4

    def searchdata(self):
        if self.evkerinput.get().isnumeric() or (
                self.evkerinput.get().isnumeric() and self.honapkerinput.get().isnumeric()
        ):
            if str(self.optmenu.get()) != "<keresett tényező>":
                evker = str(self.evkerinput.get())
                honapker, idoszak = "", "Y_"
                if self.honapkerinput.get().isnumeric() and len(self.honapkerinput.get()) == 1:
                    honapker = "-0" + str(self.honapkerinput.get())
                    idoszak = "M_"
                elif self.honapkerinput.get().isnumeric() and len(self.honapkerinput.get()) == 2:
                    honapker = "-" + str(self.honapkerinput.get())
                    idoszak = "M_"
                idoker = evker + honapker
                tenyezo = {"csapadékösszeg": "r", "napsütéses órák": "s", "átl. hőmérséklet": "ta"}
                helyker = "data/reszletes/DE_" + idoszak + tenyezo[str(self.optmenu.get())] + ".txt"
                # rtip = {"felső sorból az adatmezők": 0, ...}
                # rjelm = {ua. csak a magyarázattal}

                # rfold, sfold, tafold, stb részek majd lehet 1ből még method előtt
                # self.id, self.iid értékeket fold-onként meg kell adni insertek előtt
                # self.iid = self.id + 1 ?? de akk vhogy mindig előtte id-t is meg kell adni/léptetni

                with open(helyker) as csvfile:
                    csvolv = csv.reader(csvfile, delimiter=';')
                    # rid = int(self.tree.focus())
                    # self.tree.delete(rid)
                    self.tree.selection()
                    idotal = 0
                    for row in csvolv:
                        if idoker in str(row[0]):

                            for i, v in enumerate(row):
                                self.tree.insert(
                                    self.rfold, self.id, self.iid, text=evker,
                                    values=(v, v)
                                )
                                # text=rtip(i), values=(v, rjelm(i))
                                self.iid += 1
                                self.id += 1
                            idotal += 1
                    # self.tree.configure(state="disabled")
                    if idotal == 0:
                        messagebox.showwarning(None, "Hiba: A keresés eredménytelen volt!")
            else:
                messagebox.showerror(None, "Hiányzó vagy nem megfelelő input!!\n(Keresett tényező!)")
        else:
            messagebox.showerror(None, "Hiányzó vagy nem megfelelő input!!")

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

    @staticmethod
    def mmentvalid(instr, acttyp):
        if acttyp == '1':
            if not instr.isdigit() or len(instr) > 2 or int(instr) not in range(1, 13):
                return False
        return True


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
        # self.configure("TTreeview")


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
