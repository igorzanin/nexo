# API — Equipes, Tarefas de Implementação

## Pré-requisitos
- [ ] Modelo Team implementado
- [ ] Store com operações de team implementada

## Tarefas

- [ ] T-01, Implementar handler GET /teams
  - Origem no legado: `server/api/teams.go:handleGetTeams`
  - Critério de pronto: Retorna equipes do usuário filtradas por user_id
  - Confiança: 🟢

- [ ] T-02, Implementar handler POST /teams
  - Origem no legado: `server/api/teams.go:handleCreateTeam`
  - Critério de pronto: Cria equipe com dados válidos
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar criação de equipe
- [ ] TT-02, Testar listagem de equipes do usuário

## Ordem Sugerida
1. T-01 (listagem) primeiro
2. T-02 (criação) depois

## Lacunas Pendentes (🔴)
- 🔴 Nenhuma
