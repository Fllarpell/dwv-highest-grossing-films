from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, REAL
from ..config import Base

class Film(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_year = Column(Integer)
    director = Column(String)
    box_office = Column(REAL)
    country = Column(String)
    image_url = Column(String)
