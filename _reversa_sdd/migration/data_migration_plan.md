---
schemaVersion: 1
generatedAt: 2026-05-24T17:45:00-03:00
reversa:
  version: "1.0.0"
kind: data_migration_plan
producedBy: designer
hash: "sha256:designer-data_migration_plan-nexo"
---

# Data Migration Plan

## Contexto

> IMPORTANTE: Este sistema não está em produção. Não há dados de usuário reais a migrar.
> Este plano cobre exclusivamente migração de dados de desenvolvimento (seeds, dados de teste, board templates).

A reescrita do nexo/Focalboard usa a mesma família conceitual de tabelas do legado (`boards`, `blocks`, `users`, etc.), então a migração de dados é **predominantemente 1-para-1** em nomes e significado.
As diferenças relevantes estão na formalização do schema via SQLAlchemy/Alembic, no uso consistente de IDs `TEXT` (UUIDv4 gerados em Python) e na normalização explícita de constraints e defaults.
Como a estratégia aprovada é **Big Bang Controlado** e não há produção ativa, o objetivo não é executar CDC ou dual-write, e sim preparar um schema limpo, reprodutível e seeds confiáveis para dev/test/desktop.
Os importadores CLI continuam fora deste plano: eles alimentam `.boardarchive` e não migram banco legado diretamente.

## Mapeamento Legado → Novo

| Tabela original | Tabela nova | Tipo de transformação |
|---|---|---|
| `users` | `users` | 1-para-1 com constraints formais |
| `sessions` | `sessions` | 1-para-1 com limpeza periódica explícita |
| `preferences` | `preferences` | 1-para-1 |
| `teams` | `teams` | 1-para-1 |
| `team_members` | `team_members` | 1-para-1 com semântica guest desativada |
| `boards` | `boards` | 1-para-1 com checks de `type` e `minimum_role` |
| `board_members` | `board_members` | 1-para-1 com exclusividade de role formalizada |
| `blocks` | `blocks` | 1-para-1; polimorfismo preservado |
| `blocks_history` | `blocks_history` | 1-para-1 |
| `categories` | `categories` | 1-para-1 |
| `category_boards` | `category_boards` | 1-para-1 com unicidade explícita |
| `subscriptions` | `subscriptions` | 1-para-1 |
| `notification_hints` | `notification_hints` | 1-para-1 |
| `sharing` | `sharing` | 1-para-1; `id` tratado como board compartilhado |
| `file_info` | `file_info` | 1-para-1 |

## Transformações por Tabela

### `users`
- **Colunas**: manter `id`, `username`, `email`, `password_hash`, `is_bot`, `props`, `create_at`, `update_at`, `delete_at`.
- **Tratamento de nulos**: `username`, `email`, `password_hash`, `create_at`, `update_at` não podem ser nulos; seeds devem preencher todos.
- **Defaults**: `is_bot = false`, `delete_at = 0`.
- **Adaptação**: timestamps continuam em Unix ms (`BIGINT`); IDs permanecem `TEXT`, preferencialmente UUIDv4 no novo sistema.

### `sessions`
- **Colunas**: manter `id`, `token`, `user_id`, `create_at`, `last_active_time`, `expire_at`.
- **Tratamento de nulos**: `token`, `user_id`, `create_at`, `expire_at` obrigatórios.
- **Defaults**: nenhum default funcional além do gerador de datas na aplicação.
- **Adaptação**: sessões expiradas não são migradas para seeds; o novo sistema recria sessões conforme login e roda cleanup via `lifespan`.

### `preferences`
- **Colunas**: manter `user_id`, `category`, `name`, `value`.
- **Tratamento de nulos**: `category` e `name` obrigatórios.
- **Defaults**: onboarding usa `value = "false"` ou estado equivalente por etapa.
- **Adaptação**: persistir estado do onboarding em chaves explícitas, por exemplo `category = 'onboarding'` e `name = 'board'|'card'|'share_board'`.

### `teams`
- **Colunas**: manter `id`, `display_name`, `type`, `description`, `create_at`, `update_at`, `delete_at`.
- **Tratamento de nulos**: `display_name`, `create_at`, `update_at` obrigatórios.
- **Defaults**: `type = 'O'`, `delete_at = 0`.
- **Adaptação**: seeds criam um time padrão `default` para sustentar boards iniciais.

### `team_members`
- **Colunas**: manter estrutura atual.
- **Tratamento de nulos**: `team_id`, `user_id`, `create_at`, `update_at` obrigatórios.
- **Defaults**: `scheme_user = true`, `scheme_guest = false`, `scheme_admin = false`, `delete_at = 0`.
- **Adaptação**: no novo sistema, não criar membros `guest`; dados de desenvolvimento usam apenas `scheme_user` e opcionalmente `scheme_admin`.

