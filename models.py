from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

def current_timestamp():
    return datetime.utcnow()

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Primary key")
    username = Column(String(50), unique=True, nullable=False, comment="User login name")
    email = Column(String(100), unique=True, nullable=False, comment="User email address")
    password = Column(String(255), nullable=False, comment="Encrypted password")
    role = Column(String(20), nullable=False, default='staff', comment="User role (e.g., admin, staff)")
    created_at = Column(DateTime, nullable=False, default=current_timestamp, comment="Account creation date")
    updated_at = Column(DateTime, nullable=False, default=current_timestamp, comment="Last update date")

class Category(Base):
    __tablename__ = 'Categories'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Primary key")
    name = Column(String(100), unique=True, nullable=False, comment="Category name")
    description = Column(Text, comment="Optional category description")
    created_at = Column(DateTime, nullable=False, default=current_timestamp, comment="Category creation date")
    updated_at = Column(DateTime, nullable=False, default=current_timestamp, comment="Last update date")

    items = relationship('Item', back_populates='category')

class Item(Base):
    __tablename__ = 'Items'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Primary key")
    name = Column(String(100), nullable=False, comment="Item name")
    description = Column(Text, comment="Optional item description")
    category_id = Column(Integer, ForeignKey('Categories.id'), nullable=False, comment="Category ID (foreign key)")
    quantity = Column(Integer, nullable=False, default=0, comment="Quantity in stock")
    price = Column(Numeric(10, 2), nullable=False, comment="Price per unit")
    created_at = Column(DateTime, nullable=False, default=current_timestamp, comment="Item creation date")
    updated_at = Column(DateTime, nullable=False, default=current_timestamp, comment="Last update date")

    category = relationship('Category', back_populates='items')
    logs = relationship('Log', back_populates='item')

class Log(Base):
    __tablename__ = 'Logs'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Primary key")
    item_id = Column(Integer, ForeignKey('Items.id'), nullable=False, comment="Item ID (foreign key)")
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False, comment="User ID (foreign key)")
    action = Column(String(50), nullable=False, comment="Action performed (e.g., added, removed, updated)")
    quantity = Column(Integer, nullable=False, comment="Quantity affected")
    timestamp = Column(DateTime, nullable=False, default=current_timestamp, comment="Log timestamp")

    item = relationship('Item', back_populates='logs')
    user = relationship('User')
