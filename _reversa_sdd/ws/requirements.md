# WebSocket — Comunicação em Tempo Real

Módulo de comunicação WebSocket bidirecional (FastAPI WebSocket nativo) que mantém conexões persistentes com clientes e propaga mudanças em tempo real. Apenas modo standalone (sem plugin/cluster).

## Responsabilidades
- Handshake e upgrade HTTP → WebSocket (FastAPI nativo)
- Autenticação de conexões via JWT ou read token
- Gerenciamento de inscrições por team e por block
- Broadcast de mudanças (boards, blocks, cards, membros, categorias, config)

## Regras de Negócio
- Conexão não autenticada só permite AUTH, SUBSCRIBE_BLOCKS e UNSUBSCRIBE_BLOCKS 🟢
- SUBSCRIBE_BLOCKS exige readToken válido (compartilhamento público) 🟢
- Ações autenticadas: SUBSCRIBE_TEAM, UNSUBSCRIBE_TEAM e todos os UPDATE_* 🟢
- Broadcast de block change → membros do board + inscritos no bloco 🟢
- Broadcast de board change → membros do board 🟢
- Broadcast de member delete → membros do board (incluindo removido) 🟢
- Broadcast de config change → todos os listeners 🟢
- Apenas modo standalone (plugin adapter removido) 🟢

## Rotas WebSocket

| Path | Descrição |
|------|-----------|
| `/ws` | Conexão WebSocket principal |

## Ações

| Ação | Autenticação | Descrição |
|------|-------------|-----------|
| AUTH | Não | Autentica conexão com JWT |
| SUBSCRIBE_TEAM | Sim | Inscreve em broadcasts do team |
| UNSUBSCRIBE_TEAM | Sim | Remove inscrição do team |
| SUBSCRIBE_BLOCKS | Não (com readToken) | Inscreve em broadcasts de blocks |
| UNSUBSCRIBE_BLOCKS | Não (com readToken) | Remove inscrição de blocks |
| UPDATE_BOARD | Sim | Broadcast de board alterado |
| UPDATE_BLOCK | Sim | Broadcast de block alterado |
| UPDATE_MEMBER | Sim | Broadcast de member alterado |
| UPDATE_CATEGORY | Sim | Broadcast de categoria alterada |
| UPDATE_CLIENT_CONFIG | Sim | Broadcast de config alterada |

## Broadcast Methods (mantidos do legado)

| Método | Gatilho | Público |
|--------|---------|---------|
| `broadcast_block_change` | Bloco criado/alterado | Membros do board + inscritos |
| `broadcast_block_delete` | Bloco removido | Mesmo que BlockChange |
| `broadcast_board_change` | Board alterado | Membros do board |
| `broadcast_board_delete` | Board removido | Membros do board |
| `broadcast_member_change` | Membro adicionado/alterado | Membros do board |
| `broadcast_member_delete` | Membro removido | Membros do board (incluindo removido) |
| `broadcast_config_change` | Config alterada | Todos os listeners |
| `broadcast_category_change` | Categoria alterada | Usuário específico |

## Rastreabilidade

| Componente | Fonte legado | Confiança |
|-----------|-------------|-----------|
| WebSocket server | `server/ws/server.go` | 🟢 |
| Mensagens | `server/ws/common.go` | 🟢 |
| Broadcast methods | `server/ws/server.go` | 🟢 |

## Dependências
- FastAPI WebSocket (nativo, sem dependência extra)
- `nexo/auth/` — validação JWT
- `nexo/repositories/` — acesso a dados
