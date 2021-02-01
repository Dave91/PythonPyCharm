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
                csvfile.close()
                messagebox.showwarning(None, "A keresett évszám nem található! \n(Próbáld: 1901-2010)")
            else:
                csvfile.close()
                messagebox.showinfo(None, "Sikeres keresés :) \nVizsgált év: " + evker)
    else:
        messagebox.showerror(None, "Nem megfelelő input!! \n(Megfelelő: csak numerikus)")


# ROOT WINDOW DETAILS
root = tk.Tk()
root.title("MeteoLog")
root.geometry("300x450")
root.resizable(0, 0)
root.config(background="beige", cursor="umbrella")

# MENU ELEMENTS HERE
menubar = tk.Menu(root)
# File menu
menu_file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=menu_file)
menu_file.add_command(label='New', command=None)
menu_file.add_command(label='Open', command=None)
menu_file.add_command(label='Save', command=None)
menu_file.add_separator()
menu_file.add_command(label='Exit', command=root.destroy)

# Options menu
menu_options = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Options', menu=menu_options)
menu_options.add_command(label='Settings', command=None)

# Help menu
menu_help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=menu_help)
menu_help.add_command(label='About', command=None)

root.config(menu=menubar)

# STYLES for ttk widgets //USE style="stylename"??
style = ttk.Style()
style.configure("TMenu")
style.configure("TFrame", background="beige")
style.configure("TLabel", background="beige")
style.configure("TEntry", foreground="blue")
style.configure("TButton", background="gold")

# block control
toprow = ttk.Frame(root)
toprow.pack(side="top", expand=1, fill="x")
bottrow = ttk.Frame(root)
bottrow.pack(side="bottom", expand=1, fill="x")
leftcol = ttk.Frame(root)
leftcol.pack(side="left", expand=1, fill="both")
rightcol = ttk.Frame(root)
rightcol.pack(side="right", expand=1, fill="both")

# top row
ttk.Label(toprow, text="(debreceni adatok, mm-ben)").pack()
ttk.Label(toprow, text="(1901-2010)").pack()

# bottom row
# clouds, sun, etc icons here filling top row :)
ttk.Label(bottrow, text="test").pack()

# left column
evkerinput = tk.StringVar()
evkerinput.set("évszám")
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
ttk.Button(rightcol, text="Keresés", command=lambda: searchdata()).pack(anchor="e")

evi_csap_ossz = tk.StringVar()
ttk.Label(rightcol, textvariable=evi_csap_ossz).pack(anchor="e")

ebbol_hav = tk.StringVar()
ttk.Label(rightcol, textvariable=ebbol_hav).pack(anchor="e")

napi_csap_max = tk.StringVar()
ttk.Label(rightcol, textvariable=napi_csap_max).pack(anchor="e")

ttk.Label(rightcol, text="").pack(anchor="e")

adott_0_1 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_0_1).pack(anchor="e")

adott_1 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_1).pack(anchor="e")

adott_5 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_5).pack(anchor="e")

adott_10 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_10).pack(anchor="e")

adott_20 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_20).pack(anchor="e")

adott_30 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_30).pack(anchor="e")

adott_50 = tk.StringVar()
ttk.Label(rightcol, textvariable=adott_50).pack(anchor="e")

hav_nap = tk.StringVar()
ttk.Label(rightcol, textvariable=hav_nap).pack(anchor="e")

jeg_nap = tk.StringVar()
ttk.Label(rightcol, textvariable=jeg_nap).pack(anchor="e")

ziv_nap = tk.StringVar()
ttk.Label(rightcol, textvariable=ziv_nap).pack(anchor="e")

on_nap = tk.StringVar()
ttk.Label(rightcol, textvariable=on_nap).pack(anchor="e")

# gui handler
root.mainloop()
