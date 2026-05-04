# Documentação da API de Apostas (CRUD Completo)

Esta API RESTful permite gerenciar o ciclo de vida completo de um sistema de apostas em lutas.

## URL Base do Serviço
*   **Público:** `...`

## Endpoints da API

| Método HTTP | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Verifica o status da API. |
| **Apostadores** | | |
| `POST` | `/apostadores/` | Cria um novo apostador. |
| `GET` | `/apostadores/` | Lista todos os apostadores. |
| `PUT` | `/apostadores/{id}` | Atualiza dados de um apostador existente. |
| `DELETE` | `/apostadores/{id}` | Remove um apostador do sistema. |
| **Lutadores** | | |
| `POST` | `/lutadores/` | Cria um novo lutador. |
| `GET` | `/lutadores/` | Lista todos os lutadores. |
| `PUT` | `/lutadores/{id}` | Atualiza dados de um lutador. |
| `DELETE` | `/lutadores/{id}` | Remove um lutador. |
| **Lutas** | | |
| `POST` | `/lutas/` | Agenda uma nova luta. |
| `GET` | `/lutas/` | Lista todas as lutas. |
| `PUT` | `/lutas/{id}` | Atualiza dados de uma luta. |
| `DELETE` | `/lutas/{id}` | Cancela/Remove uma luta. |
| **Apostas** | | |
| `POST` | `/apostas/` | Realiza uma nova aposta. |
| `GET` | `/apostas/` | Lista todas as apostas. |
| `PUT` | `/apostas/{id}` | Altera o valor ou dados de uma aposta. |
| `DELETE` | `/apostas/{id}` | Remove uma aposta. |

## Exemplos de Corpo (Body) para PUT

O corpo para o `PUT` é idêntico ao do `POST`. A diferença é que você deve passar o `id` na URL.

### Exemplo: Atualizar Apostador (`PUT /apostadores/1`)
```json
{
  "nome": "João Silva Atualizado",
  "idade": 31,
  "chave_pix": "novo.pix@email.com"
}
```

## Como Testar
Acesse `/docs` no seu navegador para usar a interface interativa.
1. Clique no método desejado (PUT ou DELETE).
2. Clique em **Try it out**.
3. Preencha o campo `id` com o número do registro que deseja alterar ou excluir.
4. No caso do PUT, edite o JSON com as novas informações.
5. Clique em **Execute**.
