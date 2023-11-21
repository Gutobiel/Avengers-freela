# models.py
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import declarative_base
from database import Base

Base = declarative_base()

class Herois(Base):
    __tablename__ = 'herois'
    id = Column(Integer, primary_key=True)
    nome = Column(String(150))
    superpoder = Column(String(150))
    raca = Column(String(150))
    ativo = Column(Boolean, default=True)

    def __repr__(self):
        return '<Herois %r>' % (self.id)
