import tkinter as tk
import tkinter.ttk as ttk
import func


class StatBar(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.configure(relief="flat")
        self.pack(side="top", fill="x")

        self.statleft = tk.StringVar()
        self.statleft.set("Not logged in (guest).")
        ttk.Label(self, textvariable=self.statleft).pack(side="left")
        self.statright = tk.StringVar()
        self.statright.set("")
        ttk.Label(self, textvariable=self.statright).pack(side="right")

        # List to store the items purchased, variables for checkout
        self.cart = []
        self.total_cost = 0
        self.flag = 0  # To check if they have been checked out
        # Logs
        self.wtolog = []
        self.wtoerrorlog = []
        # Current User
        self.curuser = ""


class TabLogin(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = TabMenu()
        # self.status = StatBar(master)
        self.pack(expand=1, fill="both")
        # BG IMG
        self.bgimg = tk.PhotoImage(file="icons/menubgimg.png")
        self.bg = ttk.Label(self, image=self.bgimg)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
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

        ttk.Button(self.form, text="Login", command=None).pack(pady=4)
        # new account btn


class TabCart(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = MainAppWind()
        # self.status = StatBar(master)

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
        self.btnsearch = ttk.Button(self.menu, text="Search item", command=func.searchitem)
        self.btnlistall = ttk.Button(self.menu, text="List all items", command=lambda: func.listallitems(statself=StatBar, tabself=self))
        # sep
        self.btnaddcart = ttk.Button(self.menu, text="Add to cart", command=None)
        self.btnremovecart = ttk.Button(self.menu, text="Remove from cart", command=None)
        self.btnshowcart = ttk.Button(self.menu, text="Show cart", command=None)
        self.btncheckout = ttk.Button(self.menu, text="Checkout", command=None)
        # sep
        self.btnexit = ttk.Button(self.menu, text="Exit", command=None)

        # self.vmibtn.pack(fill="x", pady=5)
        # ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=15)
        self.btnsearch.pack(fill="x", pady=5)
        self.btnlistall.pack(fill="x", pady=5)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=15)
        self.btnaddcart.pack(fill="x", pady=5)
        self.btnremovecart.pack(fill="x", pady=5)
        self.btnshowcart.pack(fill="x", pady=5)
        self.btncheckout.pack(fill="x", pady=5)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=15)
        self.btnexit.pack(fill="x", pady=5)


class TabStock(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = MainAppWind()
        # self.status = StatBar(master)

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

        # self.vmibtn.pack(fill="x", pady=5)
        # ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=15)
        self.btnsearch.pack(fill="x", pady=5)
        self.btnlistall.pack(fill="x", pady=5)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=15)
        self.btnadditem.pack(fill="x", pady=5)
        self.btnedititem.pack(fill="x", pady=5)
        self.btnremoveitem.pack(fill="x", pady=5)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=15)
        self.btnexit.pack(fill="x", pady=5)
