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
        self.tabbrowse = TabBrowse(self)
        self.tabcart = TabCart(self)
        self.tabstock = TabStock(self)
        self.tabmenu.add(self.tablogin, text="Login")
        self.tabmenu.add(self.tabbrowse, text="Browse")
        self.tabmenu.add(self.tabcart, text="Cart", state="disabled")
        self.tabmenu.add(self.tabstock, text="Stock", state="disabled")


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

        ttk.Button(self.form, text="Login", command=lambda: login(tabself=self)).pack(pady=4)
        # new account btn


class TabBrowse(ttk.Frame):
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
        self.btnexit = ttk.Button(self.menu, text="Exit", command=None)

        # self.vmibtn.pack(fill="x", pady=4)
        # ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnsearch.pack(fill="x", pady=4)
        self.btnlistall.pack(fill="x", pady=4)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=8)
        self.btnexit.pack(fill="x", pady=4)


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


def searchitem(self):
    kerinput = simpledialog.askstring(None, "Enter item ID:")
    self.delete(*self.tree.get_children())
    try:
        con = sqlite3.connect("data/stock.db")
        with con:
            cur = con.cursor()
            cur.execute("SELECT item_number, item_price, item_desc, item_stock FROM items WHERE item_number LIKE ?",
                        (kerinput + "%",))
            rows = cur.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            if len(rows) == 0:
                messagebox.showwarning(None, "Nincs találat!")
            else:
                self.statright.set("Item found!")
                self.update_idletasks()
    except sqlite3.Error as dberror:
        self.errorlog(error="dberror: " + str(dberror), funcname="searchitem")
        messagebox.showerror(None, "Adatbázis hiba:\n" + str(dberror))
    except tk.TclError as error:
        self.errorlog(error="tclerror: " + str(error), funcname="searchitem")
        messagebox.showerror(None, "Egyéb hiba:\n" + str(error))
    finally:
        con.close()


def listallitems(tabself):
    tabself.tree.delete(*tabself.tree.get_children())
    try:
        con = sqlite3.connect("data/stock.db")
        with con:
            cur = con.cursor()
            cur.execute("SELECT item_number, item_price, item_desc, item_stock FROM items")
            rows = cur.fetchall()
            for row in rows:
                tabself.tree.insert("", "end", values=row)
            if len(rows) == 0:
                messagebox.showwarning(None, "Nincs találat!")
            # setstatvar(setval="statright", newval="All items listed: " + str(len(rows)))
            # tabself.master.update_idletasks()
    except sqlite3.Error as dberror:
        errorlog(error="dberror: " + str(dberror), funcname=str(tabself) + " - listallitems")
        messagebox.showerror(None, "Adatbázis hiba:\n" + str(dberror))
    except tk.TclError as error:
        errorlog(error="tclerror: " + str(error), funcname=str(tabself) + " - listallitems")
        messagebox.showerror(None, "Egyéb hiba:\n" + str(error))
    finally:
        con.close()


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


def removeitem(self):
    p_no = simpledialog.askinteger(None, "Enter item number: ")
    if p_no in self.unit_price:
        are_you_sure = messagebox.askyesno(None, "Are you sure you want to remove that item?")
        if are_you_sure is True:
            self.stock.pop(p_no)
            messagebox.showinfo(None, "Item successfully removed!")
    else:
        messagebox.showwarning(None, "Sorry, we don't have such an item!")


def addtocart(tabself):  # mint az add item csak a db carts táblája
    selinput = tabself.tree.selection()
    if len(selinput) != 0:
        amountinp = int(simpledialog.askinteger(None, "Enter amount of item:"))
        try:
            con = sqlite3.connect("data/stock.db")
            with con:
                cur = con.cursor()
                for sel in selinput:
                    selitemid = tabself.tree.item(sel, "values")[0]
                    cur.execute("INSERT INTO carts(cart_username, cart_item_number, amount) VALUES ('admin', ?, ?)",
                                (selitemid, amountinp,))
            con.commit()
            tabself.statright.set("Item added to cart!")
            tabself.update_idletasks()
        except sqlite3.Error as dberror:
            errorlog(error="dberror: " + str(dberror), funcname=str(tabself) + " - addtocart")
            messagebox.showerror(None, "Adatbázis hiba:\n" + str(dberror))
        except tk.TclError as error:
            errorlog(error="tclerror: " + str(error), funcname=str(tabself) + " - addtocart")
            messagebox.showerror(None, "Egyéb hiba:\n" + str(error))
        finally:
            con.close()

    '''p_no = simpledialog.askinteger(None, "Enter item number: ")
    if p_no in self.unit_price:
        if self.flag == 1:
            self.flag = 0
        stock_current = self.stock.get(p_no)
        if stock_current > 0:
            stock_current = self.stock.get(p_no)
            self.stock[p_no] = stock_curren t -1
            item_price = self.unit_price.get(p_no)
            self.total_cost = self.total_cos t +item_price
            messagebox.showinfo(None, self.description.get(p_no) + "added to cart: $" + str(item_price))
            self.cart.append(p_no)  # Stores item in cart
        else:
            messagebox.showwarning(None, "Sorry! We don't have that item in stock!")
    else:
        messagebox.showwarning(None, "Sorry! We don't have such an item!")'''


