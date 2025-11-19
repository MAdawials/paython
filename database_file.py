import sqlite3 as db

conn = db.connect('ksuwallet.db')

conn.execute("""
CREATE TABLE IF NOT EXISTS wallets (
    WALLET_NUMBER TEXT PRIMARY KEY,
    WALLET_TYPE TEXT NOT NULL,    
    BALANCE INTEGER NOT NULL,
    CREATED_AT TEXT NOT NULL
);
""")


conn.execute("""
             CREATE TABLE IF NOT EXISTS students
             (
                 STUDENT_ID
                 TEXT
                 PRIMARY
                 KEY,
                 FIRST_NAME
                 TEXT
                 NOT
                 NULL,
                 LAST_NAME
                 TEXT
                 NOT
                 NULL,
                 EMAIL
                 TEXT
                 NOT
                 NULL,
                 PHONE
                 TEXT
                 NOT
                 NULL,
                 PASSWORD
                 TEXT
                 NOT
                 NULL,
                 WALLET_NUMBER
                 TEXT,
                 FOREIGN
                 KEY
             (
                 WALLET_NUMBER
             ) REFERENCES wallets
             (
                 WALLET_NUMBER
             )
                 );
             """)

conn.execute("""
             CREATE TABLE IF NOT EXISTS admins
             (
                 ADMIN_ID
                 TEXT
                 PRIMARY
                 KEY,
                 NAME
                 TEXT
                 NOT
                 NULL,
                 PASSWORD
                 TEXT
                 NOT
                 NULL
             );
             """)

conn.execute("""
             CREATE TABLE IF NOT EXISTS entities
             (
                 ENTITY_ID
                 INTEGER
                 PRIMARY
                 KEY
                 AUTOINCREMENT,
                 NAME
                 TEXT
                 UNIQUE
                 NOT
                 NULL,
                 WALLET_NUMBER
                 TEXT,
                 FOREIGN
                 KEY
             (
                 WALLET_NUMBER
             ) REFERENCES wallets
             (
                 WALLET_NUMBER
             )
                 );
             """)

conn.execute("""
             CREATE TABLE IF NOT EXISTS transactions
             (
                 TRANS_ID
                 INTEGER
                 PRIMARY
                 KEY
                 AUTOINCREMENT,
                 FROM_WALLET
                 TEXT,
                 TO_WALLET
                 TEXT,
                 AMOUNT
                 INTEGER
                 NOT
                 NULL,
                 CREATED_AT
                 TEXT
                 NOT
                 NULL,
                 FOREIGN
                 KEY
             (
                 FROM_WALLET
             ) REFERENCES wallets
             (
                 WALLET_NUMBER
             ),
                 FOREIGN KEY
             (
                 TO_WALLET
             ) REFERENCES wallets
             (
                 WALLET_NUMBER
             )
                 );
             """)
######################################################
from database_file import conn
import sqlite3 as db
import random


def generate_wallet_number():
    wallet_digits = ''

    for _ in range(10):
        r = str(random.randint(0, 9))
        wallet_digits = wallet_digits + r

    return wallet_digits


def generate_unique_wallet_number():
    while True:
        wallet_number = generate_wallet_number()
        result = conn.execute("""
                              SELECT WALLET_NUMBER
                              FROM wallets
                              WHERE WALLET_NUMBER = :wallet_number
                              """, {"wallet_number": wallet_number}).fetchone()

        if result is None:
            return wallet_number


def create_student(student_id, first_name, last_name, email, phone, password):
    existing_student = conn.execute("""
                                    SELECT STUDENT_ID
                                    FROM students
                                    WHERE STUDENT_ID = :student_id
                                    """, {"student_id": student_id}).fetchone()

    if existing_student is not None:
        print("Error: student already registered")
        return

    wallet_number = generate_unique_wallet_number()

    conn.execute("""
                 INSERT INTO wallets (WALLET_NUMBER, WALLET_TYPE, BALANCE, CREATED_AT)
                 VALUES (:wallet_number, 'student', 1000, 'unknown')
                 """, {"wallet_number": wallet_number})

    conn.execute("""
                 INSERT INTO students (STUDENT_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, PASSWORD, WALLET_NUMBER)
                 VALUES (:student_id, :first_name, :last_name, :email, :phone, :password, :wallet_number)
                 """, {
                     "student_id": student_id,
                     "first_name": first_name,
                     "last_name": last_name,
                     "email": email,
                     "phone": phone,
                     "password": password,
                     "wallet_number": wallet_number
                 })

    print("Student created successfully")


