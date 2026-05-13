# User Story: Gerenciar Boards

## História
Como um usuário do Nexo, eu quero criar e gerenciar boards (quadros) para organizar meus projetos e tarefas visualmente.

## Critérios de Aceitação
- Dado um usuário logado, quando ele cria um board, então o board é persistido no servidor e exibido na sidebar
- Dado um board existente, quando o usuário edita o título, descrição ou ícone, então as alterações são salvas via API
- Dado um board privado, quando um usuário sem acesso tenta acessá-lo, então uma tela de erro é exibida com opção de solicitar acesso
- Dado um board, quando o usuário convida um membro, então o membro recebe acesso com o papel (role) especificado

## Rastreabilidade
- `_reversa_sdd/api/quadros/requirements.md`
- `_reversa_sdd/aplicacao/requirements.md`
- `webapp/src/store/boards.ts`

# User Story: Gerenciar Cards

## História
Como um usuário do Nexo, eu quero criar e organizar cards dentro de boards para acompanhar tarefas e ideias.

## Critérios de Aceitação
- Dado um board com propriedades definidas, quando um card é criado, então as propriedades do card são preenchidas com valores padrão
- Dado um card existente, quando o usuário edita suas propriedades, então as alterações são refletidas em tempo real via WebSocket para outros usuários
- Dado um card com conteúdo, quando o usuário adiciona texto, imagem ou checkbox, então o bloco de conteúdo é aninhado como filho do card
- Dado um board com múltiplos cards, quando o usuário filtra por propriedade, então apenas cards correspondentes são exibidos

## Rastreabilidade
- `_reversa_sdd/api/cartoes/requirements.md`
- `_reversa_sdd/blocos/card.ts`
- `webapp/src/store/cards.ts`

# User Story: Visualizar Board

## História
Como um usuário do Nexo, eu quero visualizar boards em diferentes formatos (board, table, gallery, calendar) para escolher a melhor forma de organizar minhas informações.

## Critérios de Aceitação
- Dado um board com cards, quando o usuário alterna para visualização "Table", então os cards são exibidos em formato tabular com colunas por propriedade
- Dado um board com cards, quando o usuário alterna para visualização "Gallery", então os cards são exibidos como cartões de imagem
- Dado um board com cards, quando o usuário agrupa por uma propriedade select, então os cards são organizados em colunas kanban
- Dado um board com visualização salva, quando o usuário retorna ao board, então a última visualização é restaurada

## Rastreabilidade
- `_reversa_sdd/api/quadros/requirements.md`
- `_reversa_sdd/blocos/boardView.ts`
- `webapp/src/store/views.ts`

# User Story: Autenticação

## História
Como um usuário do Nexo, eu quero me autenticar no sistema para acessar meus boards e dados com segurança.

## Critérios de Aceitação
- Dado um usuário não autenticado, quando ele acessa o login, então um formulário de username/senha é exibido
- Dado um usuário com credenciais válidas, quando ele submete o login, então é redirecionado à página anterior ou home
- Dado um usuário não registrado, quando ele acessa o registro com token de signup válido, então uma conta é criada e ele é autenticado automaticamente
- Dado um usuário logado, quando ele altera a senha, então a senha é atualizada no servidor

## Rastreabilidade
- `_reversa_sdd/paginas/loginPage.tsx`
- `_reversa_sdd/auth/requirements.md`
- `server/api/users.go`

# User Story: Importar Dados

## História
Como um usuário do Nexo, eu quero importar dados de ferramentas externas (Trello, Jira, Asana, Notion, Todoist) para migrar meus projetos existentes.

## Critérios de Aceitação
- Dado um arquivo de exportação do Trello, quando o importador é executado, então boards, listas e cards são convertidos para o formato Focalboard
- Dado um arquivo CSV do Notion, quando o importador é executado, então colunas são mapeadas como propriedades select e markdowns como conteúdo de cards
- Dado um arquivo JSON do Todoist, quando o importador é executado, então projetos e seções são convertidos
- Dado um arquivo JSON do Jira ou Asana, quando o importador é executado, então os dados são convertidos para .boardarchive

## Rastreabilidade
- `_reversa_sdd/importadores/trello/`
- `_reversa_sdd/importadores/jira/`
- `_reversa_sdd/importadores/asana/`
- `_reversa_sdd/importadores/notion/`
- `_reversa_sdd/importadores/todoist/`
