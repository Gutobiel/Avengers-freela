# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from database import Base, engine


Base = declarative_base()

class Herois(Base):
    __tablename__ = 'herois'
    id = Column(Integer, primary_key=True)
    nome = Column(String(150))
    superpoder = Column(String(150))
    raca = Column(String(150))

    def __repr__(self):
        return '<herois %r>' % (self.id)
# models.py

