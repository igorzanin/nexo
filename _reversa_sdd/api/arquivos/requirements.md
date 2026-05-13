# API — Arquivos (File Upload/Download)

## Visão Geral
Handlers REST para upload e download de arquivos anexados a boards. Suporta upload via multipart/form-data com progress tracking no frontend.

## Responsabilidades
- Upload de arquivos para um board
- Download de arquivos por ID
- Gerenciamento de limite de tamanho

## Regras de Negócio
- Upload deve pertencer a um team e board 🟢
- Limite de 100KB por arquivo 🟢

## Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| AR-RF01 | Upload de arquivo | Must | POST /files/{team}/{board} com multipart salva arquivo |
| AR-RF02 | Download de arquivo | Must | GET /files/{team}/{board}/{fileId} retorna binário |
| AR-RF03 | Validar limite de tamanho | Should | Arquivo > 100KB é rejeitado com 413 |

## Critérios de Aceitação

```gherkin
Dado um board existente
Quando faz upload de um arquivo válido (<100KB)
Então o arquivo é salvo e retorna file_id e nome (201)

Dado um arquivo previamente enviado
Quando faz download pelo file_id
Então o binário do arquivo é retornado (200)

Dado um board existente
Quando faz upload de um arquivo > 100KB
Então retorna 413 Payload Too Large
```

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server/api/files.go` | handleUploadFile, handleGetFile | 🟢 |
| `server/app/files.go` | UploadFile, GetFile | 🟢 |
