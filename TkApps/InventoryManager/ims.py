import datetime
import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog


class MainAppWind(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        # statbar
        self.statbar = StatBar(self)

        # tabmenu
        self.tabmenu = ttk.Notebook(self)
        self.tabmenu.pack(expand=1, fill="both")

        self.tablogin = TabLogin(self)
        self.tabguest = TabGuest(self)
        self.tabacc = TabAcc(self)
        self.tabstock = TabStock(self)
        self.tabcart = TabCart(self)
        self.tabadminacc = TabAdminAcc(self)
        self.tabadminstock = TabAdminStock(self)
        self.tabadmincart = TabAdminCart(self)
        self.tabadminusers = TabAdminUsers(self)

        self.tabmenu.add(self.tablogin, text="Login")
        self.tabmenu.add(self.tabguest, text="Browse as guest")
        self.tabmenu.add(self.tabacc, text="User Account", state="hidden")
        self.tabmenu.add(self.tabstock, text="Stock", state="hidden")
        self.tabmenu.add(self.tabcart, text="Cart", state="hidden")
        self.tabmenu.add(self.tabadminacc, text="Account (admin)", state="hidden")
        self.tabmenu.add(self.tabadminstock, text="Stock (admin)", state="hidden")
        self.tabmenu.add(self.tabadmincart, text="Carts (admin)", state="hidden")
        self.tabmenu.add(self.tabadminusers, text="Users (admin)", state="hidden")


class StatBar(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master
        self.configure(relief="flat")
        self.pack(fill="x")
        self.statleft = tk.StringVar()
        self.statleft.set("Not logged in (guest).")
        ttk.Label(self, textvariable=self.statleft).pack(side="left")
        self.statright = tk.StringVar()
        self.statright.set("Welcome!")
        ttk.Label(self, textvariable=self.statright).pack(side="right")


class TabLogin(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

        # BG IMG
        self.bgimg = tk.PhotoImage(file="images/menubgimg.png")
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

        ttk.Button(self.form, text="Login", command=lambda: login(tabself=self)).pack(pady=4)
        # new account btn


class TabGuest(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

        self.menu = ttk.Frame(self, width=150, borderwidth=5)
        self.outp = ttk.Frame(self, borderwidth=5)
        self.menu.pack(side="left", fill="y")
        self.outp.pack(side="right", expand=1, fill="both")

        # OUTP ELEMENTS
        self.scrbar = ttk.Scrollbar(self.outp)
        self.scrbar.pack(side="right", fill="y")
        self.tree = ttk.Treeview(self.outp, column=("column1", "column2", "column3", "column4"), show='headings',
                                 selectmode="browse", height=13, yscrollcommand=self.scrbar.set)
        self.tree.column("#1", width=80, stretch=0)  # anchor="center" v "e" igazításhoz!!
        self.tree.column("#2", width=80, stretch=0)
        self.tree.column("#3", width=240, stretch=0)
        self.tree.column("#4", width=40, stretch=0)
        self.tree.heading("#1", text="Item ID")
        self.tree.heading("#2", text="Price")
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
        self.btnsearch = ttk.Button(self.menu, text="Search item", command=None)
        self.btnlistall = ttk.Button(self.menu, text="List all items", command=lambda: listallitems(tabself=self))
        # sep
        self.btnexit = ttk.Button(self.menu, text="Exit", command=None)

        self.btnsearch.pack(fill="x", pady=4)
        self.btnlistall.pack(fill="x", pady=4)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnexit.pack(fill="x", pady=4)


class TabAcc(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

        self.menu = ttk.Frame(self, width=150, borderwidth=5)
        self.outp = ttk.Frame(self, borderwidth=5, style="LoginF.TFrame")
        self.menu.pack(side="left", fill="y")
        self.outp.pack(side="right", expand=1, fill="both")

        # MENU
        self.profilimg = tk.PhotoImage(file="images/Dave.png").subsample(4)
        self.profil = ttk.Label(self.menu, image=self.profilimg)
        self.profil.pack(fill="x")
        ttk.Label(self.menu, text="Name:\nDave\nPosition:\nJunior Programmer\nGroup:\nSoftware Development").pack()
        ttk.Button(self.menu, text="Logout", command=lambda: logout(tabself=self)).pack(pady=4)

        # OUTP
        self.actpasswlabel = ttk.Labelframe(self.outp, text="Actual Password")
        self.actpasswlabel.pack(pady=2)
        self.entactpassw = tk.StringVar()
        self.entactpassw.set("")
        ttk.Entry(self.actpasswlabel, textvariable=self.entactpassw).pack()

        self.newpasswlabel = ttk.Labelframe(self.outp, text="New Password")
        self.newpasswlabel.pack(pady=2)
        self.entnewpassw = tk.StringVar()
        self.entnewpassw.set("")
        ttk.Entry(self.newpasswlabel, textvariable=self.entnewpassw, show="*").pack()

        ttk.Button(self.outp, text="Change Password", command=lambda: changepassw(tabself=self)).pack(pady=4)

        self.contactinfolabel = ttk.Labelframe(self.outp, text="Contact Info")
        self.contactinfolabel.pack(pady=4)
        self.labemail = ttk.Label(self.contactinfolabel, text="", style="AccL.TLabel")
        self.labemail.pack()
        self.labaddress = ttk.Label(self.contactinfolabel, text="", style="AccL.TLabel")
        self.labaddress.pack()

        ttk.Button(self.outp, text="Update Contact Info", command=lambda: changecontact(tabself=self)).pack()


class TabStock(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

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
        self.tree.heading("#2", text="Price")
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
        self.btnsearch = ttk.Button(self.menu, text="Search item", command=None)
        self.btnlistall = ttk.Button(self.menu, text="List all items", command=lambda: listallitems(tabself=self))
        # sep
        self.btnaddcart = ttk.Button(self.menu, text="Add to cart", command=lambda: addtocart(tabself=self))
        # sep
        self.btnadditem = ttk.Button(self.menu, text="Add item", command=None)
        self.btnedititem = ttk.Button(self.menu, text="Edit item", command=None)
        self.btnremoveitem = ttk.Button(self.menu, text="Remove item", command=lambda: removeitem(tabself=self))

        self.btnsearch.pack(fill="x", pady=4)
        self.btnlistall.pack(fill="x", pady=4)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnaddcart.pack(fill="x", pady=4)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnadditem.pack(fill="x", pady=4)
        self.btnedititem.pack(fill="x", pady=4)
        self.btnremoveitem.pack(fill="x", pady=4)


class TabCart(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

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
        self.tree.heading("#2", text="Price")
        self.tree.heading("#3", text="Description")
        self.tree.heading("#4", text="Amount")
        self.tree.pack(side="left", expand=1, fill="both")
        self.scrbar.config(command=self.tree.yview)

        # ha kéne vmiért frame or label placed over menu vagy outp??
        '''self.menubox = ttk.Frame(self.menu)
        self.menubox.place(relx=0, rely=0.15, relwidth=1, relheight=0.75)
        ttk.Label(self.menubox)'''

        '''self.outpbox = ttk.Frame(self.outp)
        ttk.Label(self.outpbox)'''

        # MENU ELEMENTS & FUNCS
        self.btnshowcart = ttk.Button(self.menu, text="Show cart", command=lambda: showcart(tabself=self))
        self.btncheckout = ttk.Button(self.menu, text="Checkout", command=None)
        self.btnremovecart = ttk.Button(self.menu, text="Remove from cart",
                                        command=lambda: removefromcart(tabself=self))
        self.btnclearcart = ttk.Button(self.menu, text="Clear cart", command=lambda: clearcart(tabself=self))

        self.btnshowcart.pack(fill="x", pady=4)
        self.btncheckout.pack(fill="x", pady=4)
        self.btnremovecart.pack(fill="x", pady=4)
        self.btnclearcart.pack(fill="x", pady=4)

    def cartvmi(self):
        pass


class TabAdminAcc(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

        self.menu = ttk.Frame(self, width=150, borderwidth=5)
        self.outp = ttk.Frame(self, borderwidth=5, style="LoginF.TFrame")
        self.menu.pack(side="left", fill="y")
        self.outp.pack(side="right", expand=1, fill="both")

        # MENU
        self.profilimg = tk.PhotoImage(file="images/admin.png").subsample(3)
        self.profil = ttk.Label(self.menu, image=self.profilimg)
        self.profil.pack(fill="x")
        ttk.Label(self.menu, text="Name:\nadmin\nPosition:\nadmin\nGroup:\nadmin").pack()
        ttk.Button(self.menu, text="Logout", command=lambda: logout(tabself=self)).pack(pady=4)

        # OUTP
        self.actpasswlabel = ttk.Labelframe(self.outp, text="Actual Password")
        self.actpasswlabel.pack(pady=2)
        self.entactpassw = tk.StringVar()
        self.entactpassw.set("")
        ttk.Entry(self.actpasswlabel, textvariable=self.entactpassw).pack()

        self.newpasswlabel = ttk.Labelframe(self.outp, text="New Password")
        self.newpasswlabel.pack(pady=2)
        self.entnewpassw = tk.StringVar()
        self.entnewpassw.set("")
        ttk.Entry(self.newpasswlabel, textvariable=self.entnewpassw, show="*").pack()

        ttk.Button(self.outp, text="Change Password", command=lambda: changepassw(tabself=self)).pack(pady=4)

        self.contactinfolabel = ttk.Labelframe(self.outp, text="Contact Info")
        self.contactinfolabel.pack(pady=4)
        self.labemail = ttk.Label(self.contactinfolabel, text="", style="AccL.TLabel")
        self.labemail.pack()
        self.labaddress = ttk.Label(self.contactinfolabel, text="", style="AccL.TLabel")
        self.labaddress.pack()

        ttk.Button(self.outp, text="Update Contact Info", command=lambda: changecontact(tabself=self)).pack()


class TabAdminStock(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

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
        self.tree.heading("#2", text="Price")
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
        self.btnsearch = ttk.Button(self.menu, text="Search item", command=None)
        self.btnlistall = ttk.Button(self.menu, text="List all items", command=lambda: listallitems(tabself=self))
        # sep
        self.btnaddcart = ttk.Button(self.menu, text="Add to cart", command=lambda: addtocart(tabself=self))
        # sep
        self.btnadditem = ttk.Button(self.menu, text="Add item", command=None)
        self.btnedititem = ttk.Button(self.menu, text="Edit item", command=None)
        self.btnremoveitem = ttk.Button(self.menu, text="Remove item", command=lambda: removeitem(tabself=self))

        self.btnsearch.pack(fill="x", pady=4)
        self.btnlistall.pack(fill="x", pady=4)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnaddcart.pack(fill="x", pady=4)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnadditem.pack(fill="x", pady=4)
        self.btnedititem.pack(fill="x", pady=4)
        self.btnremoveitem.pack(fill="x", pady=4)


class TabAdminCart(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

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
        self.tree.heading("#2", text="Price")
        self.tree.heading("#3", text="Description")
        self.tree.heading("#4", text="Amount")
        self.tree.pack(side="left", expand=1, fill="both")
        self.scrbar.config(command=self.tree.yview)

        # ha kéne vmiért frame or label placed over menu vagy outp??
        '''self.menubox = ttk.Frame(self.menu)
        self.menubox.place(relx=0, rely=0.15, relwidth=1, relheight=0.75)
        ttk.Label(self.menubox)'''

        '''self.outpbox = ttk.Frame(self.outp)
        ttk.Label(self.outpbox)'''

        # MENU ELEMENTS & FUNCS

        self.btnshowcart = ttk.Button(self.menu, text="Show cart", command=lambda: showcart(tabself=self))
        self.btncheckout = ttk.Button(self.menu, text="Checkout", command=None)
        self.btnremovecart = ttk.Button(self.menu, text="Remove from cart",
                                        command=lambda: removefromcart(tabself=self))
        self.btnclearcart = ttk.Button(self.menu, text="Clear cart", command=lambda: clearcart(tabself=self))

        self.btnshowcart.pack(fill="x", pady=4)
        self.btncheckout.pack(fill="x", pady=4)
        self.btnremovecart.pack(fill="x", pady=4)
        self.btnclearcart.pack(fill="x", pady=4)

    def cartvmi(self):
        pass


class TabAdminUsers(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

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
        self.tree.heading("#1", text="Username")
        self.tree.heading("#2", text="Password")
        self.tree.heading("#3", text="vmi1")
        self.tree.heading("#4", text="vmi2")
        self.tree.pack(side="left", expand=1, fill="both")
        self.scrbar.config(command=self.tree.yview)

        # ha kéne vmiért frame or label placed over menu vagy outp??
        '''self.menubox = ttk.Frame(self.menu)
        self.menubox.place(relx=0, rely=0.15, relwidth=1, relheight=0.75)
        ttk.Label(self.menubox)'''

        '''self.outpbox = ttk.Frame(self.outp)
        ttk.Label(self.outpbox)'''

        # MENU ELEMENTS & FUNCS
        self.btnlistallusers = ttk.Button(self.menu, text="List all users", command=self.listallusers)
        self.btnadduser = ttk.Button(self.menu, text="Register user", command=self.adduser)
        self.btnedituser = ttk.Button(self.menu, text="Edit user data", command=self.edituser)
        self.btnremoveuser = ttk.Button(self.menu, text="Remove user", command=self.removeuser)

        self.btnlistallusers.pack(fill="x", pady=4)
        self.btnadduser.pack(fill="x", pady=4)
        self.btnedituser.pack(fill="x", pady=4)
        self.btnremoveuser.pack(fill="x", pady=4)

    def listallusers(self):
        self.tree.delete(*self.tree.get_children())
        try:
            con = sqlite3.connect("data/stock.db")
            try:
                cur = con.cursor()
                cur.execute("SELECT username, password FROM users WHERE username != 'admin'")
                rows = cur.fetchall()
                for row in rows:
                    self.tree.insert("", "end", values=row)
                if len(rows) == 0:
                    self.master.statbar.statright.set("No users found!")
                self.master.statbar.statright.set("All users listed: " + str(len(rows)))
            finally:
                con.close()
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(self) + " - listallusers")
            self.master.statbar.statright.set("An error occurred! Details logged.")

    def adduser(self):
        try:
            con = sqlite3.connect("data/stock.db")
            try:
                cur = con.cursor()
                usern = simpledialog.askstring(None, "Enter username:")
                cur.execute("SELECT * FROM users WHERE username = ?", (usern,))
                if len(cur.fetchall()) != 0:
                    messagebox.showwarning(None, "Username already exists: choose other name or edit user!")
                else:
                    passw = simpledialog.askstring(None, "Enter password:")
                    cur.execute("INSERT INTO users(username, password) VALUES (?, ?)", (usern, passw,))
                    con.commit()
                    self.master.statbar.statright.set("User account added!")
            finally:
                con.close()
                self.listallusers()
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(self) + " - adduser")
            self.master.statbar.statright.set("An error occurred! Details logged.")

    def edituser(self):
        selinput = self.tree.selection()
        if len(selinput) != 0:
            try:
                con = sqlite3.connect("data/stock.db")
                try:
                    cur = con.cursor()
                    selusern = self.tree.item(selinput, "values")[0]
                    selpassw = self.tree.item(selinput, "values")[1]
                    newusern = simpledialog.askstring(None, "Enter new username:", initialvalue=selusern)
                    newpassw = simpledialog.askstring(None, "Enter new password:", initialvalue=selpassw)
                    cur.execute("UPDATE users SET username = ?, password = ? WHERE username = ?",
                                (newusern, newpassw, selusern,))
                    con.commit()
                    self.master.statbar.statright.set("User data modified!")
                finally:
                    con.close()
                    self.listallusers()
            except (sqlite3.Error, tk.TclError) as errn:
                errorlog(error=str(errn), funcname=str(self) + " - edituser")
                self.master.statbar.statright.set("An error occurred! Details logged.")

    def removeuser(self):
        selinput = self.tree.selection()
        if len(selinput) != 0:
            are_you_sure = messagebox.askyesno(None, "Are you sure to remove this user account?")
            if are_you_sure is True:
                try:
                    con = sqlite3.connect("data/stock.db")
                    try:
                        cur = con.cursor()
                        selusern = self.tree.item(selinput, "values")[0]
                        cur.execute("DELETE FROM users WHERE username = ?",
                                    (selusern,))
                        con.commit()
                        self.master.statbar.statright.set("User account removed!")
                    finally:
                        con.close()
                        self.listallusers()
                except (sqlite3.Error, tk.TclError) as errn:
                    errorlog(error=str(errn), funcname=str(self) + " - removeuser")
                    self.master.statbar.statright.set("An error occurred! Details logged.")


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
        self.configure("AccL.TLabel", background="beige")
        self.configure("TEntry", foreground="blue", background="silver")
        self.configure("TMenubutton", background="silver")


class FuncVars:
    # List to store the items purchased, variables for checkout
    cart = []
    total_cost = 0
    flag = 0  # To check if they have been checked out
    # Logs
    wtolog = []
    wtoerrorlog = []
    # Current User
    curuser = "guest"


def searchitem(tabself):
    kerinput = simpledialog.askstring(None, "Enter item ID:")
    tabself.delete(*tabself.tree.get_children())
    try:
        con = sqlite3.connect("data/stock.db")
        try:
            cur = con.cursor()
            cur.execute("SELECT item_number, item_price, item_desc, item_stock FROM items WHERE item_number LIKE ?",
                        (kerinput + "%",))
            rows = cur.fetchall()
            for row in rows:
                tabself.tree.insert("", "end", values=row)
            if len(rows) == 0:
                messagebox.showwarning(None, "Nincs találat!")
            else:
                tabself.master.statbar.statright.set("Item found!")
        finally:
            con.close()
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - searchitem")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")


def sortbyheader(tabself, sortbycol):
    tabself.tree.delete(*tabself.tree.get_children())
    try:
        con = sqlite3.connect("data/stock.db")
        try:
            cur = con.cursor()
            if sortbycol == "item_number":
                cur.execute("SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_number ASC")
            if sortbycol == "item_price":
                cur.execute("SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_price ASC")
            if sortbycol == "item_desc":
                cur.execute("SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_desc ASC")
            if sortbycol == "item_stock":
                cur.execute("SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_stock ASC")
            rows = cur.fetchall()
            for row in rows:
                tabself.tree.insert("", "end", values=row)
            if len(rows) == 0:
                messagebox.showwarning(None, "Nincs találat!")
            tabself.master.statbar.statright.set("Sorted by: " + str(sortbycol))
        finally:
            con.close()
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - sortbyheader")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")


def listallitems(tabself):
    tabself.tree.delete(*tabself.tree.get_children())
    try:
        con = sqlite3.connect("data/stock.db")
        try:
            cur = con.cursor()
            cur.execute("SELECT item_number, item_price, item_desc, item_stock FROM items")
            rows = cur.fetchall()
            for row in rows:
                tabself.tree.insert("", "end", values=row)
            if len(rows) == 0:
                tabself.master.statbar.statright.set("No items found!")
            tabself.master.statbar.statright.set("All items listed: " + str(len(rows)))
        finally:
            con.close()
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - listallitems")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")


def additem(self):
    p_no = simpledialog.askinteger(None, "Enter item number: ")
    p_pr = simpledialog.askfloat(None, "Enter item price: ")
    p_desc = simpledialog.askstring(None, "Enter item description: ")
    p_stock = simpledialog.askinteger(None, "Enter item stock: ")

    m = 0
    for i in range(0, len(self.unit_price)):
        if p_no in self.unit_price:
            p_no += 1
            m = 1
    if m == 1:
        messagebox.showwarning(None, "That item number already exists! Changing value to " + str(p_no))

    self.unit_price.update({p_no: p_pr})
    self.description.update({p_no: p_desc})
    if p_stock > -1:
        self.stock.update({p_no: p_stock})
    else:
        p_stock = 0
        self.stock.update({p_no: p_stock})
        messagebox.showwarning(None, "The stock of an item cannot be negative, the stock has been set to 0.")
    messagebox.showinfo(None, "Item number: " + str(p_no) + "\nDescription: " + self.description.get(p_no)
                        + "\nPrice: " + self.unit_price.get(p_no) + "\nStock: " + self.stock.get(p_no))
    messagebox.showinfo(None, "Item added successfully!")


def edititem(self):
    p_no = simpledialog.askinteger(None, "Enter item number: ")
    if p_no in self.unit_price:
        p_pr = simpledialog.askfloat(None, "Enter item price: ")
        p_desc = simpledialog.askstring(None, "Enter item description: ")
        p_stock = simpledialog.askinteger(None, "Enter item stock: ")

        self.unit_price.update({p_no: p_pr})
        self.description.update({p_no: p_desc})
        self.stock.update({p_no: p_stock})
        messagebox.showinfo(None, "Item successfully updated!")
    else:
        messagebox.showwarning(None, "That item does not exist!")


def removeitem(tabself):
    selinput = tabself.tree.selection()
    if len(selinput) != 0:
        are_you_sure = messagebox.askyesno(None, "Are you sure to remove this item from stock?")
        if are_you_sure is True:
            try:
                con = sqlite3.connect("data/stock.db")
                try:
                    cur = con.cursor()
                    selitemid = tabself.tree.item(selinput, "values")[0]
                    cur.execute("DELETE FROM items WHERE item_number = ?",
                                (selitemid,))
                    con.commit()
                finally:
                    con.close()
                tabself.master.statbar.statright.set("Item removed from stock!")
            except (sqlite3.Error, tk.TclError) as errn:
                errorlog(error=str(errn), funcname=str(tabself) + " - removeitem")
                tabself.master.statbar.statright.set("An error occurred! Details logged.")


def addtocart(tabself):
    selinput = tabself.tree.selection()
    usern = FuncVars.curuser
    if len(selinput) != 0:
        try:
            con = sqlite3.connect("data/stock.db")
            try:
                cur = con.cursor()
                selitemid = tabself.tree.item(selinput, "values")[0]
                stockmaxval = int(tabself.tree.item(selinput, "values")[3])
                cur.execute("SELECT amount FROM carts WHERE cart_username = ? AND cart_item_number = ?",
                            (usern, selitemid,))
                rows = cur.fetchall()
                if len(rows) == 0:
                    addamount = simpledialog.askinteger(None, "Enter amount to add (max.: " + str(stockmaxval) + "):",
                                                        minvalue=1, maxvalue=stockmaxval, initialvalue=1)
                    cur.execute("INSERT INTO carts(cart_username, cart_item_number, amount) VALUES (?, ?, ?)",
                                (usern, selitemid, addamount,))
                    con.commit()
                    tabself.master.statbar.statright.set("Item added to cart!")
                else:
                    cartval = int((rows[0])[0])
                    are_you_sure = messagebox.askyesno(None, "Item already in cart: do you want to modify it now?")
                    if are_you_sure is True:
                        addamount = simpledialog.askinteger(None, "Accept or enter new amount: ",
                                                            minvalue=1, maxvalue=stockmaxval, initialvalue=cartval)
                        cur.execute("UPDATE carts SET amount = ? WHERE cart_username = ? AND cart_item_number = ?",
                                    (addamount, usern, selitemid,))
                    con.commit()
                    tabself.master.statbar.statright.set("Cart item amount modified!")
            finally:
                con.close()
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(tabself) + " - addtocart")
            tabself.master.statbar.statright.set("An error occurred! Details logged.")


def showcart(tabself):
    tabself.tree.delete(*tabself.tree.get_children())
    usern = FuncVars.curuser
    try:
        con = sqlite3.connect("data/stock.db")
        try:
            cur = con.cursor()
            cur.execute("SELECT item_number, item_price, item_desc, amount FROM items "
                        "INNER JOIN carts ON item_number = cart_item_number WHERE cart_username = ?", (usern,))
            rows = cur.fetchall()
            for row in rows:
                tabself.tree.insert("", "end", values=row)
            if len(rows) == 0:
                tabself.master.statbar.statright.set("No items in cart!")
            else:
                tabself.master.statbar.statright.set("All cart items listed: " + str(len(rows)))
        finally:
            con.close()
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - showcart")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")


def checkoutitems(self):
    print("You bought the following parts: ", self.cart)
    print("Total: ", "$", round(self.total_cost, 2))
    tax = round(0.13 * self.total_cost, 2)  # áfa 27%???
    print("Tax is 13%: ", "$", tax)
    total = round(self.total_cost + tax, 2)
    print("After Tax: ", "$", total)
    # fentieket labelbe kiíratni?? item-ök szövegbe fűzve? \n.join(item...)

    self.total_cost = 0
    self.flag = 1
    messagebox.showinfo(None, "You can still purchase items after check out, your cart has been reset.")


def removefromcart(tabself):
    selinput = tabself.tree.selection()
    usern = FuncVars.curuser
    if len(selinput) != 0:
        are_you_sure = messagebox.askyesno(None, "Are you sure to remove this item from cart?")
        if are_you_sure is True:
            try:
                con = sqlite3.connect("data/stock.db")
                try:
                    cur = con.cursor()
                    selitemid = tabself.tree.item(selinput, "values")[0]
                    cur.execute("DELETE FROM carts WHERE cart_username = ? AND cart_item_number = ?",
                                (usern, selitemid,))
                    con.commit()
                finally:
                    con.close()
                tabself.master.statbar.statright.set("Item removed from cart!")
            except (sqlite3.Error, tk.TclError) as errn:
                errorlog(error=str(errn), funcname=str(tabself) + " - removefromcart")
                tabself.master.statbar.statright.set("An error occurred! Details logged.")


def clearcart(tabself):
    usern = FuncVars.curuser
    are_you_sure = messagebox.askyesno(None, "Are you sure to clear ALL items from cart?")
    if are_you_sure is True:
        try:
            con = sqlite3.connect("data/stock.db")
            try:
                cur = con.cursor()
                cur.execute("DELETE FROM carts WHERE cart_username = ?",
                            (usern,))
                con.commit()
            finally:
                con.close()
            tabself.master.statbar.statright.set("All items cleared from cart!")
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(tabself) + " - clearcart")
            tabself.master.statbar.statright.set("An error occurred! Details logged.")


def login(tabself):
    usern = str(tabself.entusern.get())
    passw = str(tabself.entpassw.get())
    if str(usern) != "" and str(passw) != "":
        try:
            con = sqlite3.connect("data/stock.db")
            try:
                cur = con.cursor()
                cur.execute("SELECT email, address FROM users WHERE username = ? and password = ?",
                            (usern, passw,))
                usermatch = cur.fetchall()
                if len(usermatch) > 0:
                    email = (usermatch[0])[0]
                    address = (usermatch[0])[1]
                    accountinterior(usern, tabself, email, address)
                else:
                    messagebox.showwarning(None, "To register a new account, please contact admin: admin@it.ims.com")
            finally:
                con.close()
                tabself.entusern.set("")
                tabself.entpassw.set("")
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(tabself) + " - login")
            tabself.master.statbar.statright.set("An error occurred! Details logged.")


def changepassw(tabself):
    usern = FuncVars.curuser
    try:
        con = sqlite3.connect("data/stock.db")
        try:
            cur = con.cursor()
            cur.execute("SELECT password FROM users WHERE username = ?", (usern,))
            rows = cur.fetchall()
            passw = (rows[0])[0]
            inpactpassw = tabself.entactpassw.get()
            inpnewpassw = tabself.entnewpassw.get()
            if inpactpassw != passw:
                messagebox.showwarning(None, "Actual password entered incorrectly!")
            else:
                cur.execute("UPDATE users SET password = ? WHERE username = ?",
                            (inpnewpassw, usern,))
                con.commit()
                tabself.master.statbar.statright.set("Password changed!")
        finally:
            con.close()
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - changepassw")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")


def changecontact(tabself):
    usern = FuncVars.curuser
    try:
        con = sqlite3.connect("data/stock.db")
        try:
            cur = con.cursor()
            cur.execute("SELECT email, address FROM users WHERE username = ?", (usern,))
            rows = cur.fetchall()
            actemail = (rows[0])[0]
            actaddress = (rows[0])[1]
            newemail = simpledialog.askstring(None, "Enter new e-mail:", initialvalue=actemail)
            newaddress = simpledialog.askstring(None, "Enter new address:", initialvalue=actaddress)
            cur.execute("UPDATE users SET email = ?, address = ? WHERE username = ?",
                        (newemail, newaddress, usern,))
            con.commit()
            tabself.master.statbar.statright.set("Contact info changed!")
        finally:
            con.close()
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - changecontact")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")


