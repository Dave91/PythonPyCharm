from func import *


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
        self.tabstockcart = TabStockCart(self)
        self.tabadminusers = TabAdminUsers(self)
        self.tabadminlogs = TabAdminLogs(self)

        self.tabmenu.add(self.tablogin, text="Login")
        self.tabmenu.add(self.tabguest, text="Browse as guest")
        self.tabmenu.add(self.tabacc, text="Account", state="hidden")
        self.tabmenu.add(self.tabstockcart, text="Stock & Cart", state="hidden")
        self.tabmenu.add(self.tabadminusers, text="Users", state="hidden")
        self.tabmenu.add(self.tabadminlogs, text="Logs", state="hidden")


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
        ttk.Label(self.form, text="contact admin: admin@it.ims.com", foreground="blue", background="beige").pack()


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
        self.tree.column("#1", width=80)  # anchor="center" v "e" igazításhoz!!
        self.tree.column("#2", width=80)
        self.tree.column("#3", width=240)
        self.tree.column("#4", width=50)
        self.tree.heading("#1", text="Item ID")
        self.tree.heading("#2", text="Price")
        self.tree.heading("#3", text="Description")
        self.tree.heading("#4", text="Amount")
        self.tree.pack(side="left", expand=1, fill="both")
        self.scrbar.config(command=self.tree.yview)
        self.tree.bind("<Button-1>", self.ordercol)
        self.tree.bind("<Button-3>", self.ordercol)

        # ha kéne vmiért frame or label placed over menu vagy outp??
        '''self.menubox = ttk.Frame(self, borderwidth=15)
        self.menubox.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        self.menubox.lift()

        self.entid = tk.StringVar()
        self.entid.set("Item ID")
        ttk.Entry(self.menubox, textvariable=self.entid).pack(side="left")'''

        # MENU ELEMENTS & FUNCS
        self.btnsearch = ttk.Button(self.menu, text="Search item", command=lambda: searchitem(tabself=self))
        self.btnlistall = ttk.Button(self.menu, text="List all items", command=lambda: listallitems(tabself=self))

        self.btnsearch.pack(fill="x", pady=4)
        self.btnlistall.pack(fill="x", pady=4)

    def ordercol(self, event):
        ordermode = event.num
        orderby = self.tree.identify_column(event.x)
        self.tree.delete(*self.tree.get_children())
        coln = {"#1": "item_number", "#2": "item_price", "#3": "item_desc", "#4": "item_stock"}
        try:
            con = sqlite3.connect("data/stock.db")
            try:
                cur = con.cursor()
                if ordermode == 1:
                    if orderby == "#1":
                        cur.execute(
                            "SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_number ASC")
                    if orderby == "#2":
                        cur.execute(
                            "SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_price ASC")
                    if orderby == "#3":
                        cur.execute(
                            "SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_desc ASC")
                    if orderby == "#4":
                        cur.execute(
                            "SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_stock ASC")
                else:
                    if orderby == "#1":
                        cur.execute(
                            "SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_number DESC")
                    if orderby == "#2":
                        cur.execute(
                            "SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_price DESC")
                    if orderby == "#3":
                        cur.execute(
                            "SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_desc DESC")
                    if orderby == "#4":
                        cur.execute(
                            "SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_stock DESC")
                rows = cur.fetchall()
                for row in rows:
                    self.tree.insert("", "end", values=row)
                if len(rows) == 0:
                    messagebox.showwarning(None, "Nincs találat!")
                self.master.statbar.statright.set("Ordered by: " + str(coln[orderby]))
            finally:
                con.close()
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(self) + " - ordercol")
            self.master.statbar.statright.set("An error occurred! Details logged.")


