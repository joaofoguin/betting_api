from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Apostador, Lutador, Luta, Aposta
from pydantic import BaseModel
from typing import List, Optional

# Configuração do Banco de Dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./betting.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Apostas - Sistemas Distribuídos")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (ideal para desenvolvimento local)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc)
    allow_headers=["*"],  # Permite todos os headers
)

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas Pydantic para Criação e Atualização
class ApostadorBase(BaseModel):
    nome: str
    idade: int
    chave_pix: str

class LutadorBase(BaseModel):
    nome: str
    categoria: str
    apelido: Optional[str] = None
    arte: Optional[str] = None

class LutaBase(BaseModel):
    horario: str
    data: str
    id_lutador1: int
    id_lutador2: int

class ApostaBase(BaseModel):
    valor: float
    id_luta: int
    id_lutador: int
    id_apostador: int

# --- ENDPOINTS PARA APOSTADORES ---

@app.post("/apostadores/", response_model=dict, tags=["Apostadores"])
def create_apostador(apostador: ApostadorBase, db: Session = Depends(get_db)):
    db_apostador = Apostador(**apostador.dict())
    db.add(db_apostador)
    db.commit()
    db.refresh(db_apostador)
    return {"id": db_apostador.id, "message": "Apostador criado com sucesso"}

@app.get("/apostadores/", tags=["Apostadores"])
def list_apostadores(db: Session = Depends(get_db)):
    return db.query(Apostador).all()

@app.put("/apostadores/{id}", tags=["Apostadores"])
def update_apostador(id: int, apostador: ApostadorBase, db: Session = Depends(get_db)):
    db_obj = db.query(Apostador).filter(Apostador.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Apostador não encontrado")
    for key, value in apostador.dict().items():
        setattr(db_obj, key, value)
    db.commit()
    return {"message": "Apostador atualizado com sucesso"}

@app.delete("/apostadores/{id}", tags=["Apostadores"])
def delete_apostador(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Apostador).filter(Apostador.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Apostador não encontrado")
    db.delete(db_obj)
    db.commit()
    return {"message": "Apostador removido com sucesso"}

# --- ENDPOINTS PARA LUTADORES ---

@app.post("/lutadores/", response_model=dict, tags=["Lutadores"])
def create_lutador(lutador: LutadorBase, db: Session = Depends(get_db)):
    db_lutador = Lutador(**lutador.dict())
    db.add(db_lutador)
    db.commit()
    db.refresh(db_lutador)
    return {"id": db_lutador.id, "message": "Lutador criado com sucesso"}

@app.get("/lutadores/", tags=["Lutadores"])
def list_lutadores(db: Session = Depends(get_db)):
    return db.query(Lutador).all()

@app.put("/lutadores/{id}", tags=["Lutadores"])
def update_lutador(id: int, lutador: LutadorBase, db: Session = Depends(get_db)):
    db_obj = db.query(Lutador).filter(Lutador.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Lutador não encontrado")
    for key, value in lutador.dict().items():
        setattr(db_obj, key, value)
    db.commit()
    return {"message": "Lutador atualizado com sucesso"}

@app.delete("/lutadores/{id}", tags=["Lutadores"])
def delete_lutador(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Lutador).filter(Lutador.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Lutador não encontrado")
    db.delete(db_obj)
    db.commit()
    return {"message": "Lutador removido com sucesso"}

# --- ENDPOINTS PARA LUTAS ---

@app.post("/lutas/", response_model=dict, tags=["Lutas"])
def create_luta(luta: LutaBase, db: Session = Depends(get_db)):
    db_luta = Luta(**luta.dict())
    db.add(db_luta)
    db.commit()
    db.refresh(db_luta)
    return {"id": db_luta.id, "message": "Luta agendada com sucesso"}

@app.get("/lutas/", tags=["Lutas"])
def list_lutas(db: Session = Depends(get_db)):
    return db.query(Luta).all()

@app.put("/lutas/{id}", tags=["Lutas"])
def update_luta(id: int, luta: LutaBase, db: Session = Depends(get_db)):
    db_obj = db.query(Luta).filter(Luta.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Luta não encontrada")
    for key, value in luta.dict().items():
        setattr(db_obj, key, value)
    db.commit()
    return {"message": "Luta atualizada com sucesso"}

@app.delete("/lutas/{id}", tags=["Lutas"])
def delete_luta(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Luta).filter(Luta.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Luta não encontrada")
    db.delete(db_obj)
    db.commit()
    return {"message": "Luta removida com sucesso"}

# --- ENDPOINTS PARA APOSTAS ---

@app.post("/apostas/", response_model=dict, tags=["Apostas"])
def create_aposta(aposta: ApostaBase, db: Session = Depends(get_db)):
    db_aposta = Aposta(**aposta.dict())
    db.add(db_aposta)
    db.commit()
    db.refresh(db_aposta)
    return {"id": db_aposta.id, "message": "Aposta realizada com sucesso"}

@app.get("/apostas/", tags=["Apostas"])
def list_apostas(db: Session = Depends(get_db)):
    return db.query(Aposta).all()

@app.put("/apostas/{id}", tags=["Apostas"])
def update_aposta(id: int, aposta: ApostaBase, db: Session = Depends(get_db)):
    db_obj = db.query(Aposta).filter(Aposta.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Aposta não encontrada")
    for key, value in aposta.dict().items():
        setattr(db_obj, key, value)
    db.commit()
    return {"message": "Aposta atualizada com sucesso"}

@app.delete("/apostas/{id}", tags=["Apostas"])
def delete_aposta(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Aposta).filter(Aposta.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Aposta não encontrada")
    db.delete(db_obj)
    db.commit()
    return {"message": "Aposta removida com sucesso"}

# Root endpoint
@app.get("/", tags=["Geral"])
def read_root():
    return {"status": "API Online", "message": "Bem-vindo ao sistema de apostas"}
