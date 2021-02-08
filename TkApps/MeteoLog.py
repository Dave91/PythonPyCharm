import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog  # , simpledialog
from os import curdir
import csv


def searchdata():
    if evkerinput.get().isnumeric() or (evkerinput.get().isnumeric() and honapkerinput.get().isnumeric()) or (
        evkerinput.get().isnumeric() and honapkerinput.get().isnumeric() and napkerinput.get().isnumeric()
    ):
        if str(optmenu.get()) != "<állomáshely>":
            evker = str(evkerinput.get())
            if honapkerinput.get().isnumeric() and len(honapkerinput.get()) == 1:
                honapker = "0" + str(honapkerinput.get())
            elif honapkerinput.get().isnumeric() and len(honapkerinput.get()) == 2:
                honapker = str(honapkerinput.get())
            else:
                honapker = ""
            if napkerinput.get().isnumeric() and len(napkerinput.get()) == 1:
                napker = "0" + str(napkerinput.get())
            elif napkerinput.get().isnumeric() and len(napkerinput.get()) == 2:
                napker = str(napkerinput.get())
            else:
                napker = ""
            kerinput = evker + honapker + napker
            helyker = "data/" + str(optmenu.get()) + "_19012019.csv"
            with open(helyker) as csvfile:
                csvolv = csv.reader(csvfile, delimiter=';')
                txtbox.configure(state="normal")
                txtbox.delete(1.0, tk.END)
                match = 0
                for row in csvolv:
                    if kerinput in str(row[0]):
                        napialapoutput = "\t".join(row) + "\n"
                        txtbox.insert(tk.END, *napialapoutput.splitlines(keepends=True))
                        match += 1
                txtbox.configure(state="disabled")
                if match == 0:
                    messagebox.showwarning(None, "Hiba: A keresés eredménytelen volt!")
                else:
                    sumrestxtbox.configure(state="normal")
                    sumrestxtbox.delete(1.0, tk.END)
                    sumrestxtbox.insert(tk.END, "Sorok (napok) száma: " + str(match))
                    sumrestxtbox.configure(state="disabled")
                #    messagebox.showinfo(None, "Megtalált rekordok száma: " + str(match))
        else:
            messagebox.showerror(None, "Nem megfelelő input!! \n(Kötelező: Állomáshely kiválasztása!)")
    else:
        messagebox.showerror(None, "Nem megfelelő input!! \n(Megfelelő: Év, Év + Hónap, Év + Hónap + Nap)")


def savedata():
    if txtbox is not "":
        defdir = curdir
        savenamedir = ""
        while savenamedir == "":
            savenamedir = filedialog.asksaveasfile(
                mode="a",
                initialdir=defdir,
                filetypes=(("Text Files", "*.txt"), ("CSV Files", "*.csv")),
                defaultextension=".txt"
            )
        if savenamedir is None:
            return
        with savenamedir as savefile:
            evker = str(evkerinput.get())
            savefile.write(
                "\n\n(debreceni adatok, mm-ben)" +
                "\nA vizsgált év: " + evker +
                "\n\n" + str(txtbox) + "\n"
            )
            savefile.close()
            messagebox.showinfo(None, "Keresett rekord sikeresen elmentve!")
        # any way to check success here??
    else:
        messagebox.showerror(None, "Nincs menthető input!! \n(Előbb végezz keresést!)")


def yearentvalid(instr, acttyp):
    if acttyp == '1':
        if not instr.isdigit():
            return False
        if len(instr) == 1:
            if int(instr) < 1 or int(instr) > 2:
                return False
        if len(instr) == 2:
            if int(instr) < 19 or int(instr) > 20:
                return False
        if len(instr) == 3:
            if int(instr) < 190 or int(instr) > 201:
                return False
        if len(instr) == 4:
            if int(instr) < 1901 or int(instr) > 2019:
                return False
        if len(instr) > 4:
            return False
    return True


def mmentvalid(instr, acttyp):
    if acttyp == '1':
        if not instr.isdigit():
            return False
        if len(instr) > 2:
            return False
        if int(instr) < 1 or int(instr) > 12:
            return False
    return True


def ddentvalid(instr, acttyp):
    if acttyp == '1':
        if not instr.isdigit():
            return False
        if len(instr) > 2:
            return False
        if int(instr) < 1 or int(instr) > 31:
            return False
    return True


def sumdatares():
    txtbox.configure(state="normal")
    if len(txtbox.get(1.0, tk.END)) <= 5 or (
        evkerinput.get().isnumeric() and honapkerinput.get().isnumeric() and napkerinput.get().isnumeric()
    ):
        txtbox.configure(state="disabled")
        messagebox.showwarning(None, "Hiányzó vagy nem elegendő adatsorok!!")
    else:
        if str(sumresonoff.get()) == "off":
            sumrestxtbox.pack()
            sumbuttlab.set("Vissza")
            sumresonoff.set("on")
        else:
            sumrestxtbox.forget()
            sumbuttlab.set("Összesít")
            sumresonoff.set("off")
        txtbox.configure(state="disabled")


# ROOT WINDOW
root = tk.Tk()
root.title("MeteoLog")
appicon = tk.PhotoImage(file="icons/umbrella-icon-small.png")
root.iconphoto(False, appicon)
root.geometry("280x460")
root.resizable(0, 0)
root.config(background="beige", cursor="cross")

# MENU ELEMENTS
menubar = tk.Menu(root)

menu_file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Fájl', menu=menu_file)
menu_file.add_command(label='New', command=None)
menu_file.add_command(label='Open', command=None)
menu_file.add_command(label='Save As', command=lambda: savedata())
menu_file.add_separator()
menu_file.add_command(label='Kilépés', command=root.destroy)