def removefromcart(self):  # remove item mintájára
    are_you_sure = messagebox.askyesno(None, "Are you sure you want to remove an item from the cart?")
    if are_you_sure is True:
        p_no = simpledialog.askinteger(None, "Enter item number to remove from cart: ")
        if p_no in self.cart:
            stock_current = self.stock.get(p_no)
            self.stock[p_no] = stock_current + 1
            item_price = self.unit_price.get(p_no)
            self.total_cost = self.total_cost - item_price
            j = 0
            for i in range(0, len(self.cart)):  # To find the index of the item in the list cart
                if i == p_no:
                    j = i
            self.cart.pop(j)
            messagebox.showinfo(None, self.description.get(p_no) + "removed from cart!")
        else:
            messagebox.showwarning(None, "That item is not in your cart!")


def showcart(tabself):
    # \n.join(item...)
    try:
        con = sqlite3.connect("data/stock.db")
        with con:
            cur = con.cursor()
            cur.execute("SELECT cart_username, cart_item_number FROM carts")  # inner join itemsből ami kell mellé on cartitemnumber = itemnumber
            rows = cur.fetchall()
            for row in rows:
                tabself.tree.insert("", "end", values=row)
            if len(rows) == 0:
                messagebox.showwarning(None, "Nincs találat!")
            else:
                tabself.statright.set("All cart items listed: " + str(len(rows)))
                tabself.update_idletasks()
    except sqlite3.Error as dberror:
        errorlog(error="dberror: " + str(dberror), funcname="showcart")
        messagebox.showerror(None, "Adatbázis hiba:\n" + str(dberror))
    except tk.TclError as error:
        errorlog(error="tclerror: " + str(error), funcname="showcart")
        messagebox.showerror(None, "Egyéb hiba:\n" + str(error))
    finally:
        con.close()


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


def login(tabself):
    usern = str(tabself.entusern.get())
    passw = str(tabself.entpassw.get())
    if str(usern) != "" and str(passw) != "":
        try:
            con = sqlite3.connect("data/stock.db")
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE username = ? and password = ?", (usern, passw,))
                usermatch = cur.fetchall()
                if len(usermatch) > 0:
                    accountinterior(usern, tabself)
                else:
                    regnewuser(usern, passw, tabself)
        except sqlite3.Error as dberror:
            errorlog(error="dberror: " + str(dberror), funcname="login")
            messagebox.showerror(None, "Adatbázis hiba:\n" + str(dberror))
        except tk.TclError as error:
            errorlog(error="tclerror: " + str(error), funcname="login")
            messagebox.showerror(None, "Egyéb hiba:\n" + str(error))
        finally:
            con.close()


def accountinterior(usern, tabself):
    FuncVars.curuser = str(usern)
    tabself.master.statbar.statleft.set("Logged in as: " + str(usern))
    tabself.master.statbar.statright.set("Logged in.")
    tabself.master.tabmenu.tab(0, text="Account")
    if str(usern) == "admin":
        tabself.master.tabmenu.tab(2, state="normal")
        tabself.master.tabmenu.tab(3, state="normal")
    else:
        tabself.master.tabmenu.tab(2, state="normal")
    # tabself.master.tabmenu.select(tabself.master.tabaccount)


def regnewuser(usern, passw, tabself):
    messagebox.showwarning(None, "To register a new account, please contact admin.")
    asknewreg = messagebox.askyesno(None, "Login error: account does not exist!"
                                          "\nAdmin login needed to register a new account."
                                          "\nDo you want to do it now?")
    if asknewreg is True:
        pass
    else:
        return


def logout(tabself):
    FuncVars.curuser = "guest"
    tabself.master.statbar.statleft.set("Not logged in (guest).")
    tabself.master.statbar.statright.set("Logged out.")
    tabself.master.tabmenu.tab(0, text="Login")
    tabself.master.tabmenu.tab(2, state="disabled")
    tabself.master.tabmenu.tab(3, state="disabled")


def errorlog(error, funcname):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tolog = str(timestamp) + " - " + str(FuncVars.curuser) + " - " + str(funcname) + " - " + str(error)
    FuncVars.wtoerrorlog.append(tolog)
    # setstatvar(setval="statright", newval="Error logs updated!")
    # statself.update_idletasks()


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
    root.appicon = tk.PhotoImage(file="icons/imsicon.png")
    root.iconphoto(False, root.appicon)
    root.geometry("636x363")
    root.resizable(0, 0)
    StyleConfig()
    mainwind = MainAppWind(root)
    root.protocol("WM_DELETE_WINDOW", exitprog)
    root.mainloop()
