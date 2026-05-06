from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Luta(Base):
    __tablename__ = "lutas"
    id = Column(Integer, primary_key=True, index=True)
    evento = Column(String, nullable=False) # Nome do evento (ex: UFC 300)
    data = Column(String, nullable=False)   # Data da luta
    horario = Column(String, nullable=False) # Horário da luta
    id_lutador1 = Column(Integer, nullable=False) # ID vindo da API externa
    id_lutador2 = Column(Integer, nullable=False) # ID vindo da API externa
    categoria = Column(String, nullable=False)    # Categoria de peso