def login(user_id, password):
    student = conn.execute("""
                           SELECT *
                           FROM students
                           WHERE STUDENT_ID = :user_id
                             AND PASSWORD = :password
                           """, {"user_id": user_id, "password": password}).fetchone()

    if student is not None:
        print("Login as STUDENT")
        return "student"

    admin = conn.execute("""
                         SELECT *
                         FROM admins
                         WHERE ADMIN_ID = :user_id
                           AND PASSWORD = :password
                         """, {"user_id": user_id, "password": password}).fetchone()

    if admin is not None:
        print("Login as ADMIN")
        return "admin"

    print("Invalid ID or password")
    return None


def pay(from_wallet_number, to_wallet_number, amount):
    source_wallet = conn.execute("""
                                 SELECT BALANCE
                                 FROM wallets
                                 WHERE WALLET_NUMBER = :wallet_number
                                 """, {"wallet_number": from_wallet_number}).fetchone()

    if source_wallet is None:
        print("Source wallet does not exist")
        return

    target_wallet = conn.execute("""
                                 SELECT BALANCE
                                 FROM wallets
                                 WHERE WALLET_NUMBER = :wallet_number
                                 """, {"wallet_number": to_wallet_number}).fetchone()

    if target_wallet is None:
        print("Target wallet does not exist")
        return

    if source_wallet.BALANCE < amount:
        print("Not enough balance")
        return

    conn.execute("""
                 UPDATE wallets
                 SET BALANCE = :new_balance
                 WHERE WALLET_NUMBER = :wallet_number
                 """, {
                     "new_balance": source_wallet.BALANCE - amount,
                     "wallet_number": from_wallet_number
                 })

    conn.execute("""
                 UPDATE wallets
                 SET BALANCE = :new_balance
                 WHERE WALLET_NUMBER = :wallet_number
                 """, {
                     "new_balance": target_wallet.BALANCE + amount,
                     "wallet_number": to_wallet_number
                 })

    conn.execute("""
                 INSERT INTO transactions (FROM_WALLET, TO_WALLET, AMOUNT, CREATED_AT)
                 VALUES (:from_wallet, :to_wallet, :amount, 'unknown')
                 """, {
                     "from_wallet": from_wallet_number,
                     "to_wallet": to_wallet_number,
                     "amount": amount
                 })

    print("Payment completed successfully")


def add_entity(entity_name):
    existing_entity = conn.execute("""
                                   SELECT NAME
                                   FROM entities
                                   WHERE NAME = :entity_name
                                   """, {"entity_name": entity_name}).fetchone()

    if existing_entity is not None:
        print("Entity already exists")
        return

    wallet_number = generate_unique_wallet_number()

    conn.execute("""
                 INSERT INTO wallets (WALLET_NUMBER, WALLET_TYPE, BALANCE, CREATED_AT)
                 VALUES (:wallet_number, 'ksu', 0, 'unknown')
                 """, {"wallet_number": wallet_number})

    conn.execute("""
                 INSERT INTO entities (NAME, WALLET_NUMBER)
                 VALUES (:entity_name, :wallet_number)
                 """, {"entity_name": entity_name, "wallet_number": wallet_number})

    print("Entity created successfully")


def pay_stipends():
    student_wallets = conn.execute("""
                                   SELECT WALLET_NUMBER, BALANCE
                                   FROM wallets
                                   WHERE WALLET_TYPE = 'student'
                                   """).fetchall()  # select all

    for wallet in student_wallets:
        conn.execute("""
                     UPDATE wallets
                     SET BALANCE = :new_balance
                     WHERE WALLET_NUMBER = :wallet_number
                     """, {"new_balance": wallet.BALANCE + 1000,
                           "wallet_number": wallet.WALLET_NUMBER})

        conn.execute("""
                     INSERT INTO transactions (FROM_WALLET, TO_WALLET, AMOUNT, CREATED_AT)
                     VALUES (NULL, :wallet_number, 1000, 'unknown')
                     """, {"wallet_number": wallet.WALLET_NUMBER})

    print("Stipends paid successfully")


def cash_out():
    ksu_wallets = conn.execute("""
                               SELECT WALLET_NUMBER, BALANCE
                               FROM wallets
                               WHERE WALLET_TYPE = 'ksu'
                               """).fetchall()

    for wallet in ksu_wallets:

        if wallet.BALANCE > 0:
            conn.execute("""
                         INSERT INTO transactions (FROM_WALLET, TO_WALLET, AMOUNT, CREATED_AT)
                         VALUES (:wallet_number, NULL, :amount, 'unknown')
                         """, {"wallet_number": wallet.WALLET_NUMBER,
                               "amount": wallet.BALANCE})

        conn.execute("""
                     UPDATE wallets
                     SET BALANCE = 0
                     WHERE WALLET_NUMBER = :wallet_number
                     """, {"wallet_number": wallet.WALLET_NUMBER})

    print("Cash out completed")


