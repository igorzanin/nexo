# API, Contratos REST

## Base URL
`/api/v1`

## Autenticação
Header `Authorization: Bearer <session_token>` na maioria das rotas.
Rotas públicas: `POST /login`, `POST /register`, `POST /signup`.

## Formatos
- Request/Response: `application/json`
- File upload: `multipart/form-data`
- File download: `application/octet-stream`

---

### Auth

#### POST /login
**Request:**
```json
{
  "username": "string",
  "password": "string",
  "type": "string (opcional)"
}
```
**Response 200:**
```json
{
  "id": "string",
  "token": "string",
  "user_id": "string",
  "team_id": "string",
  "create_at": 0,
  "update_at": 0
}
```
**Erros:** 401 se credenciais inválidas.

#### POST /register
**Request:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "register_token": "string (opcional)"
}
```
**Response 201:** `User` (sem senha)
**Erros:** 400 se dados inválidos ou email duplicado.

---

### Boards

#### GET /teams/{team_id}/boards
**Response 200:** `Board[]`

#### POST /boards
**Request:**
```json
{
  "team_id": "string",
  "title": "string",
  "type": "O|P",
  "minimum_role": "viewer|commenter|editor|admin|string vazia",
  "template_version": 0,
  "is_template": false
}
```
**Response 201:** `Board`
**Erros:** 400 se inválido, 403 sem permissão.

#### GET /boards/{board_id}
**Response 200:** `Board`
**Erros:** 404 se não encontrado.

#### PATCH /boards/{board_id}
**Request:** `BoardPatch` (campos parciais)
**Response 200:** `Board` atualizado
**Erros:** 400, 403.

#### DELETE /boards/{board_id}
**Response 200**
**Erros:** 403 sem permissão.

#### POST /boards/{board_id}/duplicate
**Response 201:** `Board` duplicado

---

### Blocks

#### GET /boards/{board_id}/blocks?parent_id={id}&type={type}
**Response 200:** `Block[]`

#### POST /boards/{board_id}/blocks
**Request:** `Block` ou `Block[]` (batch)
```json
{
  "id": "string (opcional, server gera se vazio)",
  "board_id": "string",
  "parent_id": "string",
  "type": "string",
  "title": "string (max 16383 runes)",
  "fields": {},
  "create_at": 0,
  "update_at": 0,
  "delete_at": 0
}
```
**Response 201:** `Block` ou `Block[]`
**Regra:** Todos os blocks batch devem pertencer ao mesmo board.

#### PATCH /boards/{board_id}/blocks/{block_id}
**Request:** `BlockPatch` (campos parciais)
**Response 200:** `Block` atualizado

#### DELETE /boards/{board_id}/blocks/{block_id}
**Response 200** (block marcado com delete_at; block inexistente não é erro)

---

### Cards

#### GET /boards/{board_id}/cards
**Response 200:** `Card[]`

#### POST /boards/{board_id}/cards
**Request:**
```json
{
  "board_id": "string",
  "properties": {},
  "content_order": ["string"],
  "icon": "string (max 1 grafema)",
  "create_at": 0,
  "update_at": 0
}
```
**Response 201:** `Card`

#### PATCH /boards/{board_id}/cards/{card_id}
**Response 200:** `Card`

#### DELETE /boards/{board_id}/cards/{card_id}
**Response 200**

---

### Categories

#### GET /boards/{board_id}/categories
**Response 200:** `Category[]`

#### POST /boards/{board_id}/categories
**Request:**
```json
{
  "name": "string",
  "user_id": "string",
  "team_id": "string",
  "type": "system|custom"
}
```
**Response 201:** `Category`

#### PATCH /boards/{board_id}/categories/{category_id}
**Response 200:** `Category`

#### DELETE /boards/{board_id}/categories/{category_id}
**Response 200** (soft-delete)

---

### Members

#### GET /boards/{board_id}/members
**Response 200:** `BoardMember[]`

#### POST /boards/{board_id}/members
**Request:**
```json
{
  "board_id": "string",
  "user_id": "string",
  "scheme_admin": false,
  "scheme_editor": false,
  "scheme_commenter": false,
  "scheme_viewer": false
}
```
**Response 201:** `BoardMember`

#### PUT /boards/{board_id}/members/{user_id}
**Response 200:** `BoardMember`

#### DELETE /boards/{board_id}/members/{user_id}
**Response 200**
**Regra:** Último admin não pode ser removido.

---

### Sharing

#### POST /boards/{board_id}/share
**Response 201:** `BoardSharing` (contém readToken)

#### GET /boards/{board_id}/sharing
**Response 200:** `BoardSharing`

#### DELETE /boards/{board_id}/sharing
**Response 200**

---

### Files

#### POST /files/{team_id}/{board_id}
**Request:** `multipart/form-data` com campo `file`
**Response 201:**
```json
{
  "file_id": "string",
  "name": "string"
}
```

#### GET /files/{team_id}/{board_id}/{file_id}
**Response 200:** binário do arquivo
**Erros:** 404

---

### Subscriptions

#### GET /subscriptions?block_id={block_id}
**Response 200:** `Subscription[]`

#### POST /subscriptions
**Request:**
```json
{
  "block_id": "string",
  "block_type": "string",
  "subscriber_id": "string",
  "subscriber_type": "user|channel"
}
```
**Response 201:** `Subscription`

#### DELETE /subscriptions/{subscription_id}
**Response 200**

---

### Admin

#### GET /admin/config
**Response 200:** `Configuration`
**Erros:** 403 se não for admin

#### PUT /admin/config
**Request:** `Configuration` (parcial)
**Response 200:** `Configuration`
**Erros:** 403 se não for admin
