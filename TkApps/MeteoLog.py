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
                    evesadatoutput.set(
                        "Évi csapadékösszeg: " + row[1] +
                        "\n(ebből hó:) " + row[2] +
                        "\nNapi csapadék maximum: " + row[3] + " (" + row[4] + ")" +
                        "\n(adott csapadékösszegű napok)" +
                        "\n0,1-1 mm: " + row[5] +
                        "\n1-5 mm: " + row[6] +
                        "\n5-10 mm: " + row[7] +
                        "\n10-20 mm: " + row[8] +
                        "\n20-30 mm: " + row[9] +
                        "\n30-50 mm: " + row[10] +
                        "\n50+ mm: " + row[11] +
                        "\nHavas napok: " + row[12] +
                        "\nJeges napok: " + row[13] +
                        "\nZivataros napok: " + row[14] +
                        "\nÓnos napok: " + row[15]
                    )
                    match += 1
            if match == 0:
                csvfile.close()
                messagebox.showwarning(None, "A keresett évszám nem található! \n(Próbáld: 1901-2010)")
            else:
                csvfile.close()
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
                    # do sth
                    match += 1
            if match == 0:
                messagebox.showwarning(None, "A keresett évszám nem található! \n(Próbáld: 1901-2010)")
            else:
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
style.configure("TNotebook.Tab", padding=(10, 2, 10, 2))
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
toprow.pack(side="top")
bottrow = ttk.Frame(tabeves)
bottrow.pack(side="bottom", expand=1, fill="both")
leftcol = ttk.Frame(tabeves)
leftcol.pack(side="left", expand=1, fill="x")
rightcol = ttk.Frame(tabeves)
rightcol.pack(side="right", expand=1, fill="x")

# top row
ttk.Label(toprow, text="(debreceni adatok, mm-ben)").pack()
ttk.Label(toprow, text="(1901-2010)").pack()

# bottom row
evesadatoutput = tk.StringVar()
tk.Message(bottrow, textvariable=evesadatoutput, bg="lightgrey", font=("Arial", 10), relief="groove")\
    .pack(expand=1, fill="both")

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

# right column
ttk.Button(rightcol, text="Keresés", command=lambda: searchdata()).pack(anchor="w")

# TABHAVI --------------------------------------------

ttk.Label(tabhavi).pack()

# TABNAPI --------------------------------------------

ttk.Label(tabnapi).pack()

# gui handler
root.mainloop()
