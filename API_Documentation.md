# Documentação da API de Distribuição de Lutas

Esta API é responsável pelo agendamento e distribuição de lutas, integrando-se com um serviço externo de gerenciamento de lutadores.

## URL Base do Serviço
*   **Local:** `http://127.0.0.1:8000`
*   **Público:** `https://betting-api-hmup.onrender.com`

## Endpoints da API

| Método HTTP | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Verifica o status da API. |
| `POST` | `/lutas/` | Agenda uma nova luta (Valida IDs na API externa). |
| `GET` | `/lutas/` | Lista todas as lutas agendadas. |
| `GET` | `/lutas/{id}` | Obtém detalhes de uma luta específica. |
| `PUT` | `/lutas/{id}` | Atualiza os dados de uma luta. |
| `DELETE` | `/lutas/{id}` | Cancela uma luta agendada. |

## Integração com API Externa

A API possui uma lógica de integração para validar se os `id_lutador1` e `id_lutador2` existem em um serviço externo antes de permitir o agendamento.

### Exemplo de Corpo (Body) para Agendar Luta (`POST /lutas/`)

```json
{
  "evento": "UFC 300",
  "data": "2026-07-20",
  "horario": "23:00",
  "id_lutador1": 10,
  "id_lutador2": 25,
  "categoria": "Peso Pesado"
}
```

## Como Configurar a API Externa
No arquivo `main.py`, localize a variável `EXTERNAL_LUTADORES_API_URL` e substitua pela URL real do serviço de lutadores. A função `validar_lutador_externo` já está preparada para realizar a chamada via `requests`.
