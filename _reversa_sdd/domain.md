# Domain Analysis — nexo

> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Glossário de Domínio

| Termo | Definição |
|-------|-----------|
| **Board** | Quadro que organiza cards. Pode ser do tipo Open (`O`) — visível a todos no time — ou Private (`P`) — visível apenas a membros explícitos. Todo board pertence a um Team. |
| **Card** | Unidade atômica de trabalho. Contém properties, conteúdo ordenado (contentOrder), comentários e anexos. Pode ser template. |
| **Block** | Entidade base polimórfica. Boards, Cards, Views, Comments, Text, Images etc. são todos subtipos de Block. |
| **View** | Visualização de um board. 4 tipos: Board (kanban), Table, Gallery, Calendar. Cada view tem filtros, ordenação e cardOrder próprio. |
| **Team** | Agrupamento de usuários. Todo board pertence a um team. |
| **BoardMember** | Associação usuário-board com permissões. Contém scheme flags (Admin/Editor/Commenter/Viewer) e reflete o `minimumRole` do board. |
| **Category** | Pasta na sidebar que agrupa boards. Tipos: `system` (criada pelo sistema) e `custom` (criada pelo usuário). |
| **Property** | Campo customizável no schema de cards de um board. 18 tipos incluindo text, number, select, multiSelect, date, person, checkbox, url, email, phone, createdTime, createdBy, updatedTime, updatedBy. |
| **Subscription** | Inscrição de um usuário em um bloco para notificações. |
| **Sharing** | Compartilhamento público de board via readToken anônimo (link público). |
| **ReadToken** | Token de leitura anônima. Permite acesso de leitura a um board privado sem autenticação. |
| **ContentOrder** | Lista ordenada de IDs de blocos de conteúdo dentro de um card. |
| **Mutator** | Camada que centraliza chamadas à API e atualiza as stores após cada operação, controlando undo/redo via patches. |
| **Onboarding** | Tour guiado de boas-vindas com etapas: Board, Card e ShareBoard. Estado persistido em configuração do usuário. |
| **BoardArchive** | Formato de exportação/importação (.boardarchive) baseado em JSONL/NDJSON. |
| **Workspace** | Container principal da interface que orquestra Sidebar + CenterPanel. |

## Regras de Domínio

### Regras de Board

| # | Regra | Confiança | Fonte |
|---|-------|-----------|-------|
| R1 | Board deve ter um TeamID e um Type (`O`/`P`) válido | 🟢 | Spec `modelo/` |
| R2 | Board Type é imutável após criação, exceto por quem tem PermissionManageBoardType | 🟢 | Spec `api/` |
| R3 | Board MinimumRole válido: `""`, `"viewer"`, `"commenter"`, `"editor"`, `"admin"` | 🟢 | Spec `modelo/` |
| R4 | Board público (Open) requer permissão para criar | 🟢 | Spec `api/` |
| R5 | Board privado (Private) requer permissão para criar | 🟢 | Spec `api/` |
| R6 | Convidados **não** podem criar boards | 🟢 | Spec `aplicacao/` |
| R7 | Boards não-template são automaticamente adicionados à categoria padrão do usuário | 🟢 | Spec `aplicacao/` |
| R8 | Board não pode ser criado com ID pré-definido (servidor gera o ID) | 🟢 | Spec `aplicacao/` |
| R9 | Duplicação de board reverte criação se cópia de arquivos falhar | 🟢 | Spec `aplicacao/` |

### Regras de Card e Block

| # | Regra | Confiança | Fonte |
|---|-------|-----------|-------|
| R10 | Card deve ter ID, BoardID, ContentOrder, Properties não-nulo, CreateAt e UpdateAt > 0 | 🟢 | Spec `modelo/` |
| R11 | Card icon deve ter no máximo 1 grafema | 🟢 | Spec `modelo/` |
| R12 | Todos os blocos em um batch insert devem pertencer ao mesmo board | 🟢 | Spec `aplicacao/` |
| R13 | Block precisa ter BoardID não-vazio | 🟢 | Spec `modelo/` |
| R14 | Block title máximo: 16383 runes | 🟢 | Spec `modelo/` |
| R15 | Block fields JSON máximo: 800000 runes | 🟢 | Spec `modelo/` |
| R16 | Block deve pertencer ao board da rota em toda operação CRUD | 🟢 | Spec `api/` |
| R17 | Deletar bloco inexistente NÃO é erro | 🟢 | Spec `aplicacao/` |
| R18 | Restaurar bloco não-deletado NÃO é erro | 🟢 | Spec `aplicacao/` |
| R19 | ContentOrder de card gerencia ordem dos blocos de conteúdo | 🟢 | Spec `modelo/` |
| R20 | BlocksAndBoards: todo block deve referenciar um board no mesmo lote | 🟢 | Spec `modelo/` |

