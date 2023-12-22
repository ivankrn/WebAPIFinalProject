from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    bugs = relationship('Bug', back_populates='category')
    created = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())


class Bug(Base):
    __tablename__ = 'bugs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    priority = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='bugs')
    created = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())