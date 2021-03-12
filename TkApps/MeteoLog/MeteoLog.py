import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
# from tkinter import filedialog  # , simpledialog
# from os import curdir
import csv
import matplotlib.pyplot as plt
import numpy as np


class TabMenu(ttk.Notebook):
    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent)
        self.parent = parent
        self.pack(expand=1, fill="both")
        BottomBar().pack(side="bottom", expand=0, fill="x")

        TabNapiAlap(self)
        TabEvesReszl(self)
        TabDiagram(self)


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

        ttk.Button(self.toprow, text="Keresés", command=self.searchfilterdata).pack(side="left", padx=2)

        # left & right cols
        ttk.Label(self.leftcol, text="idő\tr\ttn\tt\ttx").pack(side="top")
        ttk.Label(self.rightcol).pack(side="top")

        self.scrollbar = ttk.Scrollbar(self.rightcol)
        self.scrollbar.pack(side="right", expand=1, fill="both")
        self.txtbox = tk.Text(
            self.leftcol, font=("Arial", 8), width=45, height=22, relief="groove", borderwidth=1.5,
            state="disabled", yscrollcommand=self.scrollbar.set)
        self.txtbox.pack(side="left", expand=1, fill="both")
        self.scrollbar.config(command=self.txtbox.yview)

        # bottom row
        self.sumresbutt = ttk.Button(self.bottrow, text="Összegez", command=self.sumresdataopen, state="disabled")
        self.sumresbutt.pack(side="left", padx=25)
        self.filtbutt = ttk.Button(self.bottrow, text="Szűrési opciók", command=self.filtdataopen, state="disabled")
        self.filtbutt.pack(side="right", padx=25)

        # filtkerbox PLACED OVER tabnapi
        self.filtkerbox = ttk.Frame(self, relief="groove", borderwidth=1.5)
        self.filtkerbox.lift()
        self.filtkerbox.grid_columnconfigure(4, weight=1)

        ttk.Button(self.filtkerbox, text="Bezár", command=self.filtdataclose
                   ).grid(row=1, column=2, pady=10, columnspan=3)

        self.optmenucol = tk.StringVar()
        ttk.OptionMenu(self.filtkerbox, self.optmenucol, "<adat>", "csap.össz.", "min. hőm.", "középhőm.", "max. hőm."
                       ).grid(row=2, column=1)

        self.optmenuop = tk.StringVar()
        ttk.OptionMenu(self.filtkerbox, self.optmenuop, "<jel>", " == ", " != ", " > ", " < "
                       ).grid(row=2, column=2)

        self.filtvalinput = tk.StringVar()
        self.filtvalinput.set("")
        self.filtent = ttk.Entry(self.filtkerbox, textvariable=self.filtvalinput, validate="key",
                                 width=6, justify="center")
        self.filtent["validatecommand"] = (self.filtent.register(self.filtentvalid), "%P", "%d")
        self.filtent.grid(row=2, column=3)

        ttk.Button(self.filtkerbox, text="Hozzáad", command=self.filtraddbutt).grid(row=2, column=4)

        self.filtr1 = tk.StringVar()
        self.filtr1.set("<nincs megadva>")
        self.filtr2 = tk.StringVar()
        self.filtr2.set("<nincs megadva>")
        self.filtr3 = tk.StringVar()
        self.filtr3.set("<nincs megadva>")
        self.filtr4 = tk.StringVar()
        self.filtr4.set("<nincs megadva>")
        self.filtract1 = tk.IntVar()
        self.filtract1.set(0)
        self.filtract2 = tk.IntVar()
        self.filtract2.set(0)
        self.filtract3 = tk.IntVar()
        self.filtract3.set(0)
        self.filtract4 = tk.IntVar()
        self.filtract4.set(0)

        ttk.Label(self.filtkerbox, textvariable=self.filtr1).grid(row=3, column=1, pady=2, columnspan=2)
        ttk.Label(self.filtkerbox, textvariable=self.filtr2).grid(row=4, column=1, pady=2, columnspan=2)
        ttk.Label(self.filtkerbox, textvariable=self.filtr3).grid(row=5, column=1, pady=2, columnspan=2)
        ttk.Label(self.filtkerbox, textvariable=self.filtr4).grid(row=6, column=1, pady=2, columnspan=2)

        self.filtrcb1 = ttk.Checkbutton(self.filtkerbox, offvalue=0, onvalue=1,
                                        variable=self.filtract1, state="disabled")
        self.filtrcb1.grid(row=3, column=3, pady=2)

        self.filtrcb2 = ttk.Checkbutton(self.filtkerbox, offvalue=0, onvalue=1,
                                        variable=self.filtract2, state="disabled")
        self.filtrcb2.grid(row=4, column=3, pady=2)

        self.filtrcb3 = ttk.Checkbutton(self.filtkerbox, offvalue=0, onvalue=1,
                                        variable=self.filtract3, state="disabled")
        self.filtrcb3.grid(row=5, column=3, pady=2)

        self.filtrcb4 = ttk.Checkbutton(self.filtkerbox, offvalue=0, onvalue=1,
                                        variable=self.filtract4, state="disabled")
        self.filtrcb4.grid(row=6, column=3, pady=2)

        ttk.Label(self.filtkerbox, text="Kapcsolat köztük:").grid(row=7, column=1, pady=4, columnspan=2)
        self.rbvar = tk.StringVar()
        self.rbvar.set(" and ")
        ttk.Radiobutton(self.filtkerbox, text="és", variable=self.rbvar, value=" and ").grid(row=7, column=3, pady=4)
        ttk.Radiobutton(self.filtkerbox, text="vagy", variable=self.rbvar, value=" or ").grid(row=7, column=4, pady=4)

        # sumresbox PLACED OVER tabnapi
        self.sumresbox = ttk.Frame(self, relief="groove", borderwidth=1.5)
        self.sumresbox.lift()

        ttk.Button(self.sumresbox, text="Bezár", command=self.sumresdataclose).pack(pady=10)

        self.sumrestxtbox = tk.Text(self.sumresbox, font=("Arial", 8), width=50, height=22, state="disabled",
                                    relief="groove", borderwidth=1.5)
        self.sumrestxtbox.pack()

    def filtraddbutt(self):
        fcol = self.optmenucol.get()
        fop = self.optmenuop.get()
        fval = format(float(self.filtvalinput.get()), "10.1f")

        if fcol == "<adat>" or fop == "<jel>" or fval == "":
            messagebox.showerror(None, "Hiba: hiányos input!\nKitöltetlen mezők!")

        freefiltr = [1, 2, 3, 4]
        for n in range(1, 5):
            if eval("self.filtract" + str(n) + ".get()") == 1:
                freefiltr.remove(n)

        try:
            usefiltr = str(freefiltr[0])
            eval("self.filtr" + usefiltr + ".set(fcol + fop + str(fval))")
            eval("self.filtrcb" + usefiltr + ".configure(state='normal')")
            eval("self.filtract" + usefiltr + ".set(1)")
        except IndexError:
            messagebox.showwarning(None, "A feltétel-lista megtelt!")

    def searchfilterdata(self):
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
                self.filtbutt.configure(state="disabled")
                self.sumresbutt.configure(state="disabled")
                filterfuncval = "str(row[0]).find(kerinput) == 0"
                if (self.filtract1.get() or self.filtract2.get() or self.filtract3.get() or self.filtract4.get()) == 1:
                    filterfuncval = self.filterfunconoff()
                with open(helyker) as csvfile:
                    csvolv = csv.reader(csvfile, delimiter=";")
                    self.txtbox.configure(state="normal")
                    self.txtbox.delete(1.0, tk.END)
                    ossznap, esonap, mintnap = 0, 0, 0
                    osszcsapm, sumtn, sumt, sumtx = 0.0, 0.0, 0.0, 0.0
                    abstn, abstx = 30.0, -10.0
                    for row in csvolv:
                        if eval(filterfuncval) is True:
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
                    if ossznap > 1:
                        self.filtbutt.configure(state="normal")
                        self.sumresdatafunc(esonap, ossznap, mintnap, osszcsapm, sumtn, sumt, sumtx, abstn, abstx)
                    # else:
            else:
                messagebox.showerror(None, "Nem megfelelő input!! \n(Kötelező: Állomáshely kiválasztása!)")
        else:
            messagebox.showerror(None, "Nem megfelelő input!! \n(Megfelelő: Év, Év + Hónap, Év + Hónap + Nap)")

    def filterfunconoff(self):
        colold = ["csap.össz.", "min. hőm.", "középhőm.", "max. hőm."]
        colnew = ["float(row[1])", "float(row[2])", "float(row[3])", "float(row[4])"]
        filt1 = self.filtr1.get()
        filt2 = self.filtr2.get()
        filt3 = self.filtr3.get()
        filt4 = self.filtr4.get()
        rb = self.rbvar.get()
        for e in range(4):
            filt1 = filt1.replace(colold[e], colnew[e])
            filt2 = filt2.replace(colold[e], colnew[e])
            filt3 = filt3.replace(colold[e], colnew[e])
            filt4 = filt4.replace(colold[e], colnew[e])
        withfiltprep = "str(row[0]).find(kerinput) == 0 and ("
        fpoz = 0
        if self.filtract1.get() == 1:
            fpoz += 1
            withfiltprep = withfiltprep + filt1
        if self.filtract2.get() == 1:
            if fpoz == 0:
                fpoz += 1
                withfiltprep = withfiltprep + filt2
            else:
                fpoz += 1
                withfiltprep = withfiltprep + rb + filt2
        if self.filtract3.get() == 1:
            if fpoz == 0:
                fpoz += 1
                withfiltprep = withfiltprep + filt3
            else:
                fpoz += 1
                withfiltprep = withfiltprep + rb + filt3
        if self.filtract4.get() == 1:
            if fpoz == 0:
                fpoz += 1
                withfiltprep = withfiltprep + filt4
            else:
                fpoz += 1
                withfiltprep = withfiltprep + rb + filt4
        withfiltprep = withfiltprep + ")"
        return withfiltprep

    def sumresdatafunc(self, esonap, ossznap, mintnap, osszcsapm, sumtn, sumt, sumtx, abstn, abstx):
        self.sumresbutt.configure(state="normal")
        self.sumrestxtbox.configure(state="normal")
        self.sumrestxtbox.delete(1.0, tk.END)
        esoosszrat = float(format(esonap / ossznap, "10.1f"))
        mintosszrat = float(format(mintnap / ossznap, "10.1f"))
        csapmatl = format(osszcsapm / float(esonap), "10.1f")
        tnatl = format(sumtn / float(ossznap), "10.1f")
        tatl = format(sumt / float(ossznap), "10.1f")
        txatl = format(sumtx / float(ossznap), "10.1f")
        self.sumrestxtbox.insert(
            tk.END, "Napok összesen:\t" + str(ossznap)
                    + "\nEbből csapadékos:\t" + str(esonap)
                    + "\nArányuk:\t" + str(esoosszrat)
                    + "\n\nÖsszes csapadékm.:\t" + str(format(osszcsapm, "10.1f"))
                    + "\nÁtl. (napi) csapadékm.:\t" + str(csapmatl)
                    + "\n\nNapi min. hőm. átlaga:\t" + str(tnatl)
                    + "\nNapi átl. hőm. átlaga:\t" + str(tatl)
                    + "\nNapi max. hőm. átlaga:\t" + str(txatl)
                    + "\n\nNegatív középhőm. napok:\t" + str(mintnap)
                    + "\nArányuk (összesből):\t" + str(mintosszrat)
                    + "\n\nAbsz. napi min. hőm.:\t" + str(abstn)
                    + "\nAbsz. napi max. hőm.:\t" + str(abstx)
        )
        self.sumrestxtbox.configure(state="disabled")

    @staticmethod
    def yearentvalid(instr, acttyp):
        if acttyp == "1":
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
        if acttyp == "1":
            if not instr.isdigit() or len(instr) > 2 or int(instr) not in range(1, 13):
                return False
        return True

    @staticmethod
    def ddentvalid(instr, acttyp):
        if acttyp == "1":
            if not instr.isdigit() or len(instr) > 2 or int(instr) not in range(1, 32):
                return False
        return True

    @staticmethod
    def filtentvalid(instr, acttyp):
        if acttyp == "1":
            if len(instr) > 5:
                return False
            elif not instr.isdigit() and "." not in instr and "-" not in instr:
                return False
        return True

    def sumresdataclose(self):
        self.sumresbox.place_forget()

    def sumresdataopen(self):
        self.sumresbox.place(relx=0.0, rely=0.2, relwidth=1.0, relheight=0.8)

    def filtdataclose(self):
        self.filtkerbox.place_forget()

    def filtdataopen(self):
        self.filtkerbox.place(relx=0.0, rely=0.2, relwidth=1.0, relheight=0.8)


