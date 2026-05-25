# language: pt
# spec-id: PT-004
# rastreabilidade:
#   process_flows: _reversa_sdd/domain.md §"Regras de Membro e Permissão"; _reversa_sdd/migration/target_business_rules.md §"BR-MIGRAR-009"
#   target_architecture: BC-Boards / PermissionService + BoardService + BoardPermissionGate.vue
#   paradigma_alvo: OO com DI (python-jose, SQLAlchemy async, Pinia)
#   br_migrar: BR-MIGRAR-003, BR-MIGRAR-009, BR-MIGRAR-025

Funcionalidade: Permissões e membros
  Como administrador ou membro de board
  Quero que as permissões respeitem a hierarquia e as restrições do legado
  Para impedir ações indevidas e proteger o workspace

  @paridade @critico @composicao
  Cenário: Último admin não pode ser removido nem rebaixado
    Dado que existe apenas um membro com papel Admin no board
    Quando outro fluxo tenta remover esse membro ou rebaixá-lo para papel inferior
    Então o sistema rejeita a operação
    E o board continua com pelo menos um Admin
    E o mesmo contrato observável é mantido com repositório persistente e com dublê de repositório

  @paridade
  Cenário: MinimumRole atua como piso de permissão
    Dado que o board possui minimumRole igual a "editor"
    Quando um membro com papel inferior acessa o board
    Então o sistema concede no mínimo as permissões equivalentes a Editor nesse board
    E o membro continua impedido apenas das ações exclusivas de Admin

  @paridade
  Cenário: Editor não pode gerenciar roles do board
    Dado que o usuário possui papel Editor nesse board
    Quando ele tenta alterar o papel de outro membro
    Então o sistema rejeita a alteração de roles
    E a matriz de permissões do board permanece inalterada

  @paridade
  Cenário: Viewer não pode comentar em cards
    Dado que o usuário possui apenas permissão de Viewer no board
    Quando ele tenta adicionar um comentário em um card
    Então o sistema rejeita a operação de comentário
    E o card permanece sem novo comentário persistido

  @paridade
  Cenário: Board Open cria membro sintético para leitura
    Dado que existe um board do tipo Open no team
    E que o usuário possui acesso ao team sem membership explícita no board
    Quando o usuário acessa o board
    Então o sistema resolve um BoardMember sintético para leitura
    E a permissão view_board é concedida sem criar papel administrativo implícito
