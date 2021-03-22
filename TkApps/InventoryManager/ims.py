import tkinter as tk
import tkinter.ttk as ttk
from pages import *
import func


class MainAppWind(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("InventoryManager - Inventory Management System - Dave")
        appicon = tk.PhotoImage(file="icons/imsicon.png")
        self.iconphoto(False, appicon)
        self.geometry("686x343")
        self.resizable(0, 1)

        StyleConfig()
        self.statbar = StatBar(self)
        self.tabmenu = self.TabMenu(self)

    class TabMenu(ttk.Notebook):
        def __init__(self, master):
            ttk.Notebook.__init__(self, master)
            self.master = master
            # self.configure(style="lefttab.TNotebook")
            self.pack(expand=1, fill="both")

            self.tablogin = TabLogin(self)
            self.tabcart = TabCart(self)
            self.tabstock = TabStock(self)
            self.add(self.tablogin, text="Login")
            self.add(self.tabcart, text="Cart")
            self.add(self.tabstock, text="Stock")


class StyleConfig(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.configure("TNotebook.Tab", width=15, padding=(4, 2, 4, 2))
        self.map("TNotebook.Tab", foreground=[("active", "maroon")])
        self.configure("TFrame", background="silver", relief="groove")
        self.configure("LoginF.TFrame", background="beige")
        self.configure("TLabelframe", background="beige")
        self.configure("TButton", foreground="black", background="white", padding=5)
        self.map("TButton", foreground=[("active", "maroon")], background=[("active", "coral")])
        self.configure("TLabel", background="silver")
        self.configure("TEntry", foreground="blue", background="silver")
        self.configure("TMenubutton", background="silver")


if __name__ == "__main__":
    gui = MainAppWind()
    gui.mainloop()
