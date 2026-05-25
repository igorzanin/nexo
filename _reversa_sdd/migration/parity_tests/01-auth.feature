# language: pt
# spec-id: PT-001
# rastreabilidade:
#   process_flows: _reversa_sdd/domain.md §"Regras de Autenticação"; _reversa_sdd/code-analysis.md §"Módulo: server/auth — Autenticação"
#   target_architecture: BC-Identity / Auth Module + SessionService
#   paradigma_alvo: OO com DI (python-jose, SQLAlchemy async, Pinia)
#   br_migrar: BR-MIGRAR-006, BR-MIGRAR-021

Funcionalidade: Fluxo de autenticação
  Como usuário registrado
  Quero autenticar, renovar e encerrar minha sessão
  Para acessar o sistema com o mesmo comportamento funcional do legado

  @paridade @critico @composicao
  Cenário: Login com credenciais válidas
    Dado que existe um usuário ativo com senha validada por bcrypt
    E que o limite de tentativas por IP não foi excedido
    Quando o usuário envia username e password válidos para "POST /api/v1/login"
    Então o sistema retorna um access_token Bearer com expiração de 30 dias
    E retorna um refresh_token com expiração de 60 dias
    E a sessão autenticada permite navegação para "/boards"
    E o mesmo contrato observável permanece válido com repositório SQLAlchemy async e com dublê de repositório equivalente

  @paridade
  Cenário: Login com senha errada
    Dado que existe um usuário ativo cadastrado
    Quando o usuário envia username válido e password incorreta para "POST /api/v1/login"
    Então o sistema rejeita a autenticação sem criar nova sessão
    E retorna erro de credencial inválida sem expor detalhes internos do hash

  @paridade
  Cenário: Refresh token renova a sessão
    Dado que o usuário possui um refresh_token válido e um access_token expirado
    Quando o usuário envia o refresh_token para "POST /api/v1/auth/refresh"
    Então o sistema emite um novo access_token para o mesmo usuário
    E mantém o refresh_token dentro da janela válida de 60 dias
    E o contrato de autorização para rotas protegidas volta a ser aceito

  @paridade
  Cenário: Logout invalida a sessão atual
    Dado que o usuário está autenticado com um access_token válido
    Quando o usuário executa "POST /api/v1/logout"
    Então a sessão atual deixa de autorizar chamadas protegidas
    E uma nova tentativa com o token invalidado é rejeitada

  @paridade
  Cenário: Rate limiting de login bloqueia excesso de tentativas
    Dado que o mesmo IP já realizou 10 tentativas de login no último minuto
    Quando esse IP envia uma décima primeira tentativa para "POST /api/v1/login"
    Então o sistema responde com bloqueio por rate limiting
    E nenhuma nova sessão é criada
    E o contrato permanece compatível com a política de 10 requisições por minuto
