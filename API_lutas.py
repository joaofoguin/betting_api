import requests
import os
from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

from models import Base, Luta, IntegradorAutorizado
from acess_log import registrar_tentativa
from security import verificar_assinatura
from rabbitmq_service import publicar_evento


DATABASE_URL = os.getenv("POSTGRES_URL_NON_POOLING") or os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SENHA_ADMIN = os.getenv("SENHA_ADMIN", "admin_local")

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LutaBase(BaseModel):
    data: str
    horario: str
    id_lutador1: int
    id_lutador2: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def lutador_existe(id_lutador: int) -> bool:
    try:
        r = requests.get(
            f"https://api-lutadoressd.onrender.com/api/lutadores/{id_lutador}",
            timeout=5
        )
        return r.status_code == 200

    except Exception as erro:
        print(f"[ERRO LUTADORES] ID {id_lutador}: {erro}")
        return False


def buscar_lutador_por_id(id_lutador: int):
    try:
        r = requests.get(
            f"https://api-lutadoressd.onrender.com/api/lutadores/{id_lutador}",
            timeout=5
        )

        if r.status_code == 404:
            return {"apelido": f"Lutador removido (ID {id_lutador})"}

        if r.status_code != 200:
            return {"apelido": f"Lutador indisponível (ID {id_lutador})"}

        return r.json()

    except Exception as erro:
        print(f"[ERRO LUTADORES] ID {id_lutador}: {erro}")
        return {"apelido": f"Lutador indisponível (ID {id_lutador})"}


def verificar_admin(x_admin_token: str = Header(None, alias="X-Admin-Token")):
    if not x_admin_token or x_admin_token != SENHA_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado: Token administrativo inválido."
        )

    return x_admin_token


def validar_api_externa(request: Request, db: Session = Depends(get_db)):
    ip = request.headers.get("x-forwarded-for") or request.client.host
    rota = request.url.path

    x_api_nome = request.headers.get("X-API-Nome") or request.headers.get("x-api-nome")
    x_assinatura = request.headers.get("X-Assinatura") or request.headers.get("x-assinatura")

    if not x_api_nome or not x_assinatura:
        registrar_tentativa(
            x_api_nome or "DESCONHECIDA",
            rota,
            ip,
            autorizado=False
        )
        raise HTTPException(
            status_code=401,
            detail="Cabeçalhos de autenticação ausentes"
        )

    mensagem = f"{x_api_nome}:{rota}"

    assinatura_valida = verificar_assinatura(
        mensagem,
        x_assinatura,
        x_api_nome,
        db
    )

    registrar_tentativa(
        x_api_nome,
        rota,
        ip,
        autorizado=assinatura_valida
    )

    if not assinatura_valida:
        raise HTTPException(status_code=403, detail="Assinatura inválida")

    return True


@app.get("/")
def home():
    return {
        "status": "API de Lutas na Vercel",
        "docs": "/docs"
    }


@app.post("/admin/cadastrar-integrador")
def cadastrar_integrador(
    nome_api: str,
    chave_publica: str,
    db: Session = Depends(get_db),
    admin_token: str = Depends(verificar_admin)
):
    integrador_existente = db.query(IntegradorAutorizado).filter(
        IntegradorAutorizado.nome_api == nome_api
    ).first()

    if integrador_existente:
        integrador_existente.chave_publica_pem = chave_publica
        db.commit()

        return {
            "msg": f"A chave pública do grupo {nome_api} foi atualizada com sucesso!"
        }

    novo_integrador = IntegradorAutorizado(
        nome_api=nome_api,
        chave_publica_pem=chave_publica
    )

    db.add(novo_integrador)
    db.commit()

    return {
        "msg": f"O grupo {nome_api} foi autorizado com sucesso!"
    }


