import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class MainFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side="top", expand=1, fill="both")
        self.menu = ttk.Frame(self, width=150, borderwidth=5)
        self.outp = ttk.Frame(self, borderwidth=5)
        self.menu.pack(side="left", fill="y")
        self.outp.pack(side="right", expand=1, fill="both")
        # MENU
        ttk.Button(self.menu, text="Add item").pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Remove item").pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Edit item").pack(fill="x", pady=5)
        ttk.Button(self.menu, text="List all items").pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Inquire item").pack(fill="x", pady=5)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=15)
        ttk.Button(self.menu, text="Add to cart").pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Remove from cart").pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Show cart").pack(fill="x", pady=5)
        ttk.Button(self.menu, text="Checkout").pack(fill="x", pady=5)
        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=15)
        ttk.Button(self.menu, text="Exit program").pack(fill="x", pady=5)

        # OUTP
        self.lboutp = tk.Listbox(self.outp, foreground="blue", background="beige")
        self.lboutp.pack(side="left", expand=1, fill="both")
        # scrollbar??

        # Dictionaries from stock file
        self.unit_price = {}
        self.description = {}
        self.stock = {}

        # List to store the items purchased, variables for checkout
        self.cart = []
        self.total_cost = 0
        self.flag = 0  # To check if they have been checked out

    def openfile(self):
        try:
            # Open file with stock
            with open("stock.txt", "r") as details:
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
        except:
            messagebox.showerror(None, "ERROR")

    def additem(self):
        p_no = int(input("Enter part number: "))
        p_pr = float(input("Enter part price: "))
        p_desc = input("Enter part description: ")
        p_stock = int(input("Enter part stock: "))

        m = 0
        for i in range(0, len(self.unit_price)):
            if p_no in self.unit_price:
                p_no += 1
                m = 1
        if m == 1:
            # EZEK A PRINTES RÉSZEK MESSAGEBOXOK LESZNEK!
            print("That part number already exists :(, changing value to ", p_no)

        self.unit_price.update({p_no: p_pr})
        self.description.update({p_no: p_desc})
        if p_stock > -1:
            self.stock.update({p_no: p_stock})
        else:
            p_stock = 0
            self.stock.update({p_no: p_stock})
            print("The stock of an item cannot be negative, the stock has been set to 0.")
        print("Part number: ", p_no, " Description: ", self.description.get(p_no), " Price: ", self.unit_price.get(p_no), " Stock: ", self.stock.get(p_no))
        print("Part was added successfully!")

    def removeitem(self):
        p_no = int(input("Enter part number: "))
        if p_no in self.unit_price:
            are_you_sure = input("Are you sure you want to remove that item(y/n)? ")
            if are_you_sure == "y" or are_you_sure == "Y":
                self.unit_price.pop(p_no)
                self.description.pop(p_no)
                self.stock.pop(p_no)
                print("Item successfully removed!")
        else:
            print("Sorry, we don't have such an item!")

    def edititem(self):
        p_no = int(input("Enter part number: "))
        if p_no in self.unit_price:
            p_pr = float(input("Enter part price: "))
            p_desc = input("Enter part description: ")
            p_stock = int(input("Enter part stock: "))

            self.unit_price.update({p_no: p_pr})
            self.description.update({p_no: p_desc})
            self.stock.update({p_no: p_stock})

        else:
            print("That item does not exist, to add an item use a")

    def listallitems(self):
        print("Parts and their prices: ", self.unit_price)
        print("Descriptions: ", self.description)
        print("Stock left of Item: ", self.stock)

    def inquireitem(self):
        p_no = int(input("Enter Part Number: "))
        if p_no in self.unit_price:
            print()
            print("Part number: ", p_no, " Description: ", self.description.get(p_no), " Price: ", self.unit_price.get(p_no), " Stock: ", self.stock.get(p_no))
            if self.stock.get(p_no) < 3 and self.stock.get(p_no) != 0:
                print("Only ", self.stock.get(p_no), " remaining! Hurry!")
        else:
            print("Sorry we don't have such an item!")

    def addtocart(self):
        p_no = int(input("Enter Part number: "))
        if p_no in self.unit_price:
            if self.flag == 1:
                self.flag = 0
            stock_current = self.stock.get(p_no)
            if stock_current > 0:
                stock_current = self.stock.get(p_no)
                self.stock[p_no] = stock_current-1
                item_price = self.unit_price.get(p_no)
                self.total_cost = self.total_cost+item_price
                print(self.description.get(p_no), "added to cart: ", "$", item_price)
                self.cart.append(p_no)  # Stores item in cart
            else:
                print("Sorry! We don't have that item in stock!")
        else:
            print("Sorry! We don't have such an item!")

    def removefromcart(self):
        are_you_sure = input("Are you sure you want to remove an item from the cart(y/n)? ")
        if are_you_sure == "y":
            p_no = int(input("Enter part number to remove from cart: "))
            if p_no in self.cart:
                stock_current = self.stock.get(p_no)
                self.stock[p_no] = stock_current + 1
                item_price = self.unit_price.get(p_no)
                self.total_cost = self.total_cost - item_price
                j = 0
                for i in range(0, len(self.cart)):  # To find the index of the part in the list cart
                    if i == p_no:
                        j = i

                self.cart.pop(j)
                print(self.description.get(p_no), "removed from cart: ")
            else:
                print("That item is not in your cart!")

    def showcart(self):
        print(self.cart)

    def checkoutitems(self):
        print("You bought the following parts: ", self.cart)
        print("Total: ", "$", round(self.total_cost, 2))
        tax = round(0.13 * self.total_cost, 2)  # áfa 27%???
        print("Tax is 13%: ", "$", tax)
        total = round(self.total_cost+tax, 2)
        print("After Tax: ", "$", total)
        self.total_cost = 0
        self.flag = 1
        print("You can still purchase items after check out, your cart has been reset. To quit press q")

    def savefilestockupd(self):
        # Write the updated inventory to the file
        with open("stock.txt", "w") as details:
            no_items = len(self.unit_price)
            details.write(str(no_items) + "\n")
            for i in range(0, no_items):
                details.write(str(i + 1) + "#" + str(self.unit_price[i + 1]) + "\n")

            for i in range(0, no_items):
                details.write(str(i + 1) + "#" + self.description[i + 1] + "\n")

            for i in range(0, no_items):
                details.write(str(i + 1) + "#" + str(self.stock[i + 1]) + "\n")


'''
        #Outputs total if the user quits without checking out
        if(total_cost>0 and flag==0):
            print()
            print("You bought: ",cart)
            print("Total: ","$",round(total_cost,2))
            tax= round(0.13*total_cost,2)  # áfa !!!!
            print("Tax is 13%: ","$",tax)
            total = round(total_cost+tax,2)
            print("After Tax: ","$",total)
'''


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
    root.title("InventoryManager - Inventory Management Tools - Dave")
    # appicon = tk.PhotoImage(file="")
    # root.iconphoto(False, appicon)
    root.geometry("600x600")
    root.resizable(0, 0)
    StyleConfig()
    MainFrame(root)
    # gui handler
    root.mainloop()


if __name__ == "__main__":
    main()