menu_options = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Options', menu=menu_options)
menu_options.add_command(label='Settings', command=None)

menu_help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=menu_help)
menu_help.add_command(label='About', command=None)

root.config(menu=menubar)

# STYLES
style = ttk.Style()
# style.theme_use("winnative")
style.configure("TLabel", background="beige")
style.configure("TEntry", foreground="blue")
style.configure("TButton", foreground="maroon")
style.configure("TNotebook", background="#DAF7A6")
style.configure("TNotebook.Tab", foreground="blue", padding=(10, 2, 10, 2))
style.configure("TFrame", background="beige")
style.configure("TMenubutton", background="#D7DDDC", foreground="blue")
style.configure("TScrollbar", background="beige")

# TAB MENU control
tabmenu = ttk.Notebook(root)
tabnapialap = ttk.Frame(tabmenu)
tabevesreszl = ttk.Frame(tabmenu)
tabteszt = ttk.Frame(tabmenu)
tabmenu.pack(expand=1, fill="both")

tabmenu.add(tabnapialap, text="Napi alapadatok")
tabmenu.add(tabevesreszl, text="Éves részletes")  # éves/havi/napi lenyíló menüvel (mint napinál Bp, Khely, Szhely)!!
tabmenu.add(tabteszt, text="tesztfül")
# százéves összesített
# abszolút rekordok
# diagram?? v inkább vmi treeview!! az szűrhető?? átlagok számítása, stb!

# TAB NAPI ALAP ---------------------------------------------
# block control
toprow = ttk.Frame(tabnapialap)
toprow.pack(side="top", expand=1, fill="x")
bottrow = ttk.Frame(tabnapialap)
bottrow.pack(side="bottom", expand=1, fill="x")
leftcol = ttk.Frame(tabnapialap)
leftcol.pack(side="left", expand=1, fill="both")
rightcol = ttk.Frame(tabnapialap)
rightcol.pack(side="right", expand=1, fill="both")

# sumrestxtbox
sumrestxtbox = tk.Text(
    tabmenu, background="lightgrey", font=("Arial", 8), width=45, height=25, relief="groove", borderwidth=2.5,
    # yscrollcommand=scrollbar.set
)
sumrestxtbox.configure(state="disabled")
sumrestxtbox.lift(aboveThis=tabnapialap)
sumresonoff = tk.StringVar()
sumresonoff.set("off")

# top row
ttk.Label(toprow, text="(Budapest, Keszthely, Szombathely)").pack()
ttk.Label(toprow, text="(1901.01.01 - 2019.12.31)").pack()

optmenu = tk.StringVar()
ttk.OptionMenu(toprow, optmenu, "<állomáshely>", "Budapest", "Keszthely", "Szombathely").pack(side="left", padx=4)

evkerinput = tk.StringVar()
evkerinput.set("ÉÉÉÉ")
yearent = ttk.Entry(toprow, textvariable=evkerinput, validate="key", width=5, justify="center")
yearent["validatecommand"] = (yearent.register(yearentvalid), "%P", "%d")
yearent.pack(side="left")

honapkerinput = tk.StringVar()
honapkerinput.set("HH")
monthent = ttk.Entry(toprow, textvariable=honapkerinput, validate="key", width=3, justify="center")
monthent["validatecommand"] = (monthent.register(mmentvalid), "%P", "%d")
monthent.pack(side="left")

napkerinput = tk.StringVar()
napkerinput.set("NN")
dayent = ttk.Entry(toprow, textvariable=napkerinput, validate="key", width=3, justify="center")
dayent["validatecommand"] = (dayent.register(ddentvalid), "%P", "%d")
dayent.pack(side="left")

ttk.Button(toprow, text="Keresés", command=lambda: searchdata()).pack(side="left", padx=2)

# left & right cols
ttk.Label(leftcol, text="idő\tr\ttn\tt\ttx").pack(side="top")
ttk.Label(rightcol).pack(side="top")

scrollbar = ttk.Scrollbar(rightcol)
scrollbar.pack(side="right", expand=1, fill="both")
txtbox = tk.Text(
    leftcol, background="lightgrey", font=("Arial", 8), width=40, height=20, relief="groove",
    yscrollcommand=scrollbar.set
)
txtbox.configure(state="disabled")
txtbox.pack(side="left", expand=1, fill="both")
scrollbar.config(command=txtbox.yview)

# bottom row
sumbuttlab = tk.StringVar()
sumbuttlab.set("Összesít")
ttk.Button(bottrow, textvariable=sumbuttlab, command=lambda: sumdatares()).pack(side="top", anchor="w", padx=85)

metim1 = tk.PhotoImage(file="icons/meteo1sunny.png").zoom(25).subsample(32)
ttk.Label(bottrow, image=metim1).pack(side="left")
metim2 = tk.PhotoImage(file="icons/meteo2cloudy-partly.png").zoom(25).subsample(32)
ttk.Label(bottrow, image=metim2).pack(side="left")
metim3 = tk.PhotoImage(file="icons/meteo3cloudy.png").zoom(25).subsample(32)
ttk.Label(bottrow, image=metim3).pack(side="left")
metim4 = tk.PhotoImage(file="icons/meteo4thunder-lightning-storm.png").zoom(25).subsample(32)
ttk.Label(bottrow, image=metim4).pack(side="left")
metim5 = tk.PhotoImage(file="icons/meteo5rain.png").zoom(25).subsample(32)
ttk.Label(bottrow, image=metim5).pack(side="left")

# TAB RESZL --------------------------------------------

ttk.Label(tabevesreszl).pack()

# TAB TESZT --------------------------------------------

ttk.Label(tabteszt).pack()

# gui handler
root.mainloop()
