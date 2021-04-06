import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog, messagebox, filedialog
import sqlite3
import datetime


class FuncVars:
    stock = []
    cart = []

    wtolog = []
    wtoerrorlog = []

    curuser = "guest"


def viewasusern(tabself):
    selinput = tabself.tree.selection()
    if len(selinput) != 0:
        usern = tabself.tree.item(selinput, "values")[0]
        FuncVars.curuser = str(usern)
        if str(usern) != "admin":
            tabself.master.statbar.statleft.set("Logged in as: " + str(usern) + " (admin)")
            tabself.master.tabmenu.tab(5, state="disabled")
            tabself.btnlistallusers.configure(state="disabled")
            tabself.btnadduser.configure(state="disabled")
            tabself.btnedituser.configure(state="disabled")
            tabself.btnremoveuser.configure(state="disabled")
        else:
            tabself.master.tabmenu.tab(5, state="normal")
            tabself.btnlistallusers.configure(state="normal")
            tabself.btnadduser.configure(state="normal")
            tabself.btnedituser.configure(state="normal")
            tabself.btnremoveuser.configure(state="normal")


def connectdb(tabself):
    try:
        con = sqlite3.connect("data/stock.db")
        return con
    except sqlite3.Error as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - connectdb")
        tabself.master.statbar.statright.set("Database error: connection failed. Details logged.")


def searchitem(tabself):
    kerinput = simpledialog.askstring(None, "Enter item ID:")
    tabself.delete(*tabself.tree.get_children())
    con = connectdb(tabself)
    try:
        cur = con.cursor()
        cur.execute("SELECT item_number, item_price, item_desc, item_stock FROM items WHERE item_number LIKE ?",
                    ("%" + kerinput + "%",))
        rows = cur.fetchall()
        for row in rows:
            tabself.tree.insert("", "end", values=row)
        if len(rows) == 0:
            messagebox.showwarning(None, "No item found!")
        else:
            tabself.master.statbar.statright.set("Item(s) found!")
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - searchitem")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")
    finally:
        con.close()


def listallitems(tabself):
    tabself.tree.delete(*tabself.tree.get_children())
    con = connectdb(tabself)
    try:
        cur = con.cursor()
        cur.execute("SELECT item_number, item_price, item_desc, item_stock FROM items ORDER BY item_number ASC")
        rows = cur.fetchall()
        for row in rows:
            tabself.tree.insert("", "end", values=row)
        if len(rows) == 0:
            tabself.master.statbar.statright.set("No items found!")
        tabself.master.statbar.statright.set("All items listed: " + str(len(rows)))
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - listallitems")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")
    finally:
        con.close()


def additem(tabself):
    con = connectdb(tabself)
    try:
        cur = con.cursor()
        newitemid = simpledialog.askstring(None, "Enter ID number for new item\n(ABCD-123)", initialvalue="ABCD-123")
        cur.execute("SELECT item_number FROM items WHERE item_number = ?",
                    (newitemid,))
        rows = cur.fetchall()
        if len(rows) != 0:
            messagebox.showwarning(None, "Item already exists! (Try Edit Item instead.)")
        else:
            newitemprice = simpledialog.askfloat(None, "Enter item price:", minvalue=1)
            newitemdesc = simpledialog.askstring(None, "Enter item description:")
            newitemstock = simpledialog.askinteger(None, "Enter amount of item:", minvalue=1)
            cur.execute("INSERT INTO items(item_number, item_price, item_desc, item_stock) VALUES (?, ?, ?, ?)",
                        (newitemid, newitemprice, newitemdesc, newitemstock,))
            con.commit()
            tabself.master.statbar.statright.set("New item added!")
            listallitems(tabself)
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - additem")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")
    finally:
        con.close()


