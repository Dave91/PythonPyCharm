import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv


def searchdata():
    if evkerinput.get().isnumeric():
        with open('DE_Y_r.csv') as csvfile:
            evker = str(evkerinput.get())
            csvolv = csv.reader(csvfile, delimiter=';')
            match = 0
            for row in csvolv:
                if evker in row:
                    evi_csap_ossz.set(row[1])
                    ebbol_hav.set(row[2])
                    napi_csap_max.set(row[3] + " (" + row[4] + ")")
                    adott_0_1.set(row[5])
                    adott_1.set([6])
                    adott_5.set([7])
                    adott_10.set(row[8])
                    adott_20.set(row[9])
                    adott_30.set(row[10])
                    adott_50.set(row[11])
                    hav_nap.set(row[12])
                    jeg_nap.set(row[13])
                    ziv_nap.set(row[14])
                    on_nap.set(row[15])
                    match += 1
            if match == 0:
                messagebox.showwarning(None, "A keresett évszám nem található! \n(Próbáld: 1901-2010)")
            else:
                messagebox.showinfo(None, "Sikeres keresés :) \nVizsgált év: " + evker)
    else:
        messagebox.showerror(None, "Nem megfelelő input!! \n(Megfelelő: csak numerikus)")


def savedata():
    if evkerinput.get().isnumeric():
        with open('DE_Y_r.csv') as csvfile:
            evker = str(evkerinput.get())
            csvolv = csv.reader(csvfile, delimiter=';')
            match = 0
            for row in csvolv:
                if evker in row:
                    evi_csap_ossz.set(row[1])
                    ebbol_hav.set(row[2])
                    napi_csap_max.set(row[3] + " (" + row[4] + ")")
                    adott_0_1.set(row[5])
                    adott_1.set([6])
                    adott_5.set([7])
                    adott_10.set(row[8])
                    adott_20.set(row[9])
                    adott_30.set(row[10])
                    adott_50.set(row[11])
                    hav_nap.set(row[12])
                    jeg_nap.set(row[13])
                    ziv_nap.set(row[14])
                    on_nap.set(row[15])
                    match += 1
            if match == 0:
                csvfile.close()
                messagebox.showwarning(None, "A keresett évszám nem található! \n(Próbáld: 1901-2010)")
            else:
                csvfile.close()
                messagebox.showinfo(None, "Sikeres keresés :) \nVizsgált év: " + evker)
    else:
        messagebox.showerror(None, "Nem megfelelő input!! \n(Megfelelő: csak numerikus)")


# ROOT WINDOW
root = tk.Tk()
root.title("MeteoLog")
appicon = tk.PhotoImage(file="icons/umbrella-icon-small.png")
root.iconphoto(False, appicon)
root.geometry("280x460")
root.resizable(0, 0)
root.config(background="beige", cursor="umbrella")

# MENU ELEMENTS
menubar = tk.Menu(root)

menu_file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=menu_file)
menu_file.add_command(label='New', command=None)
menu_file.add_command(label='Open', command=None)
menu_file.add_command(label='Save', command=None)
menu_file.add_separator()
menu_file.add_command(label='Exit', command=root.destroy)

menu_options = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Options', menu=menu_options)
menu_options.add_command(label='Settings', command=None)

menu_help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=menu_help)
menu_help.add_command(label='About', command=None)

root.config(menu=menubar)

# STYLES
style = ttk.Style()
style.configure("TLabel", background="beige")
style.configure("TEntry", foreground="blue")
style.configure("TButton", background="gold")
style.configure("TNotebook", background="#DAF7A6")
style.configure("TNotebook.Tab", padding=(10, 2, 10, 2), background="gold")
style.configure("TFrame", background="beige")

# TAB MENU control
tabmenu = ttk.Notebook(root)
tabeves = ttk.Frame(tabmenu)
tabhavi = ttk.Frame(tabmenu)
tabnapi = ttk.Frame(tabmenu)
tabmenu.pack(expand=1, fill="both")

