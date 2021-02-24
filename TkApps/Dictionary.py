import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import csv


class MainFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side="top", expand=1, fill="both")
        self.topf = ttk.Frame(self, borderwidth=25)
        self.topf.pack(side="top", expand=1, fill="both")
        self.midf = ttk.Frame(self)
        self.midf.pack(side="bottom", expand=1, fill="both")
        self.scrollbar = ttk.Scrollbar(self.midf)
        self.scrollbar.pack(side="right", expand=1, fill="both")
        self.txtbox = tk.Text(self.midf, background="lightgrey", font=("Arial", 8), width=45, height=20,
                              relief="groove", borderwidth=1.5, yscrollcommand=self.scrollbar.set)
        self.txtbox.configure(state="disabled")
        self.txtbox.pack(side="left", expand=1, fill="both")
        self.scrollbar.config(command=self.txtbox.yview)

        self.kerinput = tk.StringVar()
        self.kerinput.set("")
        self.kerent = ttk.Entry(self.topf, textvariable=self.kerinput, validate="key", width=15, justify="left")
        self.kerent["validatecommand"] = (self.kerent.register(self.inputvalid), "%P", "%d")
        self.kerent.pack(side="top")

        self.taln = tk.StringVar()
        ttk.Label(self.topf, textvariable=self.taln).pack()

    def inputvalid(self, instr, acttyp):
        if acttyp == "1":
            with open("data/szotarak/enhu.csv", encoding="ansi") as csvfile:
                csvolv = csv.reader(csvfile, delimiter=";")
                ossztal = 0
                self.txtbox.configure(state="normal")
                self.txtbox.delete(1.0, tk.END)
                for row in csvolv:
                    if str(row[0]).find(instr) == 0:
                        taloutput = "\t".join(row) + "\n"
                        self.txtbox.insert(tk.END, *taloutput.splitlines(keepends=True))
                        ossztal += 1
                        self.taln.set(str(ossztal) + " találat")
                self.txtbox.configure(state="disabled")
                if ossztal == 0:
                    return False
        return True


class StyleConfig(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)

        # self.theme_use("classic")
        self.configure("TLabel", background="beige")
        self.configure("TEntry", foreground="blue", background="beige")
        self.configure("TButton", foreground="maroon", background="beige")
        self.configure("TFrame", background="beige", relief="groove")


def main():
    # GUI ROOT WINDOW
    root = tk.Tk()
    root.title("Dictionary")
    appicon = tk.PhotoImage(file="icons/tools-gramm.png")
    root.iconphoto(False, appicon)
    root.geometry("300x350")
    root.resizable(0, 0)
    root.config(background="beige")
    StyleConfig()
    MainFrame(root)
    # gui handler
    root.mainloop()


if __name__ == "__main__":
    main()
