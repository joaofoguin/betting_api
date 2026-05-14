# 🥊 API de Apostas em Lutas - Sistemas Distribuídos (Microserviço)

Este projeto consiste em uma API RESTful desenvolvida para simular um sistema de agendamento e apostas em lutas. Ele foi construído como parte da disciplina de Sistemas Distribuídos, demonstrando a comunicação entre serviços independentes (interoperabilidade) e implementando uma **Arquitetura de Segurança M2M (Machine-to-Machine) com Criptografia RSA**.

> ⚠️ **Nota de Arquitetura:**  
> Este repositório contém apenas o **Microserviço de Backend**.  
> A interface web e o Gateway de autenticação de usuários residem em um repositório separado (Integrador).

---

# 🌐 URL de Acesso (Produção)

A API está hospedada e pronta para receber requisições em:

👉 `https://betting-api-hmup.onrender.com`

> *(Lembre-se: requisições diretas via navegador serão bloqueadas (Erro 401/403) devido à exigência de assinatura digital).*

---

# 🚀 Tecnologias Utilizadas

- **Python 3.11+** — Linguagem de programação principal.
- **FastAPI** — Framework moderno para construção de APIs de alta performance.
- **Cryptography** — Biblioteca para validação de assinaturas digitais RSA (*Zero Trust Security*).
- **Requests** — Biblioteca para comunicação síncrona entre APIs.
- **SQLAlchemy** — ORM para persistência de dados.
- **SQLite** — Banco de dados relacional baseado em arquivo.
- **Render.com** — Plataforma de hospedagem cloud.

---

# 📁 Estrutura do Projeto

```bash
betting_api/
├── main.py              # Lógica da API de Lutas e configuração de rotas
├── models.py            # Definição das tabelas do banco de dados
├── security.py          # Motor criptográfico para validação RSA
├── acess_log.py         # Sistema de auditoria e logs de requisições
├── public_key.pem       # Chave pública para validação das assinaturas
├── requirements.txt     # Dependências do projeto
├── lutas_agendadas.db   # Banco SQLite local (ignorado no Git)
└── API_Documentation.md # Documentação técnica dos endpoints
````

---

# 🛡️ Segurança M2M (Machine-to-Machine)

Para garantir que apenas o sistema oficial possa agendar ou cancelar lutas, esta API utiliza **Assinatura Digital RSA**.

## 🔐 Fluxo de Segurança

### 1. Recepção da Requisição

A API recebe uma requisição contendo os cabeçalhos:

```http
x-api-nome
x-assinatura
```

---

### 2. Validação Criptográfica (Local)

A API utiliza o arquivo:

```bash
public_key.pem
```

para verificar matematicamente se a assinatura foi gerada pelo Gateway oficial.

---

### 3. Validação Externa

Após validar a assinatura, a API realiza uma requisição HTTP GET para o microserviço de lutadores:

```bash
https://api-lutadoressd.onrender.com/api/lutas/
```

O objetivo é confirmar se os IDs enviados realmente existem.

---

### 4. Persistência

Somente após ambas as validações serem aprovadas:

* Assinatura RSA válida
* Lutadores existentes

a luta é salva no banco de dados local.

---

# ⚙️ Configuração e Execução Local

## 1️⃣ Pré-requisitos

Antes de iniciar:

* Ter o **Python 3.x** instalado.
* Possuir o arquivo `public_key.pem` na raiz do projeto.

---

## 2️⃣ Clonar o Repositório e Instalar Dependências

```bash
git clone https://github.com/joaofoguin/betting_api
cd betting_api

pip install -r requirements.txt
```

---

## 3️⃣ Executar a API Localmente

```bash
uvicorn API_lutadores:app --port 8001 --reload
```

A API estará disponível em:

👉 `http://127.0.0.1:8001`

---

# ☁️ Deploy no Render.com

A API já está configurada para deploy contínuo no Render.

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
uvicorn API_lutadores:app --host 0.0.0.0 --port $PORT
```

---

# 💾 Persistência no Render

Como o SQLite utiliza arquivos locais, os dados são resetados a cada novo deploy em plataformas cloud efêmeras (como o Render Free).

## ✅ Recomendação

Para persistência permanente:

* Utilizar um **Render Disk**
* Montar o disco no mesmo caminho do arquivo:

```bash
lutas_agendadas.db
```

---

# 🔄 Resetar Dados Localmente

1. Pare a execução da API.
2. Delete os arquivos:

```bash
lutas_agendadas.db
tentativas_acesso.log
```

3. Reinicie a API.

Os arquivos serão recriados automaticamente.

---

# 📚 Documentação Interativa

Para detalhes técnicos sobre os endpoints e payloads:

* Consulte o arquivo:

```bash
API_Documentation.md
```

* Ou acesse a documentação Swagger:

```bash
/docs
```

Exemplo:

```bash
https://betting-api-hmup.onrender.com/docs
```

> ⚠️ Observação:
> Testes via Swagger exigem configuração manual dos cabeçalhos RSA.

---

# 🧠 Conceitos de Sistemas Distribuídos Aplicados

Este projeto demonstra diversos conceitos estudados em Sistemas Distribuídos:

* Comunicação entre microserviços
* Arquitetura distribuída
* Segurança M2M
* Assinatura digital RSA
* Validação de identidade entre serviços
* Persistência de dados
* APIs RESTful
* Auditoria e logs
* Integração síncrona via HTTP

---

# 👨‍💻 Autores

* João Pedro Silva da Rosa Lima
* Armando Alves de Oliveira Braga
* Sophia Ishii Dognani

```
```
