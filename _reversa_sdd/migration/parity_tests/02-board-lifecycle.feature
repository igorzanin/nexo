# language: pt
# spec-id: PT-002
# rastreabilidade:
#   process_flows: _reversa_sdd/domain.md §"Regras de Board"; _reversa_sdd/code-analysis.md §"Módulo: webapp/src/store — Redux Store"
#   target_architecture: BC-Boards / BoardService + CategoryService + PermissionService
#   paradigma_alvo: OO com DI (python-jose, SQLAlchemy async, Pinia)
#   br_migrar: BR-MIGRAR-001, BR-MIGRAR-004, BR-MIGRAR-009

Funcionalidade: Ciclo de vida de board
  Como membro autorizado do time
  Quero criar, duplicar e consultar boards
  Para preservar o comportamento central do workspace

  @paridade @critico @composicao
  Cenário: Criar board com ID gerado pelo servidor
    Dado que o usuário possui permissão para criar board no team informado
    E que o payload de criação contém teamId, type e minimumRole válidos sem campo id
    Quando o usuário envia "POST /api/v1/boards"
    Então o sistema persiste o board com ID gerado pelo servidor
    E adiciona automaticamente o board não-template à categoria padrão do usuário
    E o mesmo resultado observável é mantido com persistência real e com dublê de repositório

  @paridade
  Cenário: Rejeitar board com ID pré-definido
    Dado que o usuário possui permissão para criar board
    Quando o payload de criação contém um id pré-definido pelo cliente
    Então o sistema rejeita a criação do board
    E nenhum board novo é persistido

  @paridade
  Cenário: Type do board é imutável sem permissão específica
    Dado que existe um board já criado com type "P"
    E que o usuário não possui PermissionManageBoardType
    Quando o usuário tenta alterar o type do board
    Então o sistema rejeita a alteração
    E o type original permanece inalterado

  @paridade @critico
  Cenário: Duplicar board preserva dados e reverte em falha de arquivo
    Dado que existe um board com blocos e arquivos anexados
    Quando o usuário autorizado solicita a duplicação do board
    Então o sistema cria uma cópia com novo ID gerado pelo servidor
    E replica os blocos e metadados do board original
    E se a cópia de arquivo falhar a duplicação é revertida sem board órfão persistido

  @paridade
  Cenário: Listar boards retorna apenas boards acessíveis
    Dado que existem boards Open e Private no mesmo team
    Quando o usuário consulta a lista de boards disponíveis
    Então o sistema retorna apenas os boards compatíveis com suas permissões
    E os boards retornados preservam título, tipo e pertencimento ao team
