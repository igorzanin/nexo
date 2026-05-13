# ADR-005: Dual permission system

> 🟢 CONFIRMADO — Extraído diretamente do código

## Status

Aceito (implementado)

## Contexto

O modo standalone e o modo plugin Mattermost têm sistemas de permissão fundamentalmente diferentes:

- **Standalone:** sem times/grupos externos, permissões são locais ao board
- **Plugin Mattermost:** herda times, canais e papéis do Mattermost, system admins devem ter acesso universal

## Decisão

Implementar duas implementações da interface `PermissionsService`:

1. **`localpermissions.Service`:**
   - `HasPermissionToTeam` retorna `true` para todos, exceto `PermissionManageTeam`
   - Sem bypass para admins
   - Toda autorização depende exclusivamente do BoardMember + minimumRole

2. **`mmpermissions.Service`:**
   - Requer `PermissionViewTeam` como gate de entrada
   - System admins e team admins bypassam verificações de board
   - Integração com API de permissões do Mattermost

Ambas compartilham a mesma lógica de:
- Validação de inputs
- Elevação de role via `member.MinimumRole`
- Mapeamento permission → scheme flag (tabela idêntica)

## Alternativas consideradas

- **Único sistema com branching condicional**: maior acoplamento e dificuldade de teste
- **Feature flags no runtime**: mais flexível, mas desnecessário — o modo é decidido no build

## Consequências

- Lógica de permissões testável isoladamente em cada implementação
- Código compartilhado (elevação de role, mapeamento) replicado em ambos — passível de divergência
- Interface clara (`PermissionsService`) que permite novas implementações no futuro
- Complexidade de manutenção de duas implementações paralelas
