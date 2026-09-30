from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(20), unique=True)
    full_name = Column(String(100))
    email = Column(String(100))

class Locker(Base):
    __tablename__ = "lockers"

    locker_id = Column(Integer, primary_key=True)
    locker_number = Column(String(20), unique=True)
    status = Column(String(20))

    deliveries = relationship("Delivery", back_populates="locker")

class Package(Base):
    __tablename__ = "packages"

    package_id = Column(Integer, primary_key=True)
    tracking_code = Column(String(100))
    status = Column(String(50))

    deliveries = relationship("Delivery", back_populates="package")

class Delivery(Base):
    __tablename__ = "deliveries"

    delivery_id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey("packages.package_id"))
    locker_id = Column(Integer, ForeignKey("lockers.locker_id"))

    package = relationship("Package", back_populates="deliveries")
    locker = relationship("Locker", back_populates="deliveries")