### `boards`
- **Colunas**: manter estrutura atual.
- **Tratamento de nulos**: `id`, `team_id`, `type`, `create_at`, `update_at` obrigatórios.
- **Defaults**: `type = 'P'`, `minimum_role = ''`, `template_version = 0`, `delete_at = 0`.
- **Adaptação**:
  - `type` deve ser `O` ou `P`.
  - `minimum_role` deve ser um dos valores válidos.
  - `card_properties` recebe JSON seed para templates (Kanban, Todo, Meeting Notes).
  - IDs novos devem ser gerados pelo servidor Python, não reaproveitados manualmente em fixtures futuras.

### `board_members`
- **Colunas**: manter estrutura atual.
- **Tratamento de nulos**: `board_id`, `user_id`, `create_at`, `update_at` obrigatórios.
- **Defaults**: `scheme_viewer = true`, `delete_at = 0`.
- **Adaptação**: em seeds, garantir ao menos um admin por board e nunca produzir board sem admin.

### `blocks`
- **Colunas**: manter estrutura atual.
- **Tratamento de nulos**: `id`, `type`, `create_at`, `update_at`, `board_id` obrigatórios.
- **Defaults**: `schema = 1`, `delete_at = 0`.
- **Adaptação**:
  - manter `fields` como JSON compatível com SQLAlchemy.
  - `title` e `fields` devem respeitar os limites definidos no domínio.
  - views, comments e cards continuam na mesma tabela, diferenciados por `type`.

### `blocks_history`
- **Colunas**: manter estrutura atual.
- **Tratamento de nulos**: `id`, `type`, `create_at`, `update_at`, `delete_at`, `board_id`, `insert_at` obrigatórios.
- **Defaults**: nenhum.
- **Adaptação**: não seedar histórico desnecessário; usar apenas em testes específicos de archive/restore.

### `categories`
- **Colunas**: manter estrutura atual.
- **Tratamento de nulos**: `id`, `name`, `user_id`, `team_id`, `create_at`, `update_at` obrigatórios.
- **Defaults**: `sort_order = 0`, `type = 'custom'`, `delete_at = 0`.
- **Adaptação**: criar categoria default `My Boards` como `system` para o usuário admin seed.

### `category_boards`
- **Colunas**: manter estrutura atual.
- **Tratamento de nulos**: `id`, `user_id`, `team_id`, `category_id`, `board_id`, `create_at`, `update_at` obrigatórios.
- **Defaults**: `sort_order = 0`, `hide = false`, `delete_at = 0`.
- **Adaptação**: popular vínculos entre a categoria default e os board templates visíveis no ambiente de desenvolvimento.

### `subscriptions`
- **Colunas**: manter estrutura atual.
- **Tratamento de nulos**: `block_type`, `block_id`, `subscriber_type`, `subscriber_id`, `create_at` obrigatórios.
- **Defaults**: `publish_at = 0`.
- **Adaptação**: `subscriber_type` é sempre `user`; qualquer valor diferente deve ser rejeitado na carga.

### `notification_hints`
- **Colunas**: manter estrutura atual.
- **Tratamento de nulos**: `block_type`, `block_id`, `create_at` obrigatórios.
- **Defaults**: `modify_at = 0`.
- **Adaptação**: pode iniciar vazio em seeds; é tabela operacional, não estrutural.

### `sharing`
- **Colunas**: manter `id`, `enabled`, `token`, `modified_by`, `update_at`, `create_at`.
- **Tratamento de nulos**: `id`, `token`, `update_at`, `create_at` obrigatórios.
- **Defaults**: `enabled = false`.
- **Adaptação**: `id` representa o board compartilhado; seeds podem iniciar com todos `enabled = false` e um caso de teste com `enabled = true`.

### `file_info`
- **Colunas**: manter estrutura atual.
- **Tratamento de nulos**: `id`, `create_at`, `update_at` obrigatórios; demais campos podem ser nulos em testes mínimos.
- **Defaults**: `has_preview_image = false`, `delete_at = 0`.
- **Adaptação**: para ambiente dev, usar anexos pequenos locais; não migrar artefatos grandes do legado.

## Dados de Desenvolvimento (Seeds)

### Sequência recomendada
1. **Usuário admin seed**
   - `users`: criar `admin@nexo.local` / `admin` com senha bcrypt válida.
   - `preferences`: criar chaves de onboarding em estado inicial.
2. **Time padrão**
   - `teams`: criar time `default` (`type = 'O'`).
   - `team_members`: associar o admin como `scheme_admin = true`.
3. **Categoria default**
   - `categories`: criar `My Boards` como `system` para o usuário admin.
4. **Board templates**
   - `boards`: criar 3 templates base:
     - `Kanban Template`
     - `Todo Template`
     - `Meeting Notes Template`
   - `board_members`: admin como Admin em todos os templates.
   - `category_boards`: vincular os templates à categoria default.
5. **Conteúdo mínimo por template**
   - `blocks`: inserir ao menos uma view por board template (`kanban`, `table`, `gallery/calendar` conforme aplicável), cards de exemplo e estrutura básica de conteúdo.
