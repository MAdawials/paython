
from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import random

DATABASE_PATH = "sqlite:///ksuwallet.db"

engine = create_engine(DATABASE_PATH, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()



class Wallet(Base):
    __tablename__ = "wallets"

    WALLET_NUMBER = Column(String, primary_key=True)
    WALLET_TYPE = Column(String, nullable=False)
    BALANCE = Column(Integer, nullable=False)
    CREATED_AT = Column(DateTime, default=datetime.now)



class Student(Base):
    __tablename__ = "students"

    STUDENT_ID = Column(String, primary_key=True)
    FIRST_NAME = Column(String, nullable=False)
    LAST_NAME = Column(String, nullable=False)
    EMAIL = Column(String, nullable=False)
    PHONE = Column(String, nullable=False)
    PASSWORD = Column(String, nullable=False)

    WALLET_NUMBER = Column(String, ForeignKey("wallets.WALLET_NUMBER"))



class Admin(Base):
    __tablename__ = "admins"

    ADMIN_ID = Column(String, primary_key=True)
    NAME = Column(String, nullable=False)
    PASSWORD = Column(String, nullable=False)



class Entity(Base):
    __tablename__ = "entities"

    ENTITY_ID = Column(Integer, primary_key=True, autoincrement=True)
    NAME = Column(String, unique=True, nullable=False)
    WALLET_NUMBER = Column(String, ForeignKey("wallets.WALLET_NUMBER"))



class Transaction(Base):
    __tablename__ = "transactions"

    TRANS_ID = Column(Integer, primary_key=True, autoincrement=True)
    FROM_WALLET = Column(String, ForeignKey("wallets.WALLET_NUMBER"))
    TO_WALLET = Column(String, ForeignKey("wallets.WALLET_NUMBER"))
    AMOUNT = Column(Integer, nullable=False)
    CREATED_AT = Column(DateTime, default=datetime.now)



Base.metadata.create_all(engine)

default_admin = session.query(Admin).first()

if default_admin is None:
    admin = Admin(
        ADMIN_ID="1233211233",
        NAME="Main Admin",
        PASSWORD="Admin123"
    )
    session.add(admin)
    session.commit()
    print("Default admin created.")
else:
    print("Admin already exists.")


