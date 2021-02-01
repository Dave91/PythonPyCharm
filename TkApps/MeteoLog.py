import tkinter as tk
from tkinter import ttk
import csv


# ROOT WINDOW DETAILS
root = tk.Tk()
root.title("MeteoLog")
root.geometry("320x320")
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
style.configure("TLabel", background="beige")
style.configure("TEntry", foreground="blue")
style.configure("TButton", background="gold")
style.configure("TFrame", background="beige")

root.mainloop()




def search_data():
    with open('DE_Y_r.csv') as csvfile:
        evker = str(input("Keresett év: "))
        csvolv = csv.reader(csvfile, delimiter=';')
        match = 0
        print('(Az adatok Debrecenre vonatkoznak és mm-ben értendők.)')
        for row in csvolv:
            if evker in row:
                print(f'Vizsgált év: {row[0]}')
                print(f'Évi csapadékösszeg: {row[1]} (ebből havazás: {row[2]})')
                print(f'Napi csapadék maximum: {row[3]} ({row[4]})')
                print(f'Adott csapadékösszegű napok száma (0,1-1-5-10-20-30-50mm):'
                      f'\n\t{row[5]}-{row[6]}-{row[7]}-{row[8]}-{row[9]}-{row[10]}-{row[11]}')
                print(f'Havas napok száma: {row[12]}')
                print(f'Jeges napok száma: {row[13]}')
                print(f'Zivataros napok száma: {row[14]}')
                print(f'Ónosesős napok száma: {row[15]}')
                match += 1
        if match == 0:
            print('Hiba: keresett év nem található!')
        csvfile.close()
