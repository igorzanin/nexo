# language: pt
# spec-id: PT-008
# rastreabilidade:
#   process_flows: _reversa_sdd/migration/target_screens.md §"SCR-001, SCR-004, SCR-005, SCR-006, SCR-009"; _reversa_sdd/code-analysis.md §"Módulo: webapp/src/pages — Páginas da Aplicação"
#   target_architecture: BC-Identity / Identity Feature; BC-Views / Views Feature; BC-Content / Content Feature; BC-Collaboration / Collaboration Feature
#   paradigma_alvo: OO com DI (python-jose, SQLAlchemy async, Pinia)
#   br_migrar: BR-MIGRAR-006, BR-MIGRAR-010, BR-MIGRAR-012, BR-MIGRAR-013, BR-MIGRAR-018

Funcionalidade: Contratos de tela em modo modernizado
  Como usuário do sistema
  Quero que as telas críticas preservem hierarquia, estados, textos e transições
  Para manter equivalência comportamental sem exigir paridade visual literal

  @paridade @critico @composicao
  Cenário: LoginPage (SCR-001) respeita hierarquia, estados e navegação
    Dado que a rota "/login" renderiza a hierarquia AuthLayout > Card > Form conforme a spec
    Quando a tela percorre os estados idle, loading, error e success
    Então os textos literais "Nexo", "Username", "Password", "Log in" e "create an account" permanecem corretos
    E a transição de sucesso navega para "HomePage" e o link secundário navega para "/register"
    E o mesmo contrato visual-semântico é mantido com Pinia store real ou dublê de store equivalente

  @paridade @critico
  Cenário: BoardTableView (SCR-004) preserva toolbar, estados e ausência de item removido
    Dado que a rota "/boards/:boardId/table" renderiza Sidebar, BoardPermissionGate e tabela responsiva
    Quando a tela percorre os estados idle, loading, error e success
    Então os textos literais "Properties", "Filter", "Sort", "Search cards", "New ▾" e "Share" permanecem corretos
    E clicar em um card abre "CardDetailModal" e a ação "Share" abre "ShareBoardModal"
    E o link externo "Give feedback" não é esperado por ser uma deviation aprovada

  @paridade @critico
  Cenário: BoardKanbanView (SCR-005) preserva colunas, estados e transições
    Dado que a rota "/boards/:boardId/kanban" renderiza Sidebar, BoardPermissionGate e colunas repetidas do kanban
    Quando a tela percorre os estados idle, loading, error e success
    Então os textos literais "Properties", "Filter", "Sort", "Search cards", "New ▾" e "Share" permanecem corretos
    E clicar em um card abre "CardDetailModal" e o botão "+" permanece disponível por coluna
    E o link externo "Give feedback" não é esperado por ser uma deviation aprovada

  @paridade
  Cenário: CardDetailModal (SCR-006) preserva estrutura interna e estados
    Dado que a abertura do card renderiza Modal > ModalBody > ContentRegistry > painel de propriedades
    Quando a tela percorre os estados idle, loading, error e success
    Então os textos literais "Comments", "Add a comment", "Properties", "Status", "Sprint", "Prioridade" e "Assignee" permanecem corretos
    E fechar o modal retorna para a tela de board sem perder o contexto do card atual

  @paridade
  Cenário: ShareBoardModal (SCR-009) preserva campos e atualização semântica
    Dado que a abertura de compartilhamento renderiza Modal com busca, toggle, link e tabela de membros
    Quando a tela percorre os estados idle, loading, error e success
    Então os textos literais "Share Board", "Search for people", "Allow sharing" e "Copy link" permanecem corretos
    E fechar o modal retorna para o board sem alterar a navegação principal
