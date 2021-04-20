import tkinter as tk
import tkinter.ttk as ttk


class AppGUI(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(side="top", fill="both", anchor="center")
        self.btns_frame = ttk.Frame(self)
        self.btns_frame.pack()

        self.expression = ""
        self.input_text = tk.StringVar()

        self.input_field = ttk.Entry(self.btns_frame, font=('arial', 16, 'bold'), textvariable=self.input_text,
                                     width=29, justify="right")
        self.input_field.grid(row=0, column=0, columnspan=4, ipadx=2, ipady=10, padx=1, pady=1)
        self.input_field.focus()

        # C, /
        self.clear = ttk.Button(self.btns_frame, text="C", width=40, command=lambda: self.btn_clear())
        self.divide = ttk.Button(self.btns_frame, text="/", width=10, command=lambda: self.btn_click("/"))
        self.clear.grid(row=1, column=0, columnspan=3, padx=1, pady=1)
        self.divide.grid(row=1, column=3, padx=1, pady=1)

        # 7, 8, 9, *
        self.seven = ttk.Button(self.btns_frame, text="7", width=10, command=lambda: self.btn_click("7"))
        self.eight = ttk.Button(self.btns_frame, text="8", width=10, command=lambda: self.btn_click("8"))
        self.nine = ttk.Button(self.btns_frame, text="9", width=10, command=lambda: self.btn_click("9"))
        self.multiply = ttk.Button(self.btns_frame, text="*", width=10, command=lambda: self.btn_click("*"))
        self.seven.grid(row=2, column=0, padx=1, pady=1)
        self.eight.grid(row=2, column=1, padx=1, pady=1)
        self.nine.grid(row=2, column=2, padx=1, pady=1)
        self.multiply.grid(row=2, column=3, padx=1, pady=1)

        # 4, 5, 6, -
        self.four = ttk.Button(self.btns_frame, text="4", width=10, command=lambda: self.btn_click("4"))
        self.five = ttk.Button(self.btns_frame, text="5", width=10, command=lambda: self.btn_click("5"))
        self.six = ttk.Button(self.btns_frame, text="6", width=10, command=lambda: self.btn_click("6"))
        self.minus = ttk.Button(self.btns_frame, text="-", width=10, command=lambda: self.btn_click("-"))
        self.four.grid(row=3, column=0, padx=1, pady=1)
        self.five.grid(row=3, column=1, padx=1, pady=1)
        self.six.grid(row=3, column=2, padx=1, pady=1)
        self.minus.grid(row=3, column=3, padx=1, pady=1)

        # 1, 2, 3, +
        self.one = ttk.Button(self.btns_frame, text="1", width=10, command=lambda: self.btn_click("1"))
        self.two = ttk.Button(self.btns_frame, text="2", width=10, command=lambda: self.btn_click("2"))
        self.three = ttk.Button(self.btns_frame, text="3", width=10, command=lambda: self.btn_click("3"))
        self.plus = ttk.Button(self.btns_frame, text="+", width=10, command=lambda: self.btn_click("+"))
        self.one.grid(row=4, column=0, padx=1, pady=1)
        self.two.grid(row=4, column=1, padx=1, pady=1)
        self.three.grid(row=4, column=2, padx=1, pady=1)
        self.plus.grid(row=4, column=3, padx=1, pady=1)

        # 0, ., =
        self.zero = ttk.Button(self.btns_frame, text="0", width=25, command=lambda: self.btn_click("0"))
        self.point = ttk.Button(self.btns_frame, text=".", width=10, command=lambda: self.btn_click("."))
        self.equals = ttk.Button(self.btns_frame, text="=", width=10, command=lambda: self.btn_equal())
        self.zero.grid(row=5, column=0, columnspan=2, padx=1, pady=1)
        self.point.grid(row=5, column=2, padx=1, pady=1)
        self.equals.grid(row=5, column=3, padx=1, pady=1)

    def btn_click(self, inputval):
        self.expression = self.expression + inputval
        self.input_text.set(self.expression)

    def btn_clear(self):
        self.expression = ""
        self.input_text.set("")

    def btn_equal(self):
        result = str(eval(self.expression))
        self.input_text.set(result)
        self.expression = ""


class Styles(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        self.configure("TFrame", background="silver")
        self.configure("TButton", foreground="black", background="white", padding=10, cursor="hand1")
        self.map("TButton", foreground=[("active", "maroon")], background=[("active", "coral")])
        self.configure("TEntry", foreground="grey", background="silver")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("MiniCalc - a minimalist calculator")
    root.appicon = tk.PhotoImage(file="icon_calc.png")
    root.iconphoto(False, root.appicon)
    root.geometry("360x280")
    root.resizable(0, 0)
    root.config(cursor="hand1")
    Styles()
    AppGUI(root)
    root.mainloop()
