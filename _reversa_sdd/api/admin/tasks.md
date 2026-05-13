# API — Administração, Tarefas de Implementação

## Pré-requisitos
- [ ] Sistema de autenticação e roles implementado
- [ ] Serviço de configuração implementado

## Tarefas

- [ ] T-01, Implementar handler GET /admin/config
  - Origem no legado: `server/api/admin.go:handleGetConfig`
  - Critério de pronto: Retorna config atual; 403 se não admin
  - Confiança: 🟢

- [ ] T-02, Implementar handler PUT /admin/config
  - Origem no legado: `server/api/admin.go:handleSetConfig`
  - Critério de pronto: Atualiza config; broadcast via WebSocket
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar acesso admin vs não-admin
- [ ] TT-02, Testar leitura e escrita de configuração

## Ordem Sugerida
1. T-01 (GET) primeiro
2. T-02 (PUT) depois

## Lacunas Pendentes (🔴)
- 🔴 Campos exatos da Configuration expostos via API