class TabAcc(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

        self.menu = ttk.Frame(self, width=150, borderwidth=5)
        self.outp = ttk.Frame(self, borderwidth=5, style="LoginF.TFrame")
        self.menu.pack(side="left", fill="y")
        self.outp.pack(side="right", expand=1, fill="both")

        # MENU
        ttk.Button(self.menu, text="Show Picture", command=self.showimg).pack(pady=2)
        ttk.Button(self.menu, text="Upload Image", command=self.uploadimg).pack(pady=2)
        self.labnameposg = ttk.Label(self.menu, text="")
        self.labnameposg.pack(pady=4)
        ttk.Button(self.menu, text="Logout", command=lambda: logout(tabself=self)).pack(pady=4)

        # OUTP
        self.actpasswlabel = ttk.Labelframe(self.outp, text="Actual Password")
        self.actpasswlabel.pack(pady=2)
        self.entactpassw = tk.StringVar()
        self.entactpassw.set("")
        ttk.Entry(self.actpasswlabel, textvariable=self.entactpassw, show="*").pack()

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

    def showimg(self):
        usern = FuncVars.curuser
        try:
            con = sqlite3.connect("data/stock.db")
            try:
                cur = con.cursor()
                cur.execute("SELECT photo FROM users WHERE username = ?", (usern,))
                usermatch = cur.fetchall()
                photo = (usermatch[0])[0]
                profilimg = tk.PhotoImage(data=photo).subsample(2)
                self.toplevpic(profilimg, usern)
            finally:
                con.close()
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(self) + " - uploadimg")
            self.master.statbar.statright.set("An error occurred! Details logged.")

    @staticmethod
    def toplevpic(profilimg, usern):
        toplev = tk.Toplevel()
        toplev.title(usern)
        toplev.focus()
        ttk.Label(toplev, image=profilimg).pack()
        toplev.mainloop()

    def uploadimg(self):
        usern = FuncVars.curuser
        try:
            con = sqlite3.connect("data/stock.db")
            try:
                cur = con.cursor()
                imgpath = filedialog.askopenfilename()
                profileimg = self.convimgtoblob(filename=imgpath)
                cur.execute("UPDATE users SET photo = ? WHERE username = ?", (profileimg, usern,))
                con.commit()
                self.master.statbar.statright.set("Profile image uploaded!")
            finally:
                con.close()
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(self) + " - uploadimg")
            self.master.statbar.statright.set("An error occurred! Details logged.")

    @staticmethod
    def convimgtoblob(filename):
        try:
            with open(filename, 'rb') as file:
                imgblob = file.read()
            return imgblob
        except IOError:
            messagebox.showwarning(None, "Error: image file could not be opened!")
        finally:
            file.close()