tabmenu.add(tabeves, text="Éves adatok")
tabmenu.add(tabhavi, text="Havi adatok")
tabmenu.add(tabnapi, text="Napi adatok")

# TABEVES ---------------------------------------------
# block control
toprow = ttk.Frame(tabeves)
toprow.pack(side="top", expand=1, fill="x")
bottrow = ttk.Frame(tabeves)
bottrow.pack(side="bottom", expand=1, fill="x")
leftcol = ttk.Frame(tabeves)
leftcol.pack(side="left", expand=1, fill="both")
rightcol = ttk.Frame(tabeves)
rightcol.pack(side="right", expand=1, fill="both")

# top row
ttk.Label(toprow, text="(debreceni adatok, mm-ben)").pack()
ttk.Label(toprow, text="(1901-2010)").pack()

# bottom row
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

# left column
evkerinput = tk.StringVar()
evkerinput.set("év")
ttk.Entry(leftcol, textvariable=evkerinput, justify="right").pack(pady=2, anchor="e")

ttk.Label(leftcol, text="Évi csapadékösszeg:").pack(anchor="e")
ttk.Label(leftcol, text="(ebből hó:)").pack(anchor="e")
ttk.Label(leftcol, text="Napi csapadék maximum:").pack(anchor="e")
ttk.Label(leftcol, text="(adott csapadékösszegű napok)").pack(anchor="e")
ttk.Label(leftcol, text="0,1-1 mm:").pack(anchor="e")
ttk.Label(leftcol, text="1-5 mm:").pack(anchor="e")
ttk.Label(leftcol, text="5-10 mm:").pack(anchor="e")
ttk.Label(leftcol, text="10-20 mm:").pack(anchor="e")
ttk.Label(leftcol, text="20-30 mm:").pack(anchor="e")
ttk.Label(leftcol, text="30-50 mm:").pack(anchor="e")
ttk.Label(leftcol, text="50+ mm:").pack(anchor="e")
ttk.Label(leftcol, text="Havas napok:").pack(anchor="e")
ttk.Label(leftcol, text="Jeges napok:").pack(anchor="e")
ttk.Label(leftcol, text="Zivataros napok:").pack(anchor="e")
ttk.Label(leftcol, text="Ónos napok:").pack(anchor="e")

# right column
ttk.Button(rightcol, text="Keresés", command=lambda: searchdata()).pack(anchor="w")

evi_csap_ossz = tk.StringVar()
ttk.Label(rightcol, textvariable=evi_csap_ossz).pack(anchor="w")
ebbol_hav = tk.StringVar()
ttk.Label(rightcol, textvariable=ebbol_hav).pack(anchor="w")
napi_csap_max = tk.StringVar()
ttk.Label(rightcol, textvariable=napi_csap_max).pack(anchor="w")
ttk.Label(rightcol, text="").pack(anchor="w")
adott_0_1 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_0_1).pack(anchor="w")
adott_1 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_1).pack(anchor="w")
adott_5 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_5).pack(anchor="w")
adott_10 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_10).pack(anchor="w")
adott_20 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_20).pack(anchor="w")
adott_30 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_30).pack(anchor="w")
adott_50 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_50).pack(anchor="w")
hav_nap = tk.StringVar()
ttk.Label(rightcol, textvariable=hav_nap).pack(anchor="w")
jeg_nap = tk.StringVar()
ttk.Label(rightcol, textvariable=jeg_nap).pack(anchor="w")
ziv_nap = tk.StringVar()
ttk.Label(rightcol, textvariable=ziv_nap).pack(anchor="w")
on_nap = tk.StringVar()
ttk.Label(rightcol, textvariable=on_nap).pack(anchor="w")

# TABHAVI --------------------------------------------

ttk.Label(tabhavi).pack()

# TABNAPI --------------------------------------------

ttk.Label(tabnapi).pack()

# gui handler
root.mainloop()
