# 🥊 API de Apostas em Lutas - Sistemas Distribuídos

Este projeto consiste em uma API RESTful desenvolvida para simular um sistema de apostas em lutas, como parte do trabalho da disciplina de Sistemas Distribuídos. A API permite o gerenciamento completo (CRUD - Create, Read, Update, Delete) de apostadores, lutadores, lutas e apostas.

## 🚀 Tecnologias Utilizadas

*   **Python 3.x**: Linguagem de programação principal.
*   **FastAPI**: Framework web moderno e de alta performance para construção de APIs.
*   **Uvicorn**: Servidor ASGI para rodar a aplicação FastAPI.
*   **SQLAlchemy**: ORM (Object-Relational Mapper) para interação com o banco de dados.
*   **SQLite**: Banco de dados leve e baseado em arquivo, ideal para prototipagem e desenvolvimento local.
*   **Pydantic**: Biblioteca para validação de dados e serialização com o FastAPI.

## 📋 Estrutura do Projeto

```
betting_api/
├── main.py         # Lógica principal da API e definição dos endpoints
├── models.py       # Definição dos modelos do banco de dados (SQLAlchemy)
├── betting.db      # Arquivo do banco de dados SQLite (gerado automaticamente)
├── API_Documentation.md # Documentação detalhada dos endpoints
└── index.html      # Interface web simples para interação com a API
```

## ⚙️ Configuração e Execução Local

Siga os passos abaixo para configurar e rodar a API no seu ambiente de desenvolvimento local.

### 1. Pré-requisitos

Certifique-se de ter o Python 3.x instalado em sua máquina.

### 2. Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd betting_api
```

### 3. Instalar Dependências

Instale as bibliotecas Python necessárias usando `pip`:

```bash
pip install -r requirements.txt
```

### 4. Rodar a API

Inicie o servidor Uvicorn. O `--reload` é útil para desenvolvimento, pois reinicia o servidor automaticamente a cada alteração no código.

```bash
python -m uvicorn main:app --reload
```

Se tudo ocorrer bem, você verá uma mensagem similar a esta:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     (Press CTRL+C to quit)
```

### 5. Acessar a API e Documentação

*   **API Root:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
*   **Documentação Interativa (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*   **Interface Web Simples:** Abra o arquivo `index.html` diretamente no seu navegador.

## 🌐 Deploy na Nuvem (Render.com)

Esta API está configurada para ser facilmente implantada em plataformas como o [Render.com](https://render.com), que oferece um plano gratuito para serviços web.

### Passos para Deploy no Render:

1.  **Crie uma conta no Render.com** e conecte seu repositório GitHub.
2.  Crie um **novo Web Service**.
3.  Configure as seguintes opções:
    *   **Runtime:** `Python 3`
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4.  O Render irá construir e implantar sua aplicação, fornecendo uma URL pública para acesso.

### Persistência do Banco de Dados no Render

Para que o banco de dados `betting.db` seja persistente no Render (e não seja resetado a cada deploy), você precisará configurar um **Disk** no Render e montá-lo no caminho onde o `betting.db` é criado. Consulte a documentação do Render sobre [Persistent Disks](https://render.com/docs/disks) para mais detalhes.

## 💾 Persistência do Banco de Dados (SQLite)

A API utiliza **SQLite**, que armazena os dados em um arquivo (`betting.db`) no diretório raiz do projeto. Isso significa que:

*   Os dados são **persistentes**: eles não são perdidos ao encerrar ou reiniciar a API.
*   Para **resetar** o banco de dados, basta parar a API, deletar o arquivo `betting.db` e iniciar a API novamente. Um novo arquivo vazio será criado.

## 📝 Documentação da API

Uma documentação detalhada dos endpoints, incluindo métodos HTTP, rotas e exemplos de `body` para requisições `POST` e `PUT`, pode ser encontrada no arquivo [API_Documentation.md](API_Documentation.md).

## 👨‍💻 Autores

* João Pedro Silva da Rosa Lima
* Armando Alves de Oliveira Braga
* Sophia Ishii Dognani

---

**Observação:** Para o deploy no Render, é crucial que o `main.py` esteja configurado para aceitar requisições de qualquer origem (CORS), o que já foi implementado na versão mais recente do arquivo. A URL pública da sua API no Render será gerada após o deploy bem-sucedido.
