🥊 API de Apostas em Lutas - Sistemas Distribuídos

Este projeto consiste em uma API RESTful desenvolvida para simular um sistema de agendamento e apostas em lutas. Ele foi construído como parte da disciplina de Sistemas Distribuídos, demonstrando a comunicação entre serviços independentes (interoperabilidade) para validação de dados em tempo real.

---

## 🌐 URL de Acesso (Produção)

A API está hospedada e pronta para receber requisições em:

👉 https://betting-api-hmup.onrender.com

---

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**: Linguagem de programação principal  
- **FastAPI**: Framework moderno para construção de APIs de alta performance  
- **Requests**: Biblioteca para comunicação síncrona entre APIs (consumo de microserviços)  
- **SQLAlchemy**: ORM para persistência de dados  
- **SQLite**: Banco de dados relacional baseado em arquivo  
- **Render.com**: Plataforma de hospedagem cloud  

---

## 📋 Estrutura do Projeto

```bash
betting_api/
├── main.py              # Lógica da API de Lutas e integração com API externa
├── models.py            # Definição das tabelas (Lutas e Lutadores)
├── requirements.txt     # Dependências (fastapi, uvicorn, sqlalchemy, requests)
├── lutas_agendadas.db   # Banco de dados SQLite local
└── index.html           # Interface web para agendamento de lutas
```

---

## ⚙️ Configuração e Execução Local

### 1. Pré-requisitos

- Ter o **Python 3.x** instalado

### 2. Clonar e Instalar

```bash
git clone https://github.com/joaofoguin/betting_api
cd betting_api
pip install -r requirements.txt
```

### 3. Rodar a API Localmente

```bash
python -m uvicorn main:app --port 8001 --reload
```

A API de Lutas rodará em:

👉 http://127.0.0.1:8001

---

## ⛓️ Arquitetura Distribuída

Para validar um agendamento, esta API consome dados de um serviço externo de lutadores.

- **API de Consumo**: https://onrender.com  

### 🔄 Fluxo

Ao agendar uma luta, a API:

1. Faz uma requisição HTTP para o serviço externo  
2. Verifica se os IDs dos lutadores existem  
3. Apenas persiste a luta localmente se os dados forem válidos  

---

## ⚙️ Deploy no Render.com

A API já está configurada para deploy contínuo no Render com as seguintes especificações:

- **Build Command**:
```bash
pip install -r requirements.txt
```

- **Start Command**:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 💾 Persistência no Render

Como o SQLite é baseado em arquivo, os dados são resetados a cada novo deploy.

👉 Para persistência permanente na nuvem, recomenda-se:
- Utilizar um **Render Disk**  
- Montar no caminho do arquivo `.db`  

---

## 💾 Gerenciamento do Banco de Dados

- Os dados são armazenados em `lutas_agendadas.db`

### 🔄 Resetar Dados

1. Pare a execução da API  
2. Delete o arquivo `.db`  
3. Ele será recriado automaticamente na próxima inicialização  

---

## 📚 Documentação Interativa

Acesse:

👉 `/docs`

na URL da API para testar os endpoints via **Swagger UI**

---

## 👨‍💻 Autores

- João Pedro Silva da Rosa Lima  
- Armando Alves de Oliveira Braga  
- Sophia Ishii Dognani  
