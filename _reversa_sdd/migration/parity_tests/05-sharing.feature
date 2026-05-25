# language: pt
# spec-id: PT-005
# rastreabilidade:
#   process_flows: _reversa_sdd/domain.md §"Regras de Autenticação"; _reversa_sdd/code-analysis.md §"IsValidReadToken"
#   target_architecture: BC-Collaboration / SharingService + sharing router
#   paradigma_alvo: OO com DI (python-jose, SQLAlchemy async, Pinia)
#   br_migrar: BR-MIGRAR-006, BR-MIGRAR-013

Funcionalidade: Compartilhamento público de board
  Como administrador de board
  Quero compartilhar boards por readToken
  Para permitir acesso anônimo controlado

  @paridade @critico @composicao
  Cenário: Compartilhar board gera readToken válido
    Dado que o feature flag "enablePublicSharedBoards" está habilitado
    E que o usuário possui permissão para compartilhar o board
    Quando o usuário habilita o compartilhamento público do board
    Então o sistema gera um readToken único associado ao board
    E expõe uma URL pública de leitura baseada nesse token
    E o mesmo contrato observável é mantido com repositório persistente e com dublê de repositório

  @paridade @critico
  Cenário: Acesso anônimo com readToken válido
    Dado que existe um board compartilhado publicamente com readToken ativo
    Quando um usuário anônimo acessa o board com esse readToken
    Então o sistema permite acesso somente leitura ao board
    E as ações que exigem autenticação continuam indisponíveis

  @paridade
  Cenário: Acesso é negado sem readToken
    Dado que existe um board compartilhado publicamente
    Quando um usuário anônimo tenta acessar o board sem informar readToken válido
    Então o sistema nega o acesso ao conteúdo do board
    E nenhum membership autenticado é criado implicitamente

  @paridade @idempotencia
  Cenário: Revogar readToken remove o acesso público
    Dado que um board possui readToken público ativo
    Quando o administrador revoga o compartilhamento público
    Então o readToken deixa de autorizar novos acessos anônimos
    E uma segunda revogação não recria o token nem reabre o acesso