6. **Sharing e subscriptions de teste**
   - `sharing`: um template ou board de teste com `enabled = true` e readToken previsível apenas em ambiente dev.
   - `subscriptions`: opcionalmente uma assinatura do admin em um card de exemplo.
7. **File fixtures**
   - `file_info`: anexos pequenos para fluxo de upload/download.

### Regras de seed
- Todos os timestamps em milissegundos Unix (`BIGINT`).
- Todos os IDs em `TEXT`; preferir UUIDv4 gerado por script Python seed.
- Não seedar sessões persistentes: login deve gerar sessões reais durante testes.
- Não seedar dados Mattermost, MFA, cloud limits ou roles guest, pois foram descartados.

## Estratégia de Schema (Alembic)

1. **Migration inicial única**
   - Criar uma revisão Alembic inicial baseada em `Base.metadata` com todas as tabelas do `target_data_model.md`.
   - A migration inicial deve incluir constraints, índices e FKs já definitivos, evitando migrations vazias intermediárias.
2. **Configuração do Alembic**
   - `env.py` aponta para a `Base.metadata` SQLAlchemy do backend FastAPI.
   - O mesmo conjunto de models deve funcionar em PostgreSQL e SQLite, sem forks de schema.
3. **Bootstrap do banco**
   - Desenvolvimento: `alembic upgrade head` seguido por script de seed.
   - Testes: banco limpo por suíte + seed mínima sob demanda.
   - Desktop: SQLite local inicializado via a mesma migration inicial.
4. **Evolução futura**
   - mudanças pós-MVP entram como novas revisões incrementais;
   - nenhuma migration de coexistência legado/novo é necessária, pois não há produção ativa.

## Validação Pós-Migração

### Checklist de integridade
- [ ] `users`: contagem esperada = 1 admin seed (ou contagem da fixture atual).
- [ ] `teams`: existe exatamente 1 time `default` em ambiente seed mínimo.
- [ ] `team_members`: todo `team_id` referencia time existente; todo `user_id` referencia usuário existente.
- [ ] `boards`: todos os registros têm `team_id`, `type` válido e `minimum_role` válido.
- [ ] `board_members`: cada board ativo possui pelo menos 1 admin ativo.
- [ ] `categories`: toda categoria ativa tem `user_id` e `team_id` válidos.
- [ ] `category_boards`: não existem vínculos órfãos de category ou board.
- [ ] `blocks`: todo bloco ativo referencia board existente.
- [ ] `blocks_history`: toda linha tem `delete_at > 0` e `insert_at` preenchido.
- [ ] `subscriptions`: `subscriber_type = 'user'` em 100% das linhas.
- [ ] `sharing`: `token` é único; quando `enabled = true`, o board correspondente existe.
- [ ] `preferences`: onboarding possui as 3 chaves esperadas no admin seed.
- [ ] índices principais foram criados sem erro.

### Validação funcional mínima
- [ ] login do admin seed funciona.
- [ ] `/metrics` responde 200.
- [ ] abrir board template Kanban funciona.
- [ ] compartilhamento público com readToken válido funciona.
- [ ] delete + restore de block persiste corretamente entre `blocks` e `blocks_history`.
- [ ] import de `.boardarchive` de exemplo cria board utilizável.

## Cutover de Dados (Sequência)

### Situação atual
Não aplicável no momento, porque **não há dados reais de produção para cortar**.

### Sequência atual para desenvolvimento
1. Executar `alembic upgrade head` no banco alvo.
2. Rodar script de seed Python para usuário admin, time default, categoria default e 3 templates.
3. Rodar fixtures opcionais de conteúdo, sharing e anexos.
4. Executar testes de integração essenciais (`auth`, `sharing`, `boards`, `blocks`).
5. Validar UI e modo desktop sobre o banco recém-populado.

### Sequência futura quando houver dados reais
1. Congelar escrita no sistema de origem.
2. Exportar dados em ordem de dependência: `users` → `teams` → `team_members` → `boards` → `board_members` → `categories` → `category_boards` → `blocks` → `blocks_history` → `sharing` → `subscriptions` → `notification_hints` → `file_info` → `preferences`.
3. Aplicar validações de constraints e contagens após cada lote.
4. Reexecutar import de forma idempotente se um lote falhar.
5. Liberar escrita apenas após checklist funcional completo.

## Notas
- Como os nomes de tabela do legado já coincidem com o alvo, a maior parte do esforço não é transformação, e sim **garantia de qualidade dos seeds e da migration inicial**.
- Importadores CLI TypeScript não substituem este plano; eles continuam sendo porta de entrada para dados de terceiros, não mecanismo de bootstrapping do banco principal.
- Se no futuro surgir banco legado mal documentado adicional, registrar a lacuna no ciclo de coding antes de qualquer migração real.
