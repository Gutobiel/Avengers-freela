# models.py
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import declarative_base
from database import Base
from datetime import datetime
Base = declarative_base()

class Herois(Base):
    __tablename__ = 'herois'
    id = Column(Integer, primary_key=True)
    nome = Column(String(150))
    superpoder = Column(String(150))
    raca = Column(String(150))
    data_entrada = Column(Date)
    data_saida = Column(Date)
    ativo = Column(Boolean, default=True)

    def __repr__(self):
        return f'<Herois(id={self.id}, nome={self.nome}, superpoder={self.superpoder}, raca={self.raca}, data_entrada={self.data_entrada}, data_saida={self.data_saida}, ativo={self.ativo})>'
