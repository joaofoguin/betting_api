import requests
import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Módulos locais separados
from models import Base, Luta, IntegradorAutorizado
from acess_log import registrar_tentativa
from security import verificar_assinatura

# Puxa a string de conexão do Neon enviada pela Vercel. Se não houver, usa SQLite temporário
DATABASE_URL = os.getenv("POSTGRES_URL_NON_POOLING") or os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SENHA_ADMIN = os.getenv("SENHA_ADMIN", "admin_local")

# Cria as tabelas na nuvem automaticamente se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic import BaseModel
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

def verificar_admin(request: Request):
    # Lendo de forma crua para evitar filtros de proxy da Vercel
    x_admin_token = request.headers.get("X-Admin-Token") or request.headers.get("x-admin-token")
    if not x_admin_token or x_admin_token != SENHA_ADMIN:
        raise HTTPException(status_code=403, detail="Acesso negado: Token inválido.")

def validar_api_externa(request: Request, db: Session = Depends(get_db)):
    ip = request.headers.get("x-forwarded-for") or request.client.host
    rota = request.url.path

    # Busca os cabeçalhos de forma flexível (minúsculas ou maiúsculas)
    x_api_nome = request.headers.get("X-API-Nome") or request.headers.get("x-api-nome")
    x_assinatura = request.headers.get("X-Assinatura") or request.headers.get("x-assinatura")

    if not x_api_nome or not x_assinatura:
        registrar_tentativa(x_api_nome or "DESCONHECIDA", rota, ip, autorizado=False)
        raise HTTPException(status_code=401, detail="Cabeçalhos de autenticação ausentes")
    
    mensagem = f"{x_api_nome}:{rota}"
    
    # Chama a verificação
    assinatura_valida = verificar_assinatura(mensagem, x_assinatura, x_api_nome, db)

    # Registra o log (apenas print para a Vercel)
    registrar_tentativa(x_api_nome, rota, ip, autorizado=assinatura_valida)

    # CORREÇÃO DEFINITIVA: Verificação simples sem erro de sintaxe
    if not assinatura_valida:
        raise HTTPException(status_code=403, detail="Assinatura inválida")
    
    return True

# --- ROTAS ---
@app.get("/")
def home():
    return {"status": "API de Lutas na Vercel", "docs": "/docs"}

@app.post("/admin/cadastrar-integrador")
def cadastrar_integrador(nome_api: str, chave_publica: str, db: Session = Depends(get_db), admin_valido = Depends(verificar_admin)):
    novo_integrador = IntegradorAutorizado(nome_api=nome_api, chave_publica_pem=chave_publica)
    db.add(novo_integrador)
    db.commit()
    return {"msg": f"O grupo {nome_api} foi autorizado com sucesso!"}

@app.post("/lutas/")
def agendar_luta(luta: LutaBase, db: Session = Depends(get_db), autorizado: bool = Depends(validar_api_externa)):
    if luta.id_lutador1 == luta.id_lutador2:
        raise HTTPException(status_code=400, detail="IDs devem ser diferentes")
    if not verificar_lutador_na_outra_api(luta.id_lutador1) or not verificar_lutador_na_outra_api(luta.id_lutador2):
        raise HTTPException(status_code=404, detail="Lutador não existe na API externa")

    db_luta = Luta(**luta.dict())
    db.add(db_luta)
    db.commit()
    db.refresh(db_luta)
    return db_luta

@app.get("/lutas/")
def listar_lutas(request: Request, autorizado: bool = Depends(validar_api_externa), db: Session = Depends(get_db)):
    lutas = db.query(Luta).all()
    resultado = []
    for luta in lutas:
        nome1, nome2 = "Lutador Desconhecido", "Lutador Desconhecido"
        try:
            r1 = requests.get(f"https://api-lutadoressd.onrender.com/api/lutadores/{luta.id_lutador1}", timeout=4)
            r2 = requests.get(f"https://api-lutadoressd.onrender.com/api/lutadores/{luta.id_lutador2}", timeout=4)
            if r1.status_code == 200: nome1 = r1.json().get("apelido", "Lutador Desconhecido")
            if r2.status_code == 200: nome2 = r2.json().get("apelido", "Lutador Desconhecido")
        except: pass
        resultado.append({
            "id": luta.id, "data": luta.data, "horario": luta.horario,
            "id_lutador1": luta.id_lutador1, "id_lutador2": luta.id_lutador2,
            "nome_lutador1": nome1, "nome_lutador2": nome2
        })
    return resultado