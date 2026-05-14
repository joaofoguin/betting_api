from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

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
    id = Column(Integer, primary_key=True, index=True)
    nome_api = Column(String, unique=True, nullable=False) # Ex: "api_grupo1", "api_integrador"
    chave_publica_pem = Column(String, nullable=False)     # O texto completo do arquivo public_key.pem
    ativo = Column(Integer, default=1)                     # 1 para sim, 0 para bloqueado