def accountinterior(usern, tabself, email, address):
    FuncVars.curuser = str(usern)
    tabself.master.statbar.statleft.set("Logged in as: " + str(usern))
    tabself.master.statbar.statright.set("Logged in.")
    # tablogin 0, tabguest 1, tabacc 2, tabstock 3, tabcart 4,
    # tabadminacc 5, tabadminstock 6, tabadmincart 7, tabadminusers 8
    if str(usern) == "admin":
        tabself.master.tabmenu.tab(5, state="normal")
        tabself.master.tabmenu.select(tabself.master.tabadminacc)
        tabself.master.tabadminacc.labemail.configure(text="E-mail: " + str(email))
        tabself.master.tabadminacc.labaddress.configure(text="Address: " + str(address))
        # usern, profilimg
        tabself.master.tabmenu.tab(6, state="normal")
        tabself.master.tabmenu.tab(7, state="normal")
        tabself.master.tabmenu.tab(8, state="normal")
    else:
        tabself.master.tabmenu.tab(2, state="normal")
        tabself.master.tabmenu.select(tabself.master.tabacc)
        tabself.master.tabacc.labemail.configure(text="E-mail: " + str(email))
        tabself.master.tabacc.labaddress.configure(text="Address: " + str(address))
        tabself.master.tabmenu.tab(3, state="normal")
        tabself.master.tabmenu.tab(4, state="normal")
    tabself.master.tabmenu.tab(0, state="hidden")
    tabself.master.tabmenu.tab(1, state="hidden")


