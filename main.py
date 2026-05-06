import requests
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel

# 1. Configuração do Banco (Lutas)
SQLALCHEMY_DATABASE_URL = "sqlite:///./lutas_agendadas.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Luta(Base):
    __tablename__ = "lutas"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, nullable=False)
    horario = Column(String, nullable=False)
    id_lutador1 = Column(Integer, nullable=False)
    id_lutador2 = Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)

# 2. INICIALIZAÇÃO DO APP (Deve vir antes das rotas!)
app = FastAPI()

# 3. Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Pydantic e Dependências
class LutaBase(BaseModel):
    data: str
    horario: str
    id_lutador1: int
    id_lutador2: int

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def verificar_lutador_na_outra_api(id_lutador: int):
    try:
        r = requests.get(f"https://api-lutadoressd.onrender.com/api/lutadores/{id_lutador}", timeout=5)
        return r.status_code == 200
    except:
        return False

# 5. AGORA SIM, AS ROTAS (Depois que o 'app' já existe)
@app.post("/lutas/")
def agendar_luta(luta: LutaBase, db: Session = Depends(get_db)):
    if luta.id_lutador1 == luta.id_lutador2:
        raise HTTPException(status_code=400, detail="IDs devem ser diferentes")

    if not verificar_lutador_na_outra_api(luta.id_lutador1) or not verificar_lutador_na_outra_api(luta.id_lutador2):
        raise HTTPException(status_code=404, detail="Lutador não existe na API 8000")

    db_luta = Luta(**luta.dict())
    db.add(db_luta)
    db.commit()
    db.refresh(db_luta)
    return db_luta


@app.get("/lutas/{luta_id}")
def get_luta(luta_id: int, db: Session = Depends(get_db)):
    luta = db.query(Luta).filter(Luta.id == luta_id).first()
    if not luta:
        raise HTTPException(status_code=404, detail="Luta não encontrada")
    return luta

@app.get("/lutas/")
def listar_lutas(db: Session = Depends(get_db)):
    lutas = db.query(Luta).all()
    resultado = []

    for luta in lutas:
        # Busca os nomes na outra API usando o ID
        nome1 = "Lutador Desconhecido"
        nome2 = "Lutador Desconhecido"
        
        try:
            r1 = requests.get(f"https://api-lutadoressd.onrender.com/api/lutadores/{luta.id_lutador1}", timeout=5)
            r2 = requests.get(f"https://api-lutadoressd.onrender.com/api/lutadores/{luta.id_lutador2}", timeout=5)
            
            if r1.status_code == 200: nome1 = r1.json().get('nome')
            if r2.status_code == 200: nome2 = r2.json().get('nome')
        except:
            pass # Se a API 8000 cair, mantém "Desconhecido"

        # Montamos um objeto novo que inclui os nomes para o HTML
        resultado.append({
            "id": luta.id,
            "data": luta.data,
            "horario": luta.horario,
            "nome_lutador1": nome1,
            "nome_lutador2": nome2
        })
    
    return resultado

@app.delete("/lutas/{luta_id}")
def cancelar_luta(luta_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Luta).filter(Luta.id == luta_id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Luta não encontrada")
    
    db.delete(db_obj)
    db.commit()
    return {"message": "Luta cancelada com sucesso"}
