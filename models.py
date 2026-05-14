from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Luta(Base):
    __tablename__ = "lutas"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, nullable=False)
    horario = Column(String, nullable=False)
    id_lutador1 = Column(Integer, nullable=False)
    id_lutador2 = Column(Integer, nullable=False)

class IntegradorAutorizado(Base):
    __tablename__ = "integradores_autorizados"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_api = Column(String, nullable=False, unique=True)
    chave_publica_pem = Column(String, nullable=False)