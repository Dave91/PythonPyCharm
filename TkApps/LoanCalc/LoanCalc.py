import tkinter as tk
from tkinter import ttk


class ToolsApp:
    def __init__(self):

        # ROOT WINDOW DETAILS
        root = tk.Tk()
        root.title("Loan Calculator")
        root.geometry("360x220")
        root.resizable(False, False)
        root.config(background="beige", cursor="gobbler",
                    padx=15, pady=15)

        # STYLES
        style = ttk.Style()
        style.configure("TLabel", background="beige")
        style.configure("TEntry", foreground="blue")
        style.configure("TButton", background="gold")
        style.configure("TFrame", background="beige")

        frame_left = ttk.Frame(root)
        frame_left.pack(side="left", expand=1, fill="both")
        frame_right = ttk.Frame(root)
        frame_right.pack(side="right", expand=1, fill="both")

        ttk.Label(frame_left, text="Annual Interest Rate").pack(pady=2)
        ttk.Label(frame_left, text="Number of Years").pack(pady=2)
        ttk.Label(frame_left, text="Loan Amount").pack(pady=2)
        ttk.Label(frame_left, text="Monthly Payment").pack(pady=2)
        ttk.Label(frame_left, text="Annual Payment").pack(pady=2)
        ttk.Label(frame_left, text="Total Payment").pack(pady=2)

        self.AnnualInterest = tk.StringVar()
        ttk.Entry(frame_right, textvariable=self.AnnualInterest, justify="right").pack(pady=2)

        self.years = tk.StringVar()
        ttk.Entry(frame_right, textvariable=self.years, justify="right").pack(pady=2)

        self.amount = tk.StringVar()
        ttk.Entry(frame_right, textvariable=self.amount, justify="right").pack(pady=2)

        self.monthlyPayment = tk.StringVar()
        ttk.Label(frame_right, textvariable=self.monthlyPayment).pack(pady=2)

        self.annualPayment = tk.StringVar()
        ttk.Label(frame_right, textvariable=self.annualPayment).pack(pady=2)

        self.TotalPayment = tk.StringVar()
        ttk.Label(frame_right, textvariable=self.TotalPayment).pack(pady=2)

        ttk.Button(frame_right, text="Compute", command=self.compute_payment).pack(pady=5)

        root.mainloop()

    # computes monthly, annual, total payment
    def compute_payment(self):

        month = self.get_monthly_payment(
            float(self.amount.get()),
            float(self.AnnualInterest.get()) / 1200,
            int(self.years.get()))

        self.monthlyPayment.set(format(month, '10.2f'))

        annual = float(self.monthlyPayment.get()) * 12
        self.annualPayment.set(format(annual, '10.2f'))

        total = float(self.annualPayment.get()) * int(self.years.get())
        self.TotalPayment.set(format(total, '10.2f'))

    # computing payments
    def get_monthly_payment(self, loan_amount, monthly_interest_rate, year_num):

        month = loan_amount * monthly_interest_rate / (
                1 - 1 / (1 + monthly_interest_rate) ** (year_num * 12))
        return month


if __name__ == "__main__":
    ToolsApp()
