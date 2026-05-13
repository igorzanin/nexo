# API — Arquivos, Tarefas de Implementação

## Pré-requisitos
- [ ] Backend de armazenamento implementado
- [ ] Rota de boards implementada

## Tarefas

- [ ] T-01, Implementar handler POST /files/{team_id}/{board_id}
  - Origem no legado: `server/api/files.go:handleUploadFile`
  - Critério de pronto: Upload via multipart; valida tamanho <= 100KB; retorna file_id
  - Confiança: 🟢

- [ ] T-02, Implementar handler GET /files/{team_id}/{board_id}/{file_id}
  - Origem no legado: `server/api/files.go:handleGetFile`
  - Critério de pronto: Download de arquivo por ID; 404 se não encontrado
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar upload e download de arquivo
- [ ] TT-02, Testar rejeição de arquivo > 100KB

## Ordem Sugerida
1. T-01 (upload) primeiro
2. T-02 (download) depois

## Lacunas Pendentes (🔴)
- 🔴 Backend de armazenamento: definir se filesystem local ou S3