class TabEvesReszl(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        parent.add(self, text="Éves részletes")

        # block control
        self.toprow = ttk.Frame(self)
        self.toprow.pack(side="top")
        self.bottrow = ttk.Frame(self)
        self.bottrow.pack(side="bottom", expand=1, fill="both")

        # top row
        ttk.Label(self.toprow, text="(Debrecen: 1901 - 2010)").pack()
        ttk.Label(self.toprow, text="(csap.össz., naps. órák, átlaghőm.)").pack()

        self.evkerinput = tk.StringVar()
        self.evkerinput.set("ÉÉÉÉ")
        self.yearent = ttk.Entry(self.toprow, textvariable=self.evkerinput, validate="key", width=7, justify="center")
        self.yearent["validatecommand"] = (self.yearent.register(self.yearentvalid), "%P", "%d")
        self.yearent.pack(side="left", padx=15)

        ttk.Button(self.toprow, text="Keresés", command=self.searchdata).pack(padx=2)

        # bottom row
        self.tree = ttk.Treeview(self.bottrow, columns=("Évszám", "Érték"), height=17)
        self.tree.column("#0", width=110, minwidth=110, stretch=0)
        self.tree.column("#1", width=85, minwidth=85, stretch=0)
        self.tree.column("#2", width=95, minwidth=95, stretch=0)
        self.tree.heading("#0", text="Tényező")
        self.tree.heading("#1", text="Évszám")
        self.tree.heading("#2", text="Érték")
        self.tree.pack(side="bottom")

        self.id, self.iid = 0, 2

    def searchdata(self):
        if self.evkerinput.get().isnumeric() and len(self.evkerinput.get()) == 4:
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
            evker = str(self.evkerinput.get())
            idotal = 0
            rfold = self.tree.insert("", 1, 1, text="csap.össz.")
            with open("data/evesreszl/DE_Y_r.txt") as csvfile:
                csvolv = csv.reader(csvfile, delimiter=";")
                for row in csvolv:
                    if evker in str(row[0]):
                        for i, v in enumerate(row):
                            self.tree.insert(rfold, self.id, self.iid, text="", values=(rtip[i], v))
                            self.iid += 1
                            self.id += 1
                        idotal += 1
            sfold = self.tree.insert("", 2, self.iid, text="naps. órák")
            self.iid += 1
            with open("data/evesreszl/DE_Y_s.txt") as csvfile:
                csvolv = csv.reader(csvfile, delimiter=";")
                for row in csvolv:
                    if evker in str(row[0]):
                        for i, v in enumerate(row):
                            self.tree.insert(sfold, self.id, self.iid, text="", values=(stip[i], v))
                            self.iid += 1
                            self.id += 1
                        idotal += 1
            tafold = self.tree.insert("", 3, self.iid, text="átlaghőm.")
            self.iid += 1
            with open("data/evesreszl/DE_Y_ta.txt") as csvfile:
                csvolv = csv.reader(csvfile, delimiter=";")
                for row in csvolv:
                    if evker in str(row[0]):
                        for i, v in enumerate(row):
                            self.tree.insert(tafold, self.id, self.iid, text="", values=(tatip[i], v))
                            self.iid += 1
                            self.id += 1
                        idotal += 1
            if idotal == 0:
                messagebox.showwarning(None, "Hiba: A keresés eredménytelen volt!")
        else:
            messagebox.showerror(None, "Hiányzó vagy nem megfelelő input!!")

    @staticmethod
    def yearentvalid(instr, acttyp):
        if acttyp == "1":
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


class TabDiagram(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        parent.add(self, text="Diagram")

        # block control
        self.toprow = ttk.Frame(self)
        self.toprow.pack(side="top")
        self.bottrow = ttk.Frame(self, borderwidth=2, relief="groove")
        self.bottrow.pack(side="bottom", expand=1, fill="both")

        # top row
        ttk.Label(self.toprow, text="(1901 - 2010)").pack()
        ttk.Label(self.toprow, text="(id.tény. izébizé").pack()

        self.optmenu = tk.StringVar()
        ttk.OptionMenu(
            self.toprow, self.optmenu, "<tényező>", "csapadékösszeg", "napsütéses órák", "átlaghőmérséklet"
        ).pack(side="left", padx=4)

        ttk.Button(self.toprow, text="Keresés", command=self.searchdrawdata).pack(side="left", padx=4)

        # bottom row

        '''
        matplotlib.use('TkAgg')
        self.fig = Figure(figsize=(2, 2), dpi=90)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.bottrow)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="bottom", expand=1, fill="both")
        '''

    def searchdrawdata(self):
        import pandas as pd
        if str(self.optmenu.get()) != "<tényező>":
            tenyezo = {"csapadékösszeg": "r", "napsütéses órák": "s", "átlaghőmérséklet": "ta"}
            pdread = pd.read_csv("data/evesreszl/DE_Y_" + tenyezo[str(self.optmenu.get())] + ".txt", delimiter=";")
            yval = pdread["y_rs"]
            ev = pdread["#ev"]
            x = np.arange(len(pdread))
            fig = plt.figure(figsize=(12, 5))
            canv = plt.FigureCanvasBase(fig)
            canv.draw()
            plt.bar(x, yval)  # leht ink horiz kéne, mivel ablak ink magas
            plt.xticks(x, [], rotation=90)
            plt.xlabel("idő (évek)")
            plt.ylabel("érték")  # vart áthozni tényezőtől függő mértékegys.
            plt.title("éves vmi adatok százéves alakulása")  # itt is ua.
            # plt.autoscale(True, "y")
            plt.show()
        else:
            messagebox.showerror(None, "Hiányzó vagy nem megfelelő input!!")


class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.parent = parent

        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Fájl", menu=menu_file)
        # menu_file.add_command(label='Létrehoz', command=None)
        menu_file.add_command(label="Import", command=None)
        menu_file.add_command(label="Export", command=None)
        menu_file.add_separator()
        menu_file.add_command(label="Kilépés", command=parent.destroy)

        menu_options = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Opciók", menu=menu_options)
        menu_options.add_command(label="Beállítások", command=None)

        menu_help = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Súgó", menu=menu_help)
        menu_help.add_command(label="Névjegy", command=None)

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

        # self.theme_use("winnative")
        self.configure("TLabel", background="beige")
        self.configure("TEntry", foreground="blue")
        self.configure("TButton", foreground="maroon")
        self.configure("TCheckbutton", background="beige")
        self.configure("TRadiobutton", background="beige")
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
    root.geometry("300x520")
    root.resizable(0, 0)
    root.config(background="beige", cursor="cross")
    StyleConfig()
    MenuBar(root)
    TabMenu(root)
    # gui handler
    root.mainloop()


if __name__ == "__main__":
    main()
