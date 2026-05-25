# language: pt
# spec-id: PT-006
# rastreabilidade:
#   process_flows: _reversa_sdd/domain.md §"Regras de WebSocket"; _reversa_sdd/code-analysis.md §"Módulo: server/ws — WebSocket"
#   target_architecture: BC-Collaboration / WSConnectionManager + shared\ws\useWebSocket.ts
#   paradigma_alvo: OO com DI (python-jose, SQLAlchemy async, Pinia)
#   br_migrar: BR-MIGRAR-008, BR-MIGRAR-022

Funcionalidade: WebSocket em tempo real
  Como usuário autenticado ou leitor público autorizado
  Quero receber atualizações em tempo real compatíveis com o legado
  Para manter o board sincronizado

  @paridade @critico @composicao
  Cenário: Autenticação ocorre após conectar
    Dado que o cliente abriu uma conexão em "/ws/{teamId}"
    Quando o cliente envia a ação "AUTH" com credencial válida
    Então a sessão WebSocket passa a aceitar operações restritas daquele usuário
    E o mesmo contrato observável é mantido quando a autenticação usa dependência real ou dublê equivalente do módulo de auth

  @paridade
  Cenário: Subscribe em bloco com readToken válido não exige auth prévia
    Dado que existe um board público com readToken válido
    Quando o cliente envia "SUBSCRIBE_BLOCKS" para um bloco desse board usando o readToken
    Então o servidor aceita a inscrição no bloco sem exigir "AUTH"
    E a sessão permanece limitada ao escopo de leitura permitido pelo token

  @paridade
  Cenário: Subscribe em team requer autenticação
    Dado que o cliente abriu a conexão WebSocket sem autenticar
    Quando o cliente envia "SUBSCRIBE_TEAM" para um team privado
    Então o servidor rejeita a inscrição no team
    E a conexão só passa a aceitar esse subscribe após "AUTH" válido

  @paridade @critico
  Cenário: Broadcast após modificação de bloco notifica membros e inscritos
    Dado que existem membros do board conectados e usuários inscritos no bloco alterado
    Quando uma modificação de bloco é confirmada pelo sistema
    Então o servidor emite a atualização correspondente para membros do board e inscritos no bloco
    E clientes não autorizados fora dessa audiência não recebem a mensagem
