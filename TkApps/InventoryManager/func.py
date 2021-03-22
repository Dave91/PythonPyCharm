import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog
import sqlite3
import datetime
import pages


def searchitem(self):
    kerinput = simpledialog.askstring(None, "Enter item ID:")
    self.delete(*self.tree.get_children())
    try:
        con = sqlite3.connect("data/stock.db")
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM items WHERE item_id LIKE ?", (kerinput + "%",))
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


def listallitems(statself, tabself):
    tabself.tree.delete(*tabself.tree.get_children())
    try:
        con = sqlite3.connect("data/stock.db")
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM items")
            rows = cur.fetchall()
            for row in rows:
                tabself.tree.insert("", "end", values=row)
            if len(rows) == 0:
                messagebox.showwarning(None, "Nincs találat!")
            else:
                statself.statright.set("All items listed: " + str(len(rows)))
                statself.update_idletasks()
    except sqlite3.Error as dberror:
        statself.errorlog(error="dberror: " + str(dberror), funcname="listallitems")
        messagebox.showerror(None, "Adatbázis hiba:\n" + str(dberror))
    except tk.TclError as error:
        statself.errorlog(error="tclerror: " + str(error), funcname="listallitems")
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


def addtocart(self):  # mint az add item csak a db carts táblája
    selinput = self.tree.selection()
    if len(selinput) != 0:
        amountinp = int(simpledialog.askinteger(None, "Enter amount of item:"))
        try:
            con = sqlite3.connect("data/stock.db")
            with con:
                cur = con.cursor()
                for sel in selinput:
                    selitemid = self.tree.item(sel, "values")[0]
                    cur.execute("INSERT INTO carts(username, item_id, amount) VALUES ('admin', ?, ?)",
                                (selitemid, amountinp,))
            con.commit()
            self.statright.set("Item added to cart!")
            self.update_idletasks()
        except sqlite3.Error as dberror:
            self.errorlog(error="dberror: " + str(dberror), funcname="addtocart")
            messagebox.showerror(None, "Adatbázis hiba:\n" + str(dberror))
        except tk.TclError as error:
            self.errorlog(error="tclerror: " + str(error), funcname="addtocart")
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


def showcart(self):
    # \n.join(item...)
    try:
        itemidsfromcart = []
        con = sqlite3.connect("data/stock.db")
        with con:
            cur = con.cursor()
            cur.execute("SELECT item_id FROM carts")
            itemidsfromcart = cur.fetchall()
            for ids in itemidsfromcart:
                cur.execute("SELECT *")
                self.tree.insert("", "end", values=row)
            if len(rows) == 0:
                messagebox.showwarning(None, "Nincs találat!")
            else:
                self.statright.set("All cart items listed: " + str(len(rows)))
                self.update_idletasks()
    except sqlite3.Error as dberror:
        self.errorlog(error="dberror: " + str(dberror), funcname="showcart")
        messagebox.showerror(None, "Adatbázis hiba:\n" + str(dberror))
    except tk.TclError as error:
        self.errorlog(error="tclerror: " + str(error), funcname="showcart")
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


def exitprog(self):
    # if the user quits without checking out
    if self.total_cost > 0 and self.flag == 0:
        askyn = messagebox.askyesno(None, "You have items in cart!\n"
                                          "Checkout needed: are you sure you want to quit?")
        if askyn is not True:
            return
    else:
        pass
        # wtolog --> kiíratni log.txtbe!!!
        # wtoerrorlog --> kiíratni errorlog.txtbe!!!
        # self.master.destroy()


def errorlog(self, error, funcname):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tolog = str(timestamp) + " - " + self.curuser + " - " + str(funcname) + " - " + str(error)
    self.wtoerrorlog.append(tolog)
    self.statright.set("Error logs updated!")
    self.update_idletasks()


def accountinterior(self, usern):
    self.curuser = str(usern)
    self.statleft.set("Logged in as: " + str(usern))
    self.statright.set("Logged in.")
    # self.loginoutbtn.configure(command=self.logout, text="Logout")
    if str(usern) == "admin":
        pass  # tabmenu tabok to normal ? configure(state="normal")
    else:
        pass  # tabstock state disabled
    self.update_idletasks()


def logout(self):
    self.curuser = ""
    self.statleft.set("Not logged in (guest).")
    self.statright.set("Logged out.")
    self.loginoutbtn.configure(command=None, text="Login")
    # tabok to disabled
    self.update_idletasks()


def login(self):
    usern = str(tablogin.TabLogin(None).entusern.get())
    passw = str(tablogin.TabLogin(None).entpassw.get())
    if str(usern) != "" and str(passw) != "":
        try:
            con = sqlite3.connect("data/stock.db")
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE username = ? and password = ?", (usern, passw,))
                usermatch = cur.fetchall()
                if len(usermatch) > 0:
                    self.accountinterior(usern)
                else:
                    self.regnewuser(usern, passw)
        except sqlite3.Error as dberror:
            self.master.errorlog(error="dberror: " + str(dberror), funcname="addtocart")
            messagebox.showerror(None, "Adatbázis hiba:\n" + str(dberror))
        except tk.TclError as error:
            self.master.errorlog(error="tclerror: " + str(error), funcname="addtocart")
            messagebox.showerror(None, "Egyéb hiba:\n" + str(error))
        finally:
            con.close()


def regnewuser(self, usern, passw):
    messagebox.showwarning(None, "To register a new account, please contact admin.")
    asknewreg = messagebox.askyesno(None, "Login error: account does not exist!"
                                          "\nAdmin login needed to register a new account."
                                          "\nDo you want to do it now?")
    if asknewreg is True:
        pass
    else:
        return
