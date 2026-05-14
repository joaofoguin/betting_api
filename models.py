from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Luta(Base):
    __tablename__ = "lutas"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String, nullable=False)
    horario = Column(String, nullable=False)
    id_lutador1 = Column(Integer, nullable=False)
    id_lutador2 = Column(Integer, nullable=False)

class IntegradorAutorizado(Base):
    __tablename__ = "integradores_autorizados"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_api = Column(String, nullable=False, unique=True)
    chave_publica_pem = Column(String, nullable=False)

# Nova tabela para persistir os logs de segurança direto no Postgres
class LogAcesso(Base):
    __tablename__ = "logs_acesso"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_api = Column(String, nullable=False)
    rota = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    status = Column(String, nullable=False)
    ativo = Column(Integer, default=1, nullable=False)