def edititem(tabself):
    selinput = tabself.tree.selection()
    if len(selinput) != 0:
        con = connectdb(tabself)
        try:
            cur = con.cursor()
            selitemid = tabself.tree.item(selinput, "values")[0]
            selitemprice = float(tabself.tree.item(selinput, "values")[1])
            selitemdesc = str(tabself.tree.item(selinput, "values")[2])
            selitemstock = int(tabself.tree.item(selinput, "values")[3])
            newprice = simpledialog.askfloat(None, "Accept or enter new price: ",
                                             minvalue=1, initialvalue=selitemprice)
            newdesc = simpledialog.askstring(None, "Accept or enter new description: ",
                                             initialvalue=selitemdesc)
            newstock = simpledialog.askinteger(None, "Accept or enter new amount: ",
                                               minvalue=1, initialvalue=selitemstock)
            cur.execute("UPDATE items SET item_price = ?, item_desc = ?, item_stock = ? WHERE item_number = ?",
                        (newprice, newdesc, newstock, selitemid,))
            con.commit()
            tabself.master.statbar.statright.set("Item modified!")
            listallitems(tabself)
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(tabself) + " - edititem")
            tabself.master.statbar.statright.set("An error occurred! Details logged.")
        finally:
            con.close()


def removeitem(tabself):
    selinput = tabself.tree.selection()
    if len(selinput) != 0:
        are_you_sure = messagebox.askyesno(None, "Are you sure to remove this item from stock?")
        if are_you_sure is True:
            con = connectdb(tabself)
            try:
                cur = con.cursor()
                selitemid = tabself.tree.item(selinput, "values")[0]
                cur.execute("DELETE FROM items WHERE item_number = ?",
                            (selitemid,))
                con.commit()
                tabself.master.statbar.statright.set("Item removed from stock!")
                listallitems(tabself)
            except (sqlite3.Error, tk.TclError) as errn:
                errorlog(error=str(errn), funcname=str(tabself) + " - removeitem")
                tabself.master.statbar.statright.set("An error occurred! Details logged.")
            finally:
                con.close()


def addtocart(tabself):
    selinput = tabself.tree.selection()
    usern = FuncVars.curuser
    if len(selinput) != 0:
        con = connectdb(tabself)
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
                showcart(tabself)
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
                showcart(tabself)
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(tabself) + " - addtocart")
            tabself.master.statbar.statright.set("An error occurred! Details logged.")
        finally:
            con.close()


def showcart(tabself):
    tabself.treecart.delete(*tabself.tree.get_children())
    usern = FuncVars.curuser
    con = connectdb(tabself)
    try:
        cur = con.cursor()
        cur.execute("SELECT item_number, item_price, item_desc, amount FROM items "
                    "INNER JOIN carts ON item_number = cart_item_number WHERE cart_username = ? " +
                    "ORDER BY item_number ASC", (usern,))
        rows = cur.fetchall()
        for row in rows:
            tabself.treecart.insert("", "end", values=row)
        if len(rows) == 0:
            tabself.master.statbar.statright.set("No items in cart!")
        else:
            tabself.master.statbar.statright.set("All cart items listed: " + str(len(rows)))
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - showcart")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")
    finally:
        con.close()


def checkoutitems(tabself):
    print("You bought the following parts: ", tabself.cart)
    print("Total: ", "$", round(tabself.total_cost, 2))
    tax = round(0.13 * tabself.total_cost, 2)  # áfa 27%???
    print("Tax is 13%: ", "$", tax)
    total = round(tabself.total_cost + tax, 2)
    print("After Tax: ", "$", total)
    # fentieket labelbe kiíratni?? item-ök szövegbe fűzve? \n.join(item...)
    # kosár törlése (clearcart)


def removefromcart(tabself):
    selinput = tabself.treecart.selection()
    usern = FuncVars.curuser
    if len(selinput) != 0:
        are_you_sure = messagebox.askyesno(None, "Are you sure to remove this item from cart?")
        if are_you_sure is True:
            con = connectdb(tabself)
            try:
                cur = con.cursor()
                selitemid = tabself.treecart.item(selinput, "values")[0]
                cur.execute("DELETE FROM carts WHERE cart_username = ? AND cart_item_number = ?",
                            (usern, selitemid,))
                con.commit()
                tabself.master.statbar.statright.set("Item removed from cart!")
                showcart(tabself)
            except (sqlite3.Error, tk.TclError) as errn:
                errorlog(error=str(errn), funcname=str(tabself) + " - removefromcart")
                tabself.master.statbar.statright.set("An error occurred! Details logged.")
            finally:
                con.close()


def clearcart(tabself):
    usern = FuncVars.curuser
    are_you_sure = messagebox.askyesno(None, "Are you sure to clear ALL items from cart?")
    if are_you_sure is True:
        con = connectdb(tabself)
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM carts WHERE cart_username = ?",
                        (usern,))
            con.commit()
            tabself.master.statbar.statright.set("All items cleared from cart!")
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(tabself) + " - clearcart")
            tabself.master.statbar.statright.set("An error occurred! Details logged.")
        finally:
            con.close()


