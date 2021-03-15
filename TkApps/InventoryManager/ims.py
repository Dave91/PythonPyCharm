import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog
import sqlite3


class MainFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side="top", expand=1, fill="both")

        self.menu = ttk.Frame(self, width=150, borderwidth=5)
        self.outp = ttk.Frame(self, borderwidth=5)
        self.menu.pack(side="left", fill="y")
        self.outp.pack(side="right", expand=1, fill="both")

        # OUTP ELEMENTS
        self.scrbar = ttk.Scrollbar(self.outp)
        self.scrbar.pack(side="right", fill="y")
        self.tree = ttk.Treeview(self.outp, column=("column1", "column2", "column3", "column4"), show='headings',
                                 height=14, yscrollcommand=self.scrbar.set)
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

        # VARS
        # Dicts from stock file
        self.unit_price = {}
        self.description = {}
        self.stock = {}
        self.openfilestockimp()  # loading in stock values

        # List to store the items purchased, variables for checkout
        self.cart = []
        self.total_cost = 0
        self.flag = 0  # To check if they have been checked out

        # MENU ELEMENTS & FUNCS
        ttk.Button(self.menu, text="Search item", command=self.searchitem).pack(fill="x", pady=5)
        ttk.Button(self.menu, text="List all items", command=self.listallitems).pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Add item", command=self.additem).pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Edit item", command=self.edititem).pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Remove item", command=self.removeitem).pack(fill="x", pady=5)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=15)
        ttk.Button(self.menu, text="Add to cart", command=self.addtocart).pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Remove from cart", command=self.removefromcart).pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Show cart", command=self.showcart).pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Checkout", command=self.checkoutitems).pack(fill="x", pady=5)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=15)
        ttk.Button(self.menu, text="Exit program", command=self.exitprog).pack(fill="x", pady=5)

    def openfilestockimp(self):
        # Open file with stock
        with open("data/stock.txt", "r") as details:
            # First line of the file is the number of items
            no_items = int((details.readline()).rstrip("\n"))

            # Add items to dictionaries
            for i in range(0, no_items):
                line = (details.readline()).rstrip("\n")
                x1, x2 = line.split("#")
                x1, x2 = int(x1), float(x2)
                self.unit_price.update({x1: x2})

            for i in range(0, no_items):
                line = (details.readline()).rstrip("\n")
                x1, x2 = line.split("#")
                x1 = int(x1)
                self.description.update({x1: x2})

            for i in range(0, no_items):
                line = (details.readline()).rstrip("\n")
                x1, x2 = line.split("#")
                x1, x2 = int(x1), int(x2)
                self.stock.update({x1: x2})

    def searchitem(self):
        kerinput = simpledialog.askstring(None, "Enter item ID:")
        self.tree.delete(*self.tree.get_children())
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
        except sqlite3.Error as dberror:
            messagebox.showerror(None, "Adatbázis hiba:\n" + str(dberror))
            # errorlog.txt-be iratni ezeket
        except tk.TclError as error:
            messagebox.showerror(None, "Egyéb hiba:\n" + str(error))

    def listallitems(self):
        self.tree.delete(*self.tree.get_children())
        try:
            con = sqlite3.connect("data/stock.db")
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM items")
                rows = cur.fetchall()
                for row in rows:
                    self.tree.insert("", "end", values=row)
                if len(rows) == 0:
                    messagebox.showwarning(None, "Nincs találat!")
        except sqlite3.Error as dberror:
            messagebox.showerror(None, "Adatbázis hiba:\n" + str(dberror))
            # errorlog.txt-be iratni ezeket
        except tk.TclError as error:
            messagebox.showerror(None, "Egyéb hiba:\n" + str(error))

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
                self.unit_price.pop(p_no)
                self.description.pop(p_no)
                self.stock.pop(p_no)
                messagebox.showinfo(None, "Item successfully removed!")
        else:
            messagebox.showwarning(None, "Sorry, we don't have such an item!")

    def addtocart(self):  # mint az add item csak a másik db-be insert-el accounts.db cart táblája
        selinput = self.tree.selection()
        if len(selinput) != 0:
            print(selinput)
            return
        p_no = simpledialog.askinteger(None, "Enter item number: ")
        if p_no in self.unit_price:
            if self.flag == 1:
                self.flag = 0
            stock_current = self.stock.get(p_no)
            if stock_current > 0:
                stock_current = self.stock.get(p_no)
                self.stock[p_no] = stock_current-1
                item_price = self.unit_price.get(p_no)
                self.total_cost = self.total_cost+item_price
                messagebox.showinfo(None, self.description.get(p_no) + "added to cart: $" + str(item_price))
                self.cart.append(p_no)  # Stores item in cart
            else:
                messagebox.showwarning(None, "Sorry! We don't have that item in stock!")
        else:
            messagebox.showwarning(None, "Sorry! We don't have such an item!")

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
        print(self.cart)  # labelbe kiíratni?? item-ök szövegbe fűzve? \n.join(item...)

    def checkoutitems(self):
        print("You bought the following parts: ", self.cart)
        print("Total: ", "$", round(self.total_cost, 2))
        tax = round(0.13 * self.total_cost, 2)  # áfa 27%???
        print("Tax is 13%: ", "$", tax)
        total = round(self.total_cost+tax, 2)
        print("After Tax: ", "$", total)
        # fentieket labelbe kiíratni?? item-ök szövegbe fűzve? \n.join(item...)

        self.total_cost = 0
        self.flag = 1
        messagebox.showinfo(None, "You can still purchase items after check out, your cart has been reset.")

    def savefilestockupd(self):
        # Write the updated inventory to the file
        with open("data/stock.txt", "w") as details:
            no_items = len(self.unit_price)
            details.write(str(no_items) + "\n")
            for i in range(0, no_items):
                details.write(str(i + 1) + "#" + str(self.unit_price[i + 1]) + "\n")

            for i in range(0, no_items):
                details.write(str(i + 1) + "#" + self.description[i + 1] + "\n")

            for i in range(0, no_items):
                details.write(str(i + 1) + "#" + str(self.stock[i + 1]) + "\n")

    def exitprog(self):
        # if the user quits without checking out
        if self.total_cost > 0 and self.flag == 0:
            askyn = messagebox.askyesno(None, "You have items in cart!\n"
                                              "Checkout needed: are you sure you want to quit?")
            if askyn is not True:
                return
        else:
            self.savefilestockupd()
            # self.master.destroy()


class StyleConfig(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)

        self.configure("TFrame", background="silver", relief="groove")
        self.configure("TButton", foreground="maroon", background="white", padding=5)
        self.configure("TLabel", background="silver")
        self.configure("TEntry", foreground="blue", background="silver")
        self.configure("TMenubutton", background="silver")


def main():
    # GUI ROOT WINDOW
    root = tk.Tk()
    root.title("InventoryManager - Inventory Management System - Dave")
    appicon = tk.PhotoImage(file="icons/imsicon.png")
    root.iconphoto(False, appicon)
    root.geometry("600x600")
    root.resizable(0, 0)
    StyleConfig()
    MainFrame(parent=root)
    root.mainloop()


if __name__ == "__main__":
    main()
