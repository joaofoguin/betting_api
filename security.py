import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from sqlalchemy.orm import Session
from models import IntegradorAutorizado 

def obter_chave_publica_do_banco(nome_api: str, db: Session):
    # Busca estritamente pelo nome cadastrado na tabela limpa
    integrador = db.query(IntegradorAutorizado).filter(
        IntegradorAutorizado.nome_api == nome_api
    ).first()

    if not integrador:
        return None

    chave_bytes = integrador.chave_publica_pem.encode("utf-8")
    return serialization.load_pem_public_key(chave_bytes)
    
def verificar_assinatura(mensagem: str, assinatura_base64: str, nome_api: str, db: Session) -> bool:
    try:
        public_key = obter_chave_publica_do_banco(nome_api, db)
        if not public_key:
            return False

        assinatura = base64.b64decode(assinatura_base64)
        
        public_key.verify(
            assinatura,
            mensagem.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except Exception as erro:
        print("Erro criptográfico interno:", erro)
        return False