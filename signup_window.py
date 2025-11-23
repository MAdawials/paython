import tkinter as tk
import tkinter.messagebox as mb
import re
import random
from datetime import datetime
from login_window import LoginWindow
from database_file import session, Wallet, Student

EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@student\.ksu\.edu\.sa$'
PHONE_REGEX = r'^05\d{8}$'


class SignUpWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("KSUWallet - Sign Up")
        self.window.geometry("420x350")

        self.top_frame = tk.Frame(self.window)
        self.bottom_frame = tk.Frame(self.window)

        tk.Label(self.top_frame, text="First Name:").grid(row=0, column=0, sticky="w")
        self.fn_entry = tk.Entry(self.top_frame, width=25)
        self.fn_entry.grid(row=0, column=1)

        tk.Label(self.top_frame, text="Last Name:").grid(row=1, column=0, sticky="w")
        self.ln_entry = tk.Entry(self.top_frame, width=25)
        self.ln_entry.grid(row=1, column=1)

        tk.Label(self.top_frame, text="Student ID (Must be 10 digits):").grid(row=2, column=0, sticky="w")
        self.id_entry = tk.Entry(self.top_frame, width=25)
        self.id_entry.grid(row=2, column=1)

        tk.Label(self.top_frame, text="Password (at least 6 chars):").grid(row=3, column=0, sticky="w")
        self.pw_entry = tk.Entry(self.top_frame, width=25, show="*")
        self.pw_entry.grid(row=3, column=1)

        tk.Label(self.top_frame, text="Email address:").grid(row=4, column=0, sticky="w")
        self.email_entry = tk.Entry(self.top_frame, width=25)
        self.email_entry.grid(row=4, column=1)

        tk.Label(self.top_frame, text="Phone number (05XXXXXXXX):").grid(row=5, column=0, sticky="w")
        self.phone_entry = tk.Entry(self.top_frame, width=25)
        self.phone_entry.grid(row=5, column=1)

        self.submit_btn = tk.Button(self.bottom_frame, text="Submit", width=12, command=self.submit)
        self.login_btn = tk.Button(self.bottom_frame, text="Login", width=12, command=self.open_login_window)

        self.submit_btn.grid(row=0, column=0, padx=10, pady=10)
        self.login_btn.grid(row=0, column=1, padx=10, pady=10)

        self.top_frame.pack(pady=20)
        self.bottom_frame.pack(pady=20)

        self.window.mainloop()

    def generate_wallet_number(self):
        return "".join(str(random.randint(0, 9)) for _ in range(10))

    def generate_unique_wallet_number(self):
        while True:
            wallet_num = self.generate_wallet_number()
            exists = session.query(Wallet).filter_by(WALLET_NUMBER=wallet_num).first()
            if exists is None:
                return wallet_num

    def submit(self):
        fn = self.fn_entry.get().strip()
        ln = self.ln_entry.get().strip()
        sid = self.id_entry.get().strip()
        pw = self.pw_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if fn == "":
            mb.showerror("Error", "First name cannot be empty.")
            return
        if " " in fn:
            mb.showerror("Error", "First name must be ONE word.")
            return
        for char in fn:
            if not ('a' <= char <= 'z' or 'A' <= char <= 'Z'):
                mb.showerror("Error", "First name cannot contain numbers or symbols.")
                return

        if ln == "":
            mb.showerror("Error", "Last name cannot be empty.")
            return
        if " " in ln:
            mb.showerror("Error", "Last name must be ONE word.")
            return
        for char in ln:
            if not ('a' <= char <= 'z' or 'A' <= char <= 'Z'):
                mb.showerror("Error", "Last name cannot contain numbers or symbols.")
                return

        if len(sid) != 10 or not sid.isdigit():
            mb.showerror("Error", "Student ID must be 10 digits.")
            return

        if len(pw) < 6:
            mb.showerror("Error", "Password must be at least 6 characters.")
            return

        if not re.match(EMAIL_REGEX, email):
            mb.showerror("Error", "Email must be: X@student.ksu.edu.sa")
            return

        if not re.match(PHONE_REGEX, phone):
            mb.showerror("Error", "Phone must be: 05XXXXXXXX")
            return

        existing = session.query(Student).filter_by(STUDENT_ID=sid).first()
        if existing:
            mb.showerror("Error", "Student already registered.")
            return

        wallet_number = self.generate_unique_wallet_number()
        created_time = datetime.now().replace(microsecond=0)


        new_wallet = Wallet(
            WALLET_NUMBER=wallet_number,
            WALLET_TYPE="student",
            BALANCE=1000,
            CREATED_AT=created_time
        )

        new_student = Student(
            STUDENT_ID=sid,
            FIRST_NAME=fn,
            LAST_NAME=ln,
            EMAIL=email,
            PHONE=phone,
            PASSWORD=pw,
            WALLET_NUMBER=wallet_number
        )

        session.add(new_wallet)
        session.add(new_student)
        session.commit()

        mb.showinfo(
            "Success",
            f"Student registered successfully!\n\n"
            f"Wallet Number: {wallet_number}\n"
            f"Created At: {created_time}\n"
            f"Type: student\n"
            f"Initial Balance: 1000 SR"
        )


    def open_login_window(self):
        self.window.destroy()
        LoginWindow()


if __name__ == "__main__":
    SignUpWindow()