class TabStockCart(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # self.master = master

        self.framestock = ttk.Frame(self)
        self.framestock.pack(fill="x")
        self.framecart = ttk.Frame(self)
        self.framecart.pack(fill="x")

        # FRAMESTOCK
        self.menustock = ttk.Frame(self.framestock, borderwidth=5)
        self.outpstock = ttk.Frame(self.framestock, borderwidth=5)
        self.menustock.pack(side="left", fill="y")
        self.outpstock.pack(side="right", expand=1, fill="both")
        # OUTPSTOCK
        self.scrbar = ttk.Scrollbar(self.outpstock)
        self.scrbar.pack(side="right", fill="y")
        self.tree = ttk.Treeview(self.outpstock, column=("column1", "column2", "column3", "column4"), show='headings',
                                 selectmode="browse", height=9, yscrollcommand=self.scrbar.set)
        self.tree.column("#1", width=80)
        self.tree.column("#2", width=80)
        self.tree.column("#3", width=240)
        self.tree.column("#4", width=50)
        self.tree.heading("#1", text="Item ID")
        self.tree.heading("#2", text="Price")
        self.tree.heading("#3", text="Description")
        self.tree.heading("#4", text="Amount")
        self.tree.pack(side="left", expand=1, fill="both")
        self.scrbar.config(command=self.tree.yview)

        self.btnsearch = ttk.Button(self.menustock, text="Search item", command=lambda: searchitem(tabself=self))
        self.btnlistall = ttk.Button(self.menustock, text="List all items", command=lambda: listallitems(tabself=self))
        self.btnadditem = ttk.Button(self.menustock, text="Add item", command=lambda: additem(tabself=self))
        self.btnedititem = ttk.Button(self.menustock, text="Edit item", command=lambda: edititem(tabself=self))
        self.btnremoveitem = ttk.Button(self.menustock, text="Remove item", command=lambda: removeitem(tabself=self))
        self.btnaddcart = ttk.Button(self.menustock, text="Add to cart", command=lambda: addtocart(tabself=self))

        self.btnsearch.pack(fill="x", pady=2)
        self.btnlistall.pack(fill="x", pady=2)
        self.btnadditem.pack(fill="x", pady=2)
        self.btnedititem.pack(fill="x", pady=2)
        self.btnremoveitem.pack(fill="x", pady=2)
        self.btnaddcart.pack(fill="x", pady=2)

        # FRAMECART
        self.menucart = ttk.Frame(self.framecart, borderwidth=5)
        self.outpcart = ttk.Frame(self.framecart, borderwidth=5)
        self.menucart.pack(side="left", fill="y")
        self.outpcart.pack(side="right", expand=1, fill="both")
        # OUTPCART
        self.scrbarcart = ttk.Scrollbar(self.outpcart)
        self.scrbarcart.pack(side="right", fill="y")
        self.treecart = ttk.Treeview(self.outpcart, column=("column1", "column2", "column3", "column4"),
                                     show='headings', selectmode="browse", height=6,
                                     yscrollcommand=self.scrbarcart.set)
        self.treecart.column("#1", width=80)
        self.treecart.column("#2", width=80)
        self.treecart.column("#3", width=240)
        self.treecart.column("#4", width=50)
        self.treecart.heading("#1", text="Item ID")
        self.treecart.heading("#2", text="Price")
        self.treecart.heading("#3", text="Description")
        self.treecart.heading("#4", text="Amount")
        self.treecart.pack(side="left", expand=1, fill="both")
        self.scrbarcart.config(command=self.treecart.yview)

        # ha kéne vmiért frame or label placed over menu vagy outp??

        # MENU ELEMENTS & FUNCS
        self.btnshowcart = ttk.Button(self.menucart, text="Show cart", command=lambda: showcart(tabself=self))
        self.btncheckout = ttk.Button(self.menucart, text="Checkout", command=lambda: checkoutitems(tabself=self))
        self.btnremovecart = ttk.Button(self.menucart, text="Remove", command=lambda: removefromcart(tabself=self))
        self.btnclearcart = ttk.Button(self.menucart, text="Clear cart", command=lambda: clearcart(tabself=self))

        self.btnshowcart.pack(fill="x", pady=2)
        self.btncheckout.pack(fill="x", pady=2)
        self.btnremovecart.pack(fill="x", pady=2)
        self.btnclearcart.pack(fill="x", pady=2)


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
        self.tree.heading("#3", text="E-mail")
        self.tree.heading("#4", text="Address")
        self.tree.pack(side="left", expand=1, fill="both")
        self.scrbar.config(command=self.tree.yview)

        # ha kéne vmiért frame or label placed over menu vagy outp??
        '''self.menubox = ttk.Frame(self.menu)
        self.menubox.place(relx=0, rely=0.15, relwidth=1, relheight=0.75)
        ttk.Label(self.menubox)'''

        '''self.outpbox = ttk.Frame(self.outp)
        ttk.Label(self.outpbox)'''

        # MENU ELEMENTS & FUNCS
        ttk.Button(self.menu, text="View as User", command=lambda: viewasusern(tabself=self)).pack(fill="x", pady=4)
        self.btnlistallusers = ttk.Button(self.menu, text="List all users", command=self.listallusers)
        self.btnadduser = ttk.Button(self.menu, text="Add user", command=self.adduser)
        self.btnedituser = ttk.Button(self.menu, text="Rename user", command=self.edituser)
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
                cur.execute("SELECT username, password, email, address FROM users ORDER BY username ASC")
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


class TabAdminLogs(ttk.Frame):
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
        
        self.tree = ttk.Treeview(self.outp, column=("column1", "column2", "column3"), show='headings',
                                 selectmode="browse", height=10, yscrollcommand=self.scrbar.set)
        self.tree.column("#1", width=120, minwidth=120, stretch=0)
        self.tree.column("#2", width=100, minwidth=100, stretch=0)
        self.tree.column("#3", width=270, minwidth=270, stretch=0)
        self.tree.heading("#1", text="Timestamp")
        self.tree.heading("#2", text="Username")
        self.tree.heading("#3", text="Tab & Function")
        self.tree.pack(side="top", expand=1, fill="both")
        self.scrbar.config(command=self.tree.yview)

        #show details vagy dupla kattra felugrik a desc alul??
        self.logdesc = tk.Text(self.outp)
        self.logdesc.pack(side="bottom", fill="x")
        self.logdesc.insert("end", "Error Details: " + "test")

        # MENU ELEMENTS & FUNCS
        self.logsel = tk.StringVar()
        self.logsel.set("")
        ttk.OptionMenu(self.menu, self.logsel, "Choose Log", "Errors", "Events", command=self.showrecords).pack(
            fill="x", pady=4)

        self.btnshowdetails = ttk.Button(self.menu, text="Show details", command=self.showdetails)
        self.btnclearlog = ttk.Button(self.menu, text="Clear log", command=self.clearlog)

        self.btnshowdetails.pack(fill="x", pady=4)
        self.btnclearlog.pack(fill="x", pady=4)

    def showrecords(self):
        logsel = self.logsel.get()
        logs = {"Errors": "errorlog", "Events": "log"}
        self.logdesc.configure(value="test")
        #FuncVars.wtoerrorlog[0]

    def showdetails(self):
        pass

    def clearlog(self):
        if self.logsel.get() != "Choose Log":
            pass
        else:
            return


class StyleConfig(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.configure("TNotebook.Tab", width=15, padding=(4, 2, 4, 2))
        self.map("TNotebook.Tab", foreground=[("active", "maroon")])
        self.configure("TFrame", background="silver", relief="groove")
        self.configure("LoginF.TFrame", background="beige")
        self.configure("TLabelframe", background="beige")
        self.configure("TButton", foreground="black", background="white", padding=2)
        self.map("TButton", foreground=[("active", "maroon")], background=[("active", "coral")])
        self.configure("TLabel", background="silver")
        self.configure("AccL.TLabel", background="beige")
        self.configure("TEntry", foreground="blue", background="silver")
        self.configure("TMenubutton", background="silver")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("InventoryManager - Inventory Management System - Dave")
    root.appicon = tk.PhotoImage(file="images/imsicon.png")
    root.iconphoto(False, root.appicon)
    root.geometry("640x420")
    root.resizable(0, 0)
    StyleConfig()
    mainwind = MainAppWind(root)
    root.protocol("WM_DELETE_WINDOW", lambda: exitprog(root))
    root.mainloop()
