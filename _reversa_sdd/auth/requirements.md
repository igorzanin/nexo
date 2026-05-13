# Autenticação — JWT

Módulo de autenticação baseado em JWT. Responsável por login, registro, troca de senha, validação de tokens JWT e tokens de leitura pública.

## Stack

| Componente | Tecnologia |
|------------|-----------|
| Framework | FastAPI |
| Auth | JWT (python-jose) |
| Password | bcrypt (passlib) |
| Rate limiting | slowapi |

## Responsabilidades
- Emitir JWT access + refresh tokens no login
- Validar tokens JWT em requisições autenticadas
- Registrar novas contas com validação de senha (mínimo 8 caracteres)
- Trocar senha do usuário autenticado
- Validar tokens de leitura para quadros públicos compartilhados
- Rate limiting em endpoints de login/registro

## Regras de Negócio
- JWT expira após `ACCESS_TOKEN_EXPIRE_MINUTES` configurável (padrão 30 dias) 🟢
- Refresh token permite renovar access token sem re-login 🟢
- Token de leitura permite acesso anônimo a quadro público apenas se `ENABLE_PUBLIC_SHARED_BOARDS=true` 🟢
- Senha deve ter no mínimo **8 caracteres** 🟢
- MFA não implementado (descartado por decisão) 🟢
- Rate limiting: máximo N tentativas/minuto para login 🟢

## Rotas

| Método | Caminho | Rate Limit | Descrição |
|--------|---------|-----------|-----------|
| POST | `/api/v1/login` | 10/min | Login com username/email + senha → JWT |
| POST | `/api/v1/logout` | - | Invalida refresh token |
| POST | `/api/v1/register` | 5/min | Registra nova conta |
| POST | `/api/v1/users/{id}/changepassword` | - | Troca senha |

## Rastreabilidade

| Funcionalidade | Fonte legado | Confiança |
|---------------|-------------|-----------|
| Login | `server/api/auth.go:handleLogin` | 🟢 |
| Register | `server/api/auth.go:handleRegister` | 🟢 |
| ChangePassword | `server/api/auth.go:handleChangePassword` | 🟢 |
| JWT validation | `server/auth/auth.go` (adaptado) | 🟢 |
| Read token | `server/auth/auth.go:IsValidReadToken` | 🟢 |
| Rate limiting | Novo (decisão revisor) | 🟢 |
