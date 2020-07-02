from sqlalchemy import Column, Integer, Float, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True, nullable=False)
    description = Column(String(), unique=False, nullable=True)
    price = Column(Float)
    tax = Column(Float)
    listed_since = Column(Date)
    manufacturer = Column(String(), unique=False, nullable=False)