def logout(tabself):
    FuncVars.curuser = "guest"
    tabself.master.statbar.statleft.set("Not logged in (guest).")
    tabself.master.statbar.statright.set("Logged out.")
    # tablogin 0, tabguest 1, tabacc 2, tabstock 3, tabcart 4,
    # tabadminacc 5, tabadminstock 6, tabadmincart 7, tabadminusers 8
    tabself.master.tabmenu.tab(0, state="normal")
    tabself.master.tabmenu.select(tabself.master.tablogin)
    tabself.master.tabmenu.tab(1, state="normal")
    tabself.master.tabmenu.tab(2, state="hidden")
    tabself.master.tabmenu.tab(3, state="hidden")
    tabself.master.tabmenu.tab(4, state="hidden")
    tabself.master.tabmenu.tab(5, state="hidden")
    tabself.master.tabmenu.tab(6, state="hidden")
    tabself.master.tabmenu.tab(7, state="hidden")
    tabself.master.tabmenu.tab(8, state="hidden")


def errorlog(error, funcname):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tolog = str(timestamp) + " - " + str(FuncVars.curuser) + " - " + str(funcname) + " - " + str(error)
    FuncVars.wtoerrorlog.append(tolog)


def exitprog():
    # if the user quits without checking out
    if FuncVars.total_cost > 0 and FuncVars.flag == 0:
        askyn = messagebox.askyesno(None, "You have items in cart!\n"
                                          "Are you sure you want to QUIT?")
        if askyn is not True:
            return
    else:
        # wtolog --> kiíratni log.txtbe!!!
        # wtoerrorlog --> kiíratni errorlog.txtbe!!!
        root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("InventoryManager - Inventory Management Tools - Dave")
    root.appicon = tk.PhotoImage(file="images/imsicon.png")
    root.iconphoto(False, root.appicon)
    root.geometry("636x363")
    root.resizable(0, 0)
    StyleConfig()
    mainwind = MainAppWind(root)
    root.protocol("WM_DELETE_WINDOW", exitprog)
    root.mainloop()