### Regras de Membro e Permissão

| # | Regra | Confiança | Fonte |
|---|-------|-----------|-------|
| R21 | Último admin de um board não pode ser removido nem ter seu papel rebaixado | 🟢 | Spec `aplicacao/` |
| R22 | Comentários em cards requerem permissão específica | 🟢 | Spec `api/` |
| R23 | Modificar conteúdo/blocos requer permissão específica | 🟢 | Spec `api/` |
| R24 | Alterar board type/minimumRole requer permissão específica | 🟢 | Spec `api/` |
| R25 | BoardMember scheme flags são mutuamente exclusivos | 🟡 | Padrão de uso |
| R26 | Board.minimumRole atua como piso: se board.minimumRole = "editor", todo membro ganha SchemeEditor | 🟢 | Spec `permissions.md` |

### Regras de Categoria

| # | Regra | Confiança | Fonte |
|---|-------|-----------|-------|
| R27 | Categoria deve ter ID, Name, UserID, TeamID não-vazios | 🟢 | Spec `modelo/` |
| R28 | Tipo de categoria: `"system"` ou `"custom"` | 🟢 | Spec `modelo/` |
| R29 | Categoria deletada via soft-delete (deleteAt > 0) | 🟢 | Spec `modelo/` |

### Regras de Subscription

| # | Regra | Confiança | Fonte |
|---|-------|-----------|-------|
| R30 | Subscription requer BlockID, BlockType, SubscriberID e SubscriberType válidos | 🟢 | Spec `modelo/` |
| R31 | SubscriberType deve ser `"user"` | 🟢 | Spec `modelo/` (apenas standalone) |

### Regras de Autenticação

| # | Regra | Confiança | Fonte |
|---|-------|-----------|-------|
| R32 | Autenticação via JWT Bearer token | 🟢 | Spec `auth/` |
| R33 | Token JWT expira após tempo configurável (padrão 30 dias) | 🟢 | Spec `auth/` |
| R34 | Token JWT é renovado automaticamente via refresh token | 🟢 | Spec `auth/` |
| R35 | ReadToken permite acesso público anônimo a board se habilitado | 🟢 | Spec `auth/` |
| R36 | Senha deve ter no mínimo 8 caracteres | 🟢 | Spec `auth/` |
| R37 | Rate limiting implementado para endpoints de login/registro | 🟢 | Spec `auth/` |

### Regras de Soft-Delete

| # | Regra | Confiança | Fonte |
|---|-------|-----------|-------|
| R38 | Todas as entidades usam soft-delete via campo deleteAt (0 = ativo, > 0 = deletado) | 🟢 | Spec `modelo/` |
| R39 | Deletar bloco move para tabela de histórico e depois remove | 🟢 | Spec `aplicacao/` |
| R40 | Restaurar bloco re-insere do histórico com deleteAt=0 | 🟢 | Spec `aplicacao/` |

### Regras de WebSocket

| # | Regra | Confiança | Fonte |
|---|-------|-----------|-------|
| R41 | Cliente WebSocket deve autenticar via AUTH após conectar para operações restritas | 🟢 | Spec `ws/` |
| R42 | Subscribe/Unsubscribe blocks pode ser feito sem autenticação (com readToken válido) | 🟢 | Spec `ws/` |
| R43 | Subscribe/Unsubscribe team requer autenticação | 🟢 | Spec `ws/` |
| R44 | BroadcastBlockChange notifica membros do board + inscritos no bloco | 🟢 | Spec `ws/` |
