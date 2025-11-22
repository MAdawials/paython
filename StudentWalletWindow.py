import tkinter as tk
import tkinter.messagebox as mb


from database_file import conn
from database_file import get_student_wallet, wallet_exists, get_balance, pay


class StudentWalletWindow:
    def __init__(self, student_id):
        self.student_id = student_id

        self.window = tk.Tk()
        self.window.title("KSUWallet - Student Wallet")
        self.window.geometry("420x350")

        # ============================

        try:
            data = get_student_wallet(student_id)
        except Exception as e:
            mb.showerror("Error", f"DB function missing:\n{e}")
            self.window.destroy()
            return

        if data is None:
            mb.showerror("Error", "Student wallet not found.")
            self.window.destroy()
            return

        self.wallet_number = data[0]
        self.balance = data[1]

        # ========== HEADER ==========
        tk.Label(self.window, text="Student Wallet", font=("Arial", 16, "bold")).pack(pady=10)

        # ========== WALLET INFO DISPLAY ==========
        info = tk.Frame(self.window)
        info.pack()

        tk.Label(info, text=f"Wallet Number: {self.wallet_number}", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        self.balance_label = tk.Label(info, text=f"Current Balance: {self.balance} SR", font=("Arial", 12))
        self.balance_label.grid(row=1, column=0, sticky="w")

        # ========== INPUTS ==========
        input_frame = tk.Frame(self.window)
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="Target Wallet Number:").grid(row=0, column=0, sticky="w")
        self.target_entry = tk.Entry(input_frame, width=20)
        self.target_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Amount to Pay:").grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(input_frame, width=20)
        self.amount_entry.grid(row=1, column=1)

        # ========== BUTTONS ==========
        btns = tk.Frame(self.window)
        btns.pack()

        tk.Button(btns, text="Pay", width=12, command=self.pay_action).grid(row=0, column=0, padx=10)
        tk.Button(btns, text="Back", width=12, command=self.go_back).grid(row=0, column=1, padx=10)

        self.window.mainloop()

    # ============================
    #          PAY LOGIC
    # ============================
    def pay_action(self):
        target = self.target_entry.get().strip()
        amount_str = self.amount_entry.get().strip()

        if not target.isdigit() or len(target) != 10:
            mb.showerror("Error", "Target wallet must be 10 digits.")
            return

        if target == self.wallet_number:
            mb.showerror("Error", "You cannot transfer to your own wallet.")
            return

        if not amount_str.isdigit():
            mb.showerror("Error", "Amount must be a number.")
            return

        amount = int(amount_str)
        if amount <= 0:
            mb.showerror("Error", "Amount must be greater than 0.")
            return

        # ============================

        try:
            if not wallet_exists(target):
                mb.showerror("Error", "Target wallet does not exist.")
                return
        except:
            mb.showerror("Error", "wallet_exists() function missing in database_file.")
            return

        # ============================

        try:
            current_balance = get_balance(self.wallet_number)
        except:
            mb.showerror("Error", "get_balance() function missing in database_file.")
            return

        if current_balance < amount:
            mb.showerror("Error", "There is not enough money.")
            return

        # ============================

        try:
            success = pay(self.wallet_number, target, amount)
        except:
            mb.showerror("Error", "pay() function missing or incomplete.")
            return

        if success:
            mb.showinfo("Success", f"Transferred {amount} SR to {target}")

            new_balance = get_balance(self.wallet_number)
            self.balance_label.config(text=f"Current Balance: {new_balance} SR")

            self.target_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
        else:
            mb.showerror("Error", "Payment failed.")

    # ============================
    #            BACK
    # ============================
    def go_back(self):
        self.window.destroy()
        mb.showinfo("Info", "Back to previous window.")