@app.post("/lutas/")
def agendar_luta(
    luta: LutaBase,
    db: Session = Depends(get_db),
    autorizado: bool = Depends(validar_api_externa)
):
    if luta.id_lutador1 == luta.id_lutador2:
        raise HTTPException(
            status_code=400,
            detail="IDs devem ser diferentes"
        )

    if not lutador_existe(luta.id_lutador1) or not lutador_existe(luta.id_lutador2):
        raise HTTPException(
            status_code=404,
            detail="Um ou ambos os lutadores não existem na API externa"
        )

    db_luta = Luta(**luta.dict())

    db.add(db_luta)
    db.commit()
    db.refresh(db_luta)

    publicar_evento(
        "luta_criada",
        {
            "id": db_luta.id,
            "data": db_luta.data,
            "horario": db_luta.horario,
            "id_lutador1": db_luta.id_lutador1,
            "id_lutador2": db_luta.id_lutador2
        }
    )

    return db_luta


@app.get("/lutas/")
def listar_lutas(
    request: Request,
    autorizado: bool = Depends(validar_api_externa),
    db: Session = Depends(get_db)
):
    lutas = db.query(Luta).all()

    resultado = []

    for luta in lutas:
        lutador1 = buscar_lutador_por_id(luta.id_lutador1)
        lutador2 = buscar_lutador_por_id(luta.id_lutador2)

        nome1 = lutador1.get(
            "apelido",
            f"Lutador removido (ID {luta.id_lutador1})"
        )

        nome2 = lutador2.get(
            "apelido",
            f"Lutador removido (ID {luta.id_lutador2})"
        )

        resultado.append({
            "id": luta.id,
            "data": luta.data,
            "horario": luta.horario,
            "id_lutador1": luta.id_lutador1,
            "id_lutador2": luta.id_lutador2,
            "nome_lutador1": nome1,
            "nome_lutador2": nome2
        })

    return resultado


@app.delete("/lutas/{luta_id}")
def cancelar_luta(
    luta_id: int,
    db: Session = Depends(get_db),
    autorizado: bool = Depends(validar_api_externa)
):
    db_luta = db.query(Luta).filter(Luta.id == luta_id).first()

    if not db_luta:
        raise HTTPException(
            status_code=404,
            detail="Luta não encontrada"
        )

    db.delete(db_luta)
    db.commit()

    publicar_evento(
        "luta_cancelada",
        {
            "id": luta_id
        }
    )

    return {
        "message": f"Luta {luta_id} cancelada com sucesso"
    }


@app.put("/lutas/{luta_id}")
def editar_luta(
    luta_id: int,
    luta_atualizada: LutaBase,
    db: Session = Depends(get_db),
    autorizado: bool = Depends(validar_api_externa)
):
    db_luta = db.query(Luta).filter(Luta.id == luta_id).first()

    if not db_luta:
        raise HTTPException(
            status_code=404,
            detail="Luta não encontrada para edição"
        )

    if luta_atualizada.id_lutador1 == luta_atualizada.id_lutador2:
        raise HTTPException(
            status_code=400,
            detail="IDs dos lutadores devem ser diferentes"
        )

    if not lutador_existe(luta_atualizada.id_lutador1) or not lutador_existe(luta_atualizada.id_lutador2):
        raise HTTPException(
            status_code=404,
            detail="Um ou ambos os lutadores não existem na API externa"
        )

    db_luta.data = luta_atualizada.data
    db_luta.horario = luta_atualizada.horario
    db_luta.id_lutador1 = luta_atualizada.id_lutador1
    db_luta.id_lutador2 = luta_atualizada.id_lutador2

    db.commit()
    db.refresh(db_luta)

    publicar_evento(
        "luta_editada",
        {
            "id": db_luta.id,
            "data": db_luta.data,
            "horario": db_luta.horario,
            "id_lutador1": db_luta.id_lutador1,
            "id_lutador2": db_luta.id_lutador2
        }
    )

    return {
        "msg": "Luta atualizada com sucesso",
        "luta": db_luta
    }