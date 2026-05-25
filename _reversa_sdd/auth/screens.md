# screens — auth

> Spec de interface das telas pertencentes à unit `auth` (`server/auth`).
> Gerado por: reversa-visor — 2026-05-24

---

## Tela 1 — Login Page

**Screenshot:** `screenshots/login-page.png`
**Propósito:** Autenticar o usuário para acesso ao Focalboard.
**Estado:** Formulário vazio (campos em branco).
**Contexto de uso:** Ponto de entrada quando o usuário não está autenticado ou após logout.

### Layout

- Fundo branco simples, sem sidebar.
- Card centralizado (horizontal e verticalmente) com bordas arredondadas e sombra sutil.

### Formulário

| Campo | Tipo | Placeholder | Obrigatório |
|---|---|---|---|
| Username | Text input | "Enter username" | Sim |
| Password | Password input | "Enter password" | Sim |

### Ações

| Elemento | Tipo | Comportamento |
|---|---|---|
| Log in | Botão primário (azul, largura total) | Submete o formulário com username + password |
| "or create an account if you don't have one" | Link (azul, centralizado) | Navega para tela de registro/criação de conta |

### Estados não capturados (inferidos)

| Estado | Descrição |
|---|---|
| Erro de credenciais | Exibe mensagem de erro (ex: "Invalid username or password") |
| Campo obrigatório vazio | Possível validação inline nos campos |
| Loading | Botão pode exibir spinner durante a requisição |

### Fluxo de saída

- **Sucesso:** redireciona para Home (lista de boards) ou último board acessado.
- **"Create account":** redireciona para tela de registro (não capturada).
