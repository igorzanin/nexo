# Autenticação, Tarefas de Implementação

## Tarefas

- [ ] T-01, Implementar JWT create/decode (access + refresh tokens)
  - Fonte legado: `server/auth/auth.go`
  - Critério: Access token 30d, refresh token 60d

- [ ] T-02, Implementar password hashing com bcrypt
  - Fonte legado: `server/services/auth/password.go`
  - Critério: Hash com custo 12; verify funcional

- [ ] T-03, Implementar auth dependency (get_current_user)
  - Fonte legado: `server/api/auth.go:attachSession`
  - Critério: Token inválido → 401; token válido → retorna User

- [ ] T-04, Implementar endpoint POST /api/v1/login
  - Fonte legado: `server/api/auth.go:handleLogin`
  - Critério: Credenciais válidas → JWT; inválidas → 401; rate limited

- [ ] T-05, Implementar endpoint POST /api/v1/register
  - Fonte legado: `server/api/auth.go:handleRegister`
  - Critério: Senha ≥ 8 caracteres; username/email únicos; rate limited

- [ ] T-06, Implementar endpoint POST /api/v1/logout
  - Fonte legado: `server/api/auth.go:handleLogout`

- [ ] T-07, Implementar endpoint POST /api/v1/users/{id}/changepassword
  - Fonte legado: `server/api/auth.go:handleChangePassword`

- [ ] T-08, Implementar read token validation
  - Fonte legado: `server/auth/auth.go:IsValidReadToken`
  - Critério: Compara sharing.token + enabled + EnablePublicSharedBoards

- [ ] T-09, Configurar rate limiting para login (10/min) e register (5/min)
  - Decisão do revisor

## Lacunas
- MFA: não implementado (decisão do revisor)
- Rate limiting: implementado (decisão do revisor)
- Password: 8 caracteres mínimo (decisão do revisor)
