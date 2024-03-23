from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Contact(Base):
    """
    Ім'я
    Прізвище
    Електронна адреса
    Номер телефону
    День народження
    Додаткові дані (необов'язково)
    """

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    birthday = Column(Date)
    comments = Column(Text)
    favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
