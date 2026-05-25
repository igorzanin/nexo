# language: pt
# spec-id: PT-003
# rastreabilidade:
#   process_flows: _reversa_sdd/domain.md §"Regras de Card e Block"; _reversa_sdd/domain.md §"Regras de Soft-Delete"
#   target_architecture: BC-Content / BlockService + BlockHistoryService
#   paradigma_alvo: OO com DI (python-jose, SQLAlchemy async, Pinia)
#   br_migrar: BR-MIGRAR-002, BR-MIGRAR-007, BR-MIGRAR-019

Funcionalidade: CRUD de blocos e cards
  Como membro com permissão para gerenciar conteúdo
  Quero criar, inserir em lote, deletar e restaurar cards
  Para manter a integridade do aggregate Block

  @paridade @critico @composicao
  Cenário: Criar card com invariantes obrigatórios
    Dado que o usuário possui PermissionManageBoardCards no board da rota
    Quando o usuário envia um card com boardId da rota, contentOrder válido e properties não-nulo
    Então o sistema cria o card com id, createAt e updateAt maiores que zero
    E o card permanece vinculado ao mesmo board da rota
    E o mesmo contrato observável é mantido com repositório persistente e com dublê de repositório

  @paridade
  Cenário: Batch insert aceita blocos do mesmo board
    Dado que existe um lote com múltiplos blocos apontando para o mesmo board
    Quando o usuário envia o batch insert
    Então o sistema persiste todos os blocos no mesmo board
    E preserva a ordem lógica informada pelo lote

  @paridade
  Cenário: Batch insert com boards diferentes retorna erro
    Dado que existe um lote com blocos apontando para boards diferentes
    Quando o usuário envia o batch insert
    Então o sistema rejeita o lote inteiro
    E nenhum bloco do lote é persistido

  @paridade @critico
  Cenário: Deletar card move o snapshot para histórico
    Dado que existe um card ativo no board
    Quando o usuário autorizado deleta esse card
    Então o card deixa de aparecer entre os blocos ativos
    E um snapshot equivalente é registrado em "blocks_history"
    E o card passa a ter delete_at maior que zero

  @paridade
  Cenário: Restaurar card reidrata o bloco deletado
    Dado que existe um card previamente deletado com snapshot em histórico
    Quando o usuário solicita a restauração do card
    Então o sistema reinsere o card a partir do histórico
    E o card volta ao conjunto ativo com delete_at igual a zero

  @paridade @idempotencia
  Cenário: Deletar card inexistente não é erro
    Dado que o identificador informado não corresponde a um bloco ativo
    Quando o usuário solicita a exclusão desse card
    Então o sistema responde sem erro funcional
    E o estado observável do board permanece inalterado

  @paridade
  Cenário: Título do block respeita o máximo de 16383 runes
    Dado que o usuário está criando ou atualizando um card
    Quando o título informado excede 16383 runes
    Então o sistema rejeita a mutação
    E nenhum bloco inválido é persistido
