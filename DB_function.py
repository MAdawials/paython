

from datetime import datetime
from database_file import session, Wallet, Student, Admin, Entity, Transaction
import random



def generate_wallet_number():
    wallet_digits = ""
    for _ in range(10):
        wallet_digits += str(random.randint(0, 9))
    return wallet_digits


def generate_unique_wallet_number():
    while True:
        wallet_number = generate_wallet_number()
        exists = session.query(Wallet).filter_by(WALLET_NUMBER=wallet_number).first()
        if exists is None:
            return wallet_number



def create_student(student_id, first_name, last_name, email, phone, password):

    existing_student = session.query(Student).filter_by(
        STUDENT_ID=student_id
    ).first()

    if existing_student is not None:
        print("Error: student already registered")
        return

    wallet_number = generate_unique_wallet_number()

    new_wallet = Wallet(
        WALLET_NUMBER=wallet_number,
        WALLET_TYPE="student",
        BALANCE=1000,
        CREATED_AT=datetime.now()
    )

    new_student = Student(
        STUDENT_ID=student_id,
        FIRST_NAME=first_name,
        LAST_NAME=last_name,
        EMAIL=email,
        PHONE=phone,
        PASSWORD=password,
        WALLET_NUMBER=wallet_number
    )

    session.add(new_wallet)
    session.add(new_student)
    session.commit()

    print("Student created successfully")



def login(user_id, password):

    student = session.query(Student).filter_by(
        STUDENT_ID=user_id,
        PASSWORD=password
    ).first()

    if student is not None:
        print("Login as STUDENT")
        return "student"

    admin = session.query(Admin).filter_by(
        ADMIN_ID=user_id,
        PASSWORD=password
    ).first()

    if admin is not None:
        print("Login as ADMIN")
        return "admin"

    print("Invalid ID or password")
    return None



def pay(from_wallet_number, to_wallet_number, amount):

    source = session.query(Wallet).filter_by(WALLET_NUMBER=from_wallet_number).first()
    if  source is None:
        print("Source wallet does not exist")
        return

    target = session.query(Wallet).filter_by(WALLET_NUMBER=to_wallet_number).first()
    if  target is None:
        print("Target wallet does not exist")
        return

    if source.BALANCE < amount:
        print("Not enough balance")
        return

    source.BALANCE -= amount
    target.BALANCE += amount

    trx = Transaction(
        FROM_WALLET=from_wallet_number,
        TO_WALLET=to_wallet_number,
        AMOUNT=amount,
        CREATED_AT=datetime.now()
    )

    session.add(trx)
    session.commit()

    print("Payment completed successfully")



def add_entity(entity_name):

    existing = session.query(Entity).filter_by(NAME=entity_name).first()
    if existing is not None:
        print("Entity already exists")
        return

    wallet_number = generate_unique_wallet_number()

    new_wallet = Wallet(
        WALLET_NUMBER=wallet_number,
        WALLET_TYPE="ksu",
        BALANCE=0,
        CREATED_AT=datetime.now()
    )

    new_entity = Entity(
        NAME=entity_name,
        WALLET_NUMBER=wallet_number
    )

    session.add(new_wallet)
    session.add(new_entity)
    session.commit()

    print("Entity created successfully")



def pay_stipends():

    student_wallets = session.query(Wallet).filter_by(WALLET_TYPE="student").all()

    for wallet in student_wallets:
        wallet.BALANCE += 1000

        t = Transaction(
            FROM_WALLET=None,
            TO_WALLET=wallet.WALLET_NUMBER,
            AMOUNT=1000,
            CREATED_AT=datetime.now()
        )
        session.add(t)

    session.commit()

    print("Stipends paid successfully")



def cash_out():

    ksu_wallets = session.query(Wallet).filter_by(WALLET_TYPE="ksu").all()

    for wallet in ksu_wallets:

        if wallet.BALANCE > 0:

            trx = Transaction(
                FROM_WALLET=wallet.WALLET_NUMBER,
                TO_WALLET=None,
                AMOUNT=wallet.BALANCE,
                CREATED_AT=datetime.now()
            )

            session.add(trx)

        wallet.BALANCE = 0

    session.commit()

    print("Cash out completed")

def get_student_wallet(student_id):
    student = session.query(Student).filter_by(STUDENT_ID=student_id).first()
    if not student:
        return None

    wallet = session.query(Wallet).filter_by(WALLET_NUMBER=student.WALLET_NUMBER).first()
    if not wallet:
        return None

    return wallet.WALLET_NUMBER, wallet.BALANCE

def wallet_exists(wallet_number):
    exists = session.query(Wallet).filter_by(WALLET_NUMBER=wallet_number).first()
    return exists is not None

 def get_balance(wallet_number):
    wallet = session.query(Wallet).filter_by(WALLET_NUMBER=wallet_number).first()
    if wallet:
        return wallet.BALANCE
    return None

