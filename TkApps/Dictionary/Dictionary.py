import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import sqlite3


class MainFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side="top", expand=1, fill="both")

        self.botf = ttk.Frame(self, relief="flat")
        self.botf.pack(side="bottom", expand=0, fill="x")
        self.topf = ttk.Frame(self, borderwidth=10)
        self.topf.pack(side="top", expand=1, fill="both")
        self.midf = ttk.Frame(self)
        self.midf.pack(side="bottom", expand=1, fill="both")

        # TOPF
        self.topf.grid_columnconfigure(4, weight=1)
        ttk.Label(self.topf, text="Keresés nyelve:").grid(row=1, column=1)
        self.kerlang = tk.StringVar()
        self.kerlang.set("eng")
        ttk.Radiobutton(self.topf, text="Angol", variable=self.kerlang, value="eng").grid(row=1, column=2, sticky="w")
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
        self.kerent = tk.StringVar()
        self.kerent.set("")
        ent = ttk.Entry(self.topf, textvariable=self.kerent, width=20)
        ent.grid(row=5, column=2, sticky="w")
        ent.bind("<Return>", self.kerinput)
        ent.focus()
        ttk.Button(self.topf, text="Keresés", command=self.kerinput).grid(row=5, column=3)

        # MIDF
        self.scrbar = ttk.Scrollbar(self.midf)
        self.scrbar.pack(side="right", fill="y")
        self.tree = ttk.Treeview(self.midf, column=("column1", "column2"), show='headings', height=20,
                                 yscrollcommand=self.scrbar.set)
        self.tree.heading("#1", text="English")
        self.tree.heading("#2", text="Magyar")
        self.tree.pack(side="left", expand=1, fill="both")
        self.scrbar.config(command=self.tree.yview)

        # BOTF
        self.statlab = tk.StringVar()
        self.statlab.set("")
        ttk.Label(self.botf, textvariable=self.statlab).pack(side="left")

    def opendict(self):
        con = sqlite3.connect("data/dict.db")
        with con:
            cur = con.cursor()
            for row in cur.execute("SELECT * FROM dict"):
                self.tree.insert("", tk.END, values=row)

    def kerinput(self, event=None):
        self.statlab.set("Keresés...")
        self.botf.update_idletasks()  # sima update helyett!!
        lang = self.kerlang.get()
        ker = self.kerent.get()
        mod = self.kermod.get()
        self.tree.delete(*self.tree.get_children())
        con = sqlite3.connect("data/dict.db")
        with con:
            cur = con.cursor()
            if mod == "teljes":
                if lang == "eng":
                    cur.execute("SELECT * FROM dict WHERE eng LIKE ?", (ker, ))
                if lang == "hun":
                    cur.execute("SELECT * FROM dict WHERE hun LIKE ?", (ker, ))
            elif mod == "eleje":
                if lang == "eng":
                    cur.execute("SELECT * FROM dict WHERE eng LIKE ?", (ker + "%", ))
                if lang == "hun":
                    cur.execute("SELECT * FROM dict WHERE hun LIKE ?", (ker + "%", ))
            elif mod == "mindegy":
                if lang == "eng":
                    cur.execute("SELECT * FROM dict WHERE eng LIKE ?", ("%" + ker + "%", ))
                if lang == "hun":
                    cur.execute("SELECT * FROM dict WHERE hun LIKE ?", ("%" + ker + "%", ))
            else:
                messagebox.showerror(None, "Hiba!")
            rows = cur.fetchall()
            for row in rows:
                self.tree.insert("", tk.END, values=row)
            if len(rows) == 0:
                self.statlab.set("Nincs találat!")
            else:
                self.statlab.set(str(len(rows)) + " találat")


class StyleConfig(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)

        self.configure("TLabel", background="beige")
        self.configure("TEntry", foreground="blue", background="beige")
        self.configure("TFrame", background="beige", relief="groove")
        self.configure("TRadiobutton", background="beige")
        self.configure("TMenubutton", background="beige")


def main():
    # GUI ROOT WINDOW
    root = tk.Tk()
    root.title("Dictionary - Szótár (angol-magyar nagyszótár)")
    appicon = tk.PhotoImage(file="icons/dicticon.png")
    root.iconphoto(False, appicon)
    root.geometry("560x480")
    root.resizable(0, 0)
    root.config(background="beige")
    StyleConfig()
    MainFrame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
