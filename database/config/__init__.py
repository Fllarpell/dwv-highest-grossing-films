from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    url="postgresql+psycopg2://admin1:admin1@localhost:5432/films",
    echo=True,
    pool_pre_ping=True
)

Session = sessionmaker(bind=engine)

Base = declarative_base()

def create_tables(): 
    Base.metadata.create_all(engine)
