import tkinter.ttk as ttk
from func import *


class MainAppWind(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        # statbar
        # StatBar(self)

        # tabmenu
        self.tabmenu = ttk.Notebook(self)
        self.tabmenu.pack(expand=1, fill="both")
        self.tablogin = TabLogin(self)
        self.tabcart = TabCart(self)
        self.tabstock = TabStock(self)
        self.tabmenu.add(self.tablogin, text="Login")
        self.tabmenu.add(self.tabcart, text="Cart", state="disabled")
        self.tabmenu.add(self.tabstock, text="Stock", state="disabled")


'''class StatBar(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = MainAppWind()

        self.configure(relief="flat")
        self.statleft = tk.StringVar()
        self.statleft.set("Not logged in (guest).")
        ttk.Label(self, textvariable=self.statleft).pack(side="left")
        self.statright = tk.StringVar()
        self.statright.set("")
        ttk.Label(self, textvariable=self.statright).pack(side="right")'''


class TabLogin(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

        # BG IMG
        self.bgimg = tk.PhotoImage(file="icons/menubgimg.png")
        self.bg = ttk.Label(self, image=self.bgimg)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        '''# statbar
        self.statbar = ttk.Label(self, text="asdfjklé")
        self.statbar.place(relx=0, rely=0, relwidth=1, relheight=0.1)'''

        # FORM
        self.form = ttk.Frame(self, style="LoginF.TFrame", borderwidth=20)
        self.form.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)

        self.formusernlabel = ttk.Labelframe(self.form, text="Username")
        self.formusernlabel.pack(pady=2)
        self.entusern = tk.StringVar()
        self.entusern.set("")
        ttk.Entry(self.formusernlabel, textvariable=self.entusern).pack()

        self.formpasswlabel = ttk.Labelframe(self.form, text="Password")
        self.formpasswlabel.pack(pady=2)
        self.entpassw = tk.StringVar()
        self.entpassw.set("")
        ttk.Entry(self.formpasswlabel, textvariable=self.entpassw, show="*").pack()

        ttk.Button(self.form, text="Login", command=lambda: login(tabself=self)).pack(pady=4)
        # new account btn


class TabCart(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master
        '''self.statbar = ttk.Label(self, text="asdfjklé")
        self.statbar.pack(side="top", expand=1, fill="x")'''

        self.menu = ttk.Frame(self, width=150, borderwidth=5)
        self.outp = ttk.Frame(self, borderwidth=5)
        self.menu.pack(side="left", fill="y")
        self.outp.pack(side="right", expand=1, fill="both")

        # OUTP ELEMENTS
        self.scrbar = ttk.Scrollbar(self.outp)
        self.scrbar.pack(side="right", fill="y")
        self.tree = ttk.Treeview(self.outp, column=("column1", "column2", "column3", "column4"), show='headings',
                                 selectmode="browse", height=13, yscrollcommand=self.scrbar.set)
        self.tree.column("#1", width=80, minwidth=80, stretch=0)
        self.tree.column("#2", width=80, minwidth=80, stretch=0)
        self.tree.column("#3", width=240, minwidth=240, stretch=0)
        self.tree.column("#4", width=40, minwidth=40, stretch=0)
        self.tree.heading("#1", text="Item ID")
        self.tree.heading("#2", text="Unit price")
        self.tree.heading("#3", text="Description")
        self.tree.heading("#4", text="Stock")
        self.tree.pack(side="left", expand=1, fill="both")
        self.scrbar.config(command=self.tree.yview)

        # ha kéne vmiért frame or label placed over menu vagy outp??
        '''self.menubox = ttk.Frame(self.menu)
        self.menubox.place(relx=0, rely=0.15, relwidth=1, relheight=0.75)
        ttk.Label(self.menubox)'''

        '''self.outpbox = ttk.Frame(self.outp)
        ttk.Label(self.outpbox)'''

        # MENU ELEMENTS & FUNCS
        # self.vmibtn = ttk.Button(self.menu, text="Login", command=None)
        # sep
        self.btnsearch = ttk.Button(self.menu, text="Search item", command=None)
        self.btnlistall = ttk.Button(self.menu, text="List all items", command=lambda: listallitems(tabself=self))
        # sep
        self.btnaddcart = ttk.Button(self.menu, text="Add to cart", command=None)
        self.btnremovecart = ttk.Button(self.menu, text="Remove from cart", command=None)
        self.btnshowcart = ttk.Button(self.menu, text="Show cart", command=None)
        self.btncheckout = ttk.Button(self.menu, text="Checkout", command=None)
        # sep
        self.btnexit = ttk.Button(self.menu, text="Exit", command=None)

        # self.vmibtn.pack(fill="x", pady=4)
        # ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnsearch.pack(fill="x", pady=4)
        self.btnlistall.pack(fill="x", pady=4)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnaddcart.pack(fill="x", pady=4)
        self.btnremovecart.pack(fill="x", pady=4)
        self.btnshowcart.pack(fill="x", pady=4)
        self.btncheckout.pack(fill="x", pady=4)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnexit.pack(fill="x", pady=4)


class TabStock(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master
        '''self.statbar = ttk.Label(self, text="asdfjklé")
        self.statbar.pack(side="top", expand=1, fill="x")'''

        self.menu = ttk.Frame(self, width=150, borderwidth=5)
        self.outp = ttk.Frame(self, borderwidth=5)
        self.menu.pack(side="left", fill="y")
        self.outp.pack(side="right", expand=1, fill="both")

        # OUTP ELEMENTS
        self.scrbar = ttk.Scrollbar(self.outp)
        self.scrbar.pack(side="right", fill="y")
        self.tree = ttk.Treeview(self.outp, column=("column1", "column2", "column3", "column4"), show='headings',
                                 selectmode="browse", height=13, yscrollcommand=self.scrbar.set)
        self.tree.column("#1", width=80, minwidth=80, stretch=0)
        self.tree.column("#2", width=80, minwidth=80, stretch=0)
        self.tree.column("#3", width=240, minwidth=240, stretch=0)
        self.tree.column("#4", width=40, minwidth=40, stretch=0)
        self.tree.heading("#1", text="Item ID")
        self.tree.heading("#2", text="Unit price")
        self.tree.heading("#3", text="Description")
        self.tree.heading("#4", text="Stock")
        self.tree.pack(side="left", expand=1, fill="both")
        self.scrbar.config(command=self.tree.yview)

        # ha kéne vmiért frame or label placed over menu vagy outp??
        '''self.menubox = ttk.Frame(self.menu)
        self.menubox.place(relx=0, rely=0.15, relwidth=1, relheight=0.75)
        ttk.Label(self.menubox)'''

        '''self.outpbox = ttk.Frame(self.outp)
        ttk.Label(self.outpbox)'''

        # MENU ELEMENTS & FUNCS
        # self.vmibtn = ttk.Button(self.menu, text="Login", command=None)
        # sep
        self.btnsearch = ttk.Button(self.menu, text="Search item", command=None)
        self.btnlistall = ttk.Button(self.menu, text="List all items", command=None)
        # sep
        self.btnadditem = ttk.Button(self.menu, text="Add item", command=None)
        self.btnedititem = ttk.Button(self.menu, text="Edit item", command=None)
        self.btnremoveitem = ttk.Button(self.menu, text="Remove item", command=None)
        # sep
        self.btnexit = ttk.Button(self.menu, text="Exit", command=None)

        # self.vmibtn.pack(fill="x", pady=4)
        # ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnsearch.pack(fill="x", pady=4)
        self.btnlistall.pack(fill="x", pady=4)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnadditem.pack(fill="x", pady=4)
        self.btnedititem.pack(fill="x", pady=4)
        self.btnremoveitem.pack(fill="x", pady=4)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnexit.pack(fill="x", pady=4)


class StyleConfig(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.configure("TNotebook.Tab", width=15, padding=(4, 2, 4, 2))
        self.map("TNotebook.Tab", foreground=[("active", "maroon")])
        self.configure("TFrame", background="silver", relief="groove")
        self.configure("LoginF.TFrame", background="beige")
        self.configure("TLabelframe", background="beige")
        self.configure("TButton", foreground="black", background="white", padding=4)
        self.map("TButton", foreground=[("active", "maroon")], background=[("active", "coral")])
        self.configure("TLabel", background="silver")
        self.configure("TEntry", foreground="blue", background="silver")
        self.configure("TMenubutton", background="silver")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("InventoryManager - Inventory Management Tools - Dave")
    root.appicon = tk.PhotoImage(file="icons/imsicon.png")
    root.iconphoto(False, root.appicon)
    root.geometry("636x363")
    root.resizable(0, 0)
    StyleConfig()
    mainwind = MainAppWind(root)
    root.mainloop()