def login(tabself):
    usern = str(tabself.entusern.get())
    passw = str(tabself.entpassw.get())
    if str(usern) != "" and str(passw) != "":
        con = connectdb(tabself)
        try:
            cur = con.cursor()
            cur.execute("SELECT email, address, photo FROM users WHERE username = ? and password = ?",
                        (usern, passw,))
            usermatch = cur.fetchall()
            if len(usermatch) > 0:
                email = (usermatch[0])[0]
                address = (usermatch[0])[1]
                accountinterior(usern, tabself, email, address)
            else:
                messagebox.showwarning(None, "To register a new account or in case of forgotten password, " +
                                       "please contact admin: admin@it.ims.com")
        except (sqlite3.Error, tk.TclError) as errn:
            errorlog(error=str(errn), funcname=str(tabself) + " - login")
            tabself.master.statbar.statright.set("An error occurred! Details logged.")
        finally:
            con.close()
            tabself.entusern.set("")
            tabself.entpassw.set("")


def changepassw(tabself):
    usern = FuncVars.curuser
    con = connectdb(tabself)
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
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - changepassw")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")
    finally:
        con.close()
        tabself.entactpassw.set("")
        tabself.entnewpassw.set("")


def changecontact(tabself):
    usern = FuncVars.curuser
    con = connectdb(tabself)
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
    except (sqlite3.Error, tk.TclError) as errn:
        errorlog(error=str(errn), funcname=str(tabself) + " - changecontact")
        tabself.master.statbar.statright.set("An error occurred! Details logged.")
    finally:
        con.close()


def accountinterior(usern, tabself, email, address):
    FuncVars.curuser = str(usern)
    tabself.master.statbar.statleft.set("Logged in as: " + str(usern))
    tabself.master.statbar.statright.set("Logged in.")
    # tablogin 0, tabguest 1, tabacc 2, tabstockcart 3
    # tabadminusers 4, tabadminlogs 5
    if str(usern) == "admin":
        tabself.master.tabmenu.tab(4, state="normal")
        tabself.master.tabmenu.tab(5, state="normal")
    else:
        tabself.master.tabmenu.tab(3, state="normal")
    tabself.master.tabacc.labnameposg.configure(text="Name:\n" + str(usern) +
                                                     "\nPosition:\nJunior Programmer\nGroup:\nSoftware Development")
    tabself.master.tabacc.labemail.configure(text="E-mail: " + str(email))
    tabself.master.tabacc.labaddress.configure(text="Address: " + str(address))
    tabself.master.tabmenu.tab(2, state="normal")
    tabself.master.tabmenu.select(tabself.master.tabacc)
    tabself.master.tabmenu.tab(3, state="normal")
    tabself.master.tabmenu.tab(0, state="hidden")
    tabself.master.tabmenu.tab(1, state="hidden")


def logout(tabself):
    FuncVars.curuser = "guest"
    tabself.master.statbar.statleft.set("Not logged in (guest).")
    tabself.master.statbar.statright.set("Logged out.")
    # tablogin 0, tabguest 1, tabacc 2, tabstockcart 3
    # tabadminusers 4, tabadminlogs 5
    tabself.master.tabmenu.tab(0, state="normal")
    tabself.master.tabmenu.select(tabself.master.tablogin)
    tabself.master.tabmenu.tab(1, state="normal")
    tabself.master.tabmenu.tab(2, state="hidden")
    tabself.master.tabmenu.tab(3, state="hidden")
    tabself.master.tabmenu.tab(4, state="hidden")
    tabself.master.tabmenu.tab(5, state="hidden")


def errorlog(error, funcname):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tolog = str(timestamp) + " - " + str(FuncVars.curuser) + " - " + str(funcname) + " - " + str(error)
    FuncVars.wtoerrorlog.append(tolog)


def exitprog(root):
    if FuncVars.curuser != "guest" and len(FuncVars.cart) != 0:
        askyn = messagebox.askyesno(None, "You have items in cart!\nAre you sure you want to QUIT?")
        if askyn is False:
            return
    # wtolog --> kiíratni log.txtbe!!!
    # wtoerrorlog --> kiíratni errorlog.txtbe!!!
    root.destroy()
