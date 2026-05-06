from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Luta
from pydantic import BaseModel
import requests
from typing import List, Optional

# Configuração do Banco de Dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./lutas.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Distribuição de Lutas - Sistemas Distribuídos")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL da API Externa de Lutadores (Para você alterar depois)
EXTERNAL_LUTADORES_API_URL = "https://api-exemplo-lutadores.com/lutadores"

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema Pydantic para Luta
class LutaBase(BaseModel):
    evento: str
    data: str
    horario: str
    id_lutador1: int
    id_lutador2: int
    categoria: str

# Função para validar lutador na API externa
def validar_lutador_externo(id_lutador: int):
    """
    Esta função simula a validação de um lutador em uma API externa.
    Quando você tiver a URL real, descomente o código abaixo.
    """
    # try:
    #     response = requests.get(f"{EXTERNAL_LUTADORES_API_URL}/{id_lutador}")
    #     return response.status_code == 200
    # except:
    #     return False
    
    # Por enquanto, vamos aceitar qualquer ID para você conseguir testar
    return True

# --- ENDPOINTS PARA LUTAS ---

@app.post("/lutas/", tags=["Distribuição de Lutas"])
def agendar_luta(luta: LutaBase, db: Session = Depends(get_db)):
    # Validação dos lutadores na API externa
    if not validar_lutador_externo(luta.id_lutador1) or not validar_lutador_externo(luta.id_lutador2):
        raise HTTPException(status_code=400, detail="Um ou ambos os lutadores não foram encontrados na API externa")
    
    if luta.id_lutador1 == luta.id_lutador2:
        raise HTTPException(status_code=400, detail="Um lutador não pode lutar contra si mesmo")

    db_luta = Luta(**luta.dict())
    db.add(db_luta)
    db.commit()
    db.refresh(db_luta)
    return {"id": db_luta.id, "message": "Luta agendada e distribuída com sucesso"}

@app.get("/lutas/", tags=["Distribuição de Lutas"])
def listar_lutas(db: Session = Depends(get_db)):
    return db.query(Luta).all()

@app.get("/lutas/{id}", tags=["Distribuição de Lutas"])
def obter_luta(id: int, db: Session = Depends(get_db)):
    luta = db.query(Luta).filter(Luta.id == id).first()
    if not luta:
        raise HTTPException(status_code=404, detail="Luta não encontrada")
    return luta

@app.put("/lutas/{id}", tags=["Distribuição de Lutas"])
def atualizar_luta(id: int, luta: LutaBase, db: Session = Depends(get_db)):
    db_obj = db.query(Luta).filter(Luta.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Luta não encontrada")
    
    for key, value in luta.dict().items():
        setattr(db_obj, key, value)
    
    db.commit()
    return {"message": "Luta atualizada com sucesso"}

@app.delete("/lutas/{id}", tags=["Distribuição de Lutas"])
def cancelar_luta(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Luta).filter(Luta.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Luta não encontrada")
    
    db.delete(db_obj)
    db.commit()
    return {"message": "Luta cancelada com sucesso"}

@app.get("/", tags=["Geral"])
def read_root():
    return {
        "status": "API de Distribuição Online",
        "message": "Pronta para agendar lutas consumindo dados externos"
    }
