import tkinter as tk
from tkinter import ttk


class ToolsApp:
    def __init__(self):

        # ROOT WINDOW DETAILS
        root = tk.Tk()
        root.title("Toolkit Application")
        root.geometry("425x255")
        root.resizable(0, 0)
        root.config(background="beige", cursor="gobbler")

        # MENU ELEMENTS HERE
        menubar = tk.Menu(root)  # creating menu (under root)
        # File menu
        menu_file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=menu_file)
        menu_file.add_command(label='New', command=None)
        menu_file.add_command(label='Open', command=None)
        menu_file.add_command(label='Save', command=None)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=root.destroy)

        # Options menu
        menu_options = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Options', menu=menu_options)
        menu_options.add_command(label='Settings', command=None)
        # all in settings via new pop-up window??
        # or each detail in separate commands in submenu??
        # potential things to change:
        # styles: bg color, etc...
        # tabs: horizontal/vertical orientation
        # language eng/hun (with small flag icons) from dictionaries OR TXT LANG FILES INSTEAD??

        # Help menu
        menu_help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=menu_help)
        menu_help.add_command(label='About', command=None)

        root.config(menu=menubar)

        # STYLES for ttk widgets //USE style="stylename"??
        style = ttk.Style()
        style.configure("TLabel", background="beige")
        style.configure("TEntry", foreground="blue")
        style.configure("TButton", background="gold")
        style.configure("lefttab.TNotebook", tabposition="wn", background="#DAF7A6")
        style.configure("TNotebook.Tab", width=22, padding=(10, 5, 10, 5))
        style.configure("TFrame", background="beige")

        # TABS widget control
        tab_ctrl = ttk.Notebook(root, style="lefttab.TNotebook")
        tabloan = ttk.Frame(tab_ctrl)
        tabtemp = ttk.Frame(tab_ctrl)
        tabarea = ttk.Frame(tab_ctrl)
        tabspeed = ttk.Frame(tab_ctrl)
        tabgramm = ttk.Frame(tab_ctrl)
        tabnote = ttk.Frame(tab_ctrl)
        tabeff = ttk.Frame(tab_ctrl)
        tabfuel = ttk.Frame(tab_ctrl)

        # tab details
        toolsloan = tk.PhotoImage(file="icons/tools-loan.png")
        toolstemp = tk.PhotoImage(file="icons/tools-temp.png")
        toolsarea = tk.PhotoImage(file="icons/tools-area.png")
        toolsspeed = tk.PhotoImage(file="icons/tools-speed.png")
        toolsgramm = tk.PhotoImage(file="icons/tools-gramm.png")
        toolsnote = tk.PhotoImage(file="icons/tools-note.png")
        toolseff = tk.PhotoImage(file="icons/tools-eff.png")
        toolsfuel = tk.PhotoImage(file="icons/tools-fuel.png")

        tab_ctrl.add(tabloan, compound="left", image=toolsloan, text="Loan Calculator")
        tab_ctrl.add(tabtemp, compound="left", image=toolstemp, text="Temperature Converter")
        tab_ctrl.add(tabarea, compound="left", image=toolsarea, text="Area Unit Converter")
        tab_ctrl.add(tabspeed, compound="left", image=toolsspeed, text="Speed Unit Converter")
        tab_ctrl.add(tabgramm, compound="left", image=toolsgramm, text="Grammar Cheatsheet")
        tab_ctrl.add(tabnote, compound="left", image=toolsnote, text="Notes for Self")
        tab_ctrl.add(tabeff, compound="left", image=toolseff, text="Effective Stack Height")
        tab_ctrl.add(tabfuel, compound="left", image=toolsfuel, text="Fuel Expense Account")
        tab_ctrl.pack(expand=1, fill="both")

        # ---------- TAB LOAN ------------

        tabloan_left = ttk.Frame(tabloan)
        tabloan_left.pack(side="left", expand=1, fill="both")
        tabloan_right = ttk.Frame(tabloan)
        tabloan_right.pack(side="right", expand=1, fill="both")

        ttk.Label(tabloan_left, text="Annual Interest Rate").pack()
        ttk.Label(tabloan_left, text="Number of Years").pack()
        ttk.Label(tabloan_left, text="Loan Amount").pack()
        ttk.Label(tabloan_left, text="Monthly Payment").pack()
        ttk.Label(tabloan_left, text="Annual Payment").pack()
        ttk.Label(tabloan_left, text="Total Payment").pack()
        # ttk.Separator(tabloan_left, orient="horizontal").pack(expand=1, fill="x")

        self.AnnualInterest = tk.StringVar()
        ttk.Entry(tabloan_right, textvariable=self.AnnualInterest, justify="right").pack()

        self.years = tk.StringVar()
        ttk.Entry(tabloan_right, textvariable=self.years, justify="right").pack()

        self.amount = tk.StringVar()
        ttk.Entry(tabloan_right, textvariable=self.amount, justify="right").pack()

        self.monthlyPayment = tk.StringVar()
        ttk.Label(tabloan_right, textvariable=self.monthlyPayment).pack()

        self.annualPayment = tk.StringVar()
        ttk.Label(tabloan_right, textvariable=self.annualPayment).pack()

        self.TotalPayment = tk.StringVar()
        ttk.Label(tabloan_right, textvariable=self.TotalPayment).pack()

        ttk.Button(tabloan_right, text="Compute", command=lambda: self.progBar(tabloan)).pack()

        self.progress = ttk.Progressbar(tabloan_left, orient="horizontal", length=100)
        self.progress.pack()
        self.progress.config(mode="indeterminate", maximum=100)

        self.elapTimeLabel = tk.StringVar()
        ttk.Label(tabloan_left, textvariable=self.elapTimeLabel).pack()

        # --------------- TAB TEMP ------------------

        ttk.Label(tabtemp)

        temp_select = tk.StringVar()
        temp_select.set('Celsius to Fahrenheit')
        ttk.OptionMenu(tabtemp, temp_select, 'Celsius to Fahrenheit', 'Fahrenheit to Celsius')

        ttk.Entry(tabtemp)

        ttk.Button(tabtemp, text='Convert')

        # --------------- TAB AREA ------------------

        tabarea_left = ttk.Frame(tabarea)
        tabarea_left.pack(side="left")
        tabarea_right = ttk.Frame(tabarea)
        tabarea_right.pack(side="right")

        self.area_input = tk.StringVar()
        self.area_input.set(0)
        ttk.Entry(tabarea_left, textvariable=self.area_input, justify="right").pack()

        self.area_select = tk.StringVar()
        self.area_select.trace_add("write", self.ConvertArea)
        ttk.OptionMenu(tabarea_right, self.area_select, "(choose)", "m2", "nöl", "hold", "ha", "km2").pack()

        self.area_m2 = tk.StringVar()
        ttk.Label(tabarea_left, textvariable=self.area_m2, justify="right").pack()
        ttk.Label(tabarea_right, text="m2").pack()

        self.area_nol = tk.StringVar()
        ttk.Label(tabarea_left, textvariable=self.area_nol, justify="right").pack()
        ttk.Label(tabarea_right, text="nöl").pack()

        self.area_hold = tk.StringVar()
        ttk.Label(tabarea_left, textvariable=self.area_hold, justify="right").pack()
        ttk.Label(tabarea_right, text="hold").pack()

        self.area_ha = tk.StringVar()
        ttk.Label(tabarea_left, textvariable=self.area_ha, justify="right").pack()
        ttk.Label(tabarea_right, text="ha").pack()

        self.area_km2 = tk.StringVar()
        ttk.Label(tabarea_left, textvariable=self.area_km2, justify="right").pack()
        ttk.Label(tabarea_right, text="km2").pack()

        # --------------- TAB SPEED ------------------

        ttk.Label(tabspeed)

        # --------------- TAB GRAMM ------------------

        ttk.Label(tabgramm)

        # --------------- TAB NOTE ------------------

        ttk.Label(tabnote)

        # ---------------- TAB EFF ------------------

        c = tk.Canvas(tabeff, width=150, height=200, bg="white")
        c.pack()

        # ttk.Entry(tabeff)
        # entry
        # entry
        # d1 = entryvarname.get()
        # d2 =
        data = [5, 15]
        c_width = 150
        c_height = 200
        y_stretch = 10
        y_gap = 15
        x_stretch = 5
        x_width = 15
        x_gap = 15

        for x, y in enumerate(data):
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = c_height - y_gap
            # draws the bar
            c.create_rectangle(x0, y0, x1, y1, fill="red")
            # labels for bars (y values)
            c.create_text(x0 + 2, y0, anchor=tk.SW, text=str(y))

        # --------------- TAB FUEL -------------------

        ttk.Label(tabfuel)

        # ------- END OF TAB ELEMENTS -----------------

        # parts of an OPTIONS MENU maybe??
        self.eng = ['Annual Interest Rate', 'Number of Years', 'Loan Amount', 'Monthly Payment', 'Total Payment',
                    'Compute', 'Hun']
        self.hun = ['Éves Kamat (%)', 'Futamidő (Év)', 'Felvett összeg', 'Havi részlet', 'Teljes hitelösszeg', 'Számol',
                    'Eng']
        # self.lang = 'eng'

        # DO NOT CHANGE OR MOVE THIS!!
        root.mainloop()

    # METHODS
    # tabloan / progress bar, timer, starts compute
    def progBar(self, tabloan):
        import time

        # ONLY Numbers.. AND Not Null..
        # if self.AnnualInterest.get() == 0:
        # nested if?? or maybe that TRY method would be better

        self.progress.start(1)

        startTime = time.time()

        tabloan.update_idletasks()

        self.ComputePayment()  # starts compute func

        self.progress.stop()

        endTime = time.time()
        elapsedTime = endTime-startTime
        self.elapTimeLabel.set(format(elapsedTime, '10.3f') + ' s')

    # tabloan / computes monthly, annual, total payment
    def ComputePayment(self):

        month = self.getMonthlyPayment(
            float(self.amount.get()),
            float(self.AnnualInterest.get()) / 1200,
            int(self.years.get()))

        self.monthlyPayment.set(format(month, '10.2f'))

        annual = float(self.monthlyPayment.get()) * 12
        self.annualPayment.set(format(annual, '10.2f'))

        total = float(self.annualPayment.get()) * int(self.years.get())
        self.TotalPayment.set(format(total, '10.2f'))

    # tabloan / for computing payments
    def getMonthlyPayment(self, loanAmount, monthlyInterestRate, numberOfYears):

        month = loanAmount * monthlyInterestRate / (
            1 - 1 / (1 + monthlyInterestRate) ** (numberOfYears * 12))
        return month

    # tabarea / converts area units
    def ConvertArea(self, a, b, c):

        if self.area_select.get() == "m2":
            m2 = float(self.area_input.get())
        elif self.area_select.get() == "nöl":
            m2 = float(self.area_input.get()) * 3.597
        elif self.area_select.get() == "hold":
            m2 = float(self.area_input.get()) * 5754.642
        elif self.area_select.get() == "ha":
            m2 = float(self.area_input.get()) * 10000
        elif self.area_select.get() == "km2":
            m2 = float(self.area_input.get()) * 1000000
        else:
            m2 = 0

        self.area_m2.set(format(m2, '10.3f'))

        nol = float(self.area_m2.get()) / 3.597
        self.area_nol.set(format(nol, '10.3f'))

        hold = float(self.area_nol.get()) / 1600
        self.area_hold.set(format(hold, '10.3f'))

        ha = float(self.area_hold.get()) / 1.738
        self.area_ha.set(format(ha, '10.3f'))

        km2 = float(self.area_ha.get()) / 100
        self.area_km2.set(format(km2, '10.3f'))

    # further methods come here


ToolsApp()
