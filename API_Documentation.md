# 📄 Documentação da API de Distribuição de Lutas

Esta API é responsável pelo agendamento e distribuição de lutas, funcionando como um microserviço que valida dados em um serviço externo de lutadores.

---

## 🌐 URL Base do Serviço

- **Local**: http://127.0.0.1:8001  
- **Público**: https://betting-api-hmup.onrender.com  

---

## 📌 Endpoints da API

| Método HTTP | Rota        | Descrição |
|------------|------------|----------|
| GET        | /          | Verifica o status da API |
| POST       | /lutas/    | Agenda uma nova luta (valida IDs na API externa) |
| GET        | /lutas/    | Lista todas as lutas agendadas (com nomes dos lutadores) |
| GET        | /lutas/{id} | Obtém detalhes de uma luta específica por ID |
| DELETE     | /lutas/{id} | Cancela uma luta agendada e remove do banco |

---

## ⛓️ Integração Distribuída

A API realiza chamadas síncronas para o serviço de lutadores hospedado em:

👉 https://onrender.com  

O agendamento só é confirmado se ambos os lutadores retornarem **status 200 OK** na API externa.

---

## 📥 Estrutura de Dados para Agendamento (POST /lutas/)

Para agendar uma luta, envie um JSON com os campos obrigatórios:

```json
{
  "data": "2026-07-20",
  "horario": "23:00",
  "id_lutador1": 1,
  "id_lutador2": 2
}
```

---

## 📤 Resposta de Listagem (GET /lutas/)

A API retorna dados agregados, buscando os nomes dos lutadores em tempo real:

```json
[
  {
    "id": 1,
    "data": "2026-07-20",
    "horario": "23:00",
    "nome_lutador1": "Anderson Silva",
    "nome_lutador2": "Alex Poatan"
  }
]
```

---

## ⚠️ Tratamento de Erros Comuns

- **400 Bad Request**: IDs dos lutadores são iguais  
- **404 Not Found**: Um ou ambos os IDs não existem na API externa  
- **500 Internal Server Error**: Falha de conexão ou timeout com a API externa  

---

## 💡 Dica de Implementação

A função `verificar_lutador_na_outra_api` no código fonte:

- Gerencia exceções de rede  
- Evita que o sistema trave caso o serviço externo esteja instável  
