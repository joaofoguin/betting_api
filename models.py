from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Apostador(Base):
    __tablename__ = "apostadores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    chave_pix = Column(String, nullable=False)

class Lutador(Base):
    __tablename__ = "lutadores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    apelido = Column(String)
    arte = Column(String)

class Luta(Base):
    __tablename__ = "lutas"
    id = Column(Integer, primary_key=True, index=True)
    horario = Column(String, nullable=False)
    data = Column(String, nullable=False)
    id_lutador1 = Column(Integer, ForeignKey("lutadores.id"))
    id_lutador2 = Column(Integer, ForeignKey("lutadores.id"))
    
    lutador1 = relationship("Lutador", foreign_keys=[id_lutador1])
    lutador2 = relationship("Lutador", foreign_keys=[id_lutador2])

class Aposta(Base):
    __tablename__ = "apostas"
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, nullable=False)
    id_luta = Column(Integer, ForeignKey("lutas.id"))
    id_lutador = Column(Integer, ForeignKey("lutadores.id"))
    id_apostador = Column(Integer, ForeignKey("apostadores.id"))

    luta = relationship("Luta")
    lutador = relationship("Lutador")
    apostador = relationship("Apostador")
