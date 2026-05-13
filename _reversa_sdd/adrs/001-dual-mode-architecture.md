# ADR-001: Standalone-only architecture (Mattermost plugin removido)

> 🟢 CONFIRMADO — Decisão do revisor

## Status

Substituído. Decisão original (dual-mode) foi revertida: o Nexo opera **apenas em modo standalone**.

## Histórico

- **Original (legado):** Dual-mode: standalone + plugin Mattermost
- **2026-05-13:** Revisor decidiu remover o modo plugin. Apenas standalone.

## Contexto

O Nexo é um fork do Focalboard (Mattermost). O Focalboard era originalmente um plugin do Mattermost com capacidade standalone. Para simplificar a arquitetura e remover a dependência do ecossistema Mattermost, o modo plugin foi removido.

## Decisão

- Modo **standalone** é o único modo de operação
- Plugin Mattermost, PluginAdapter, mmpermissions, mattermostauthlayer: **removidos**
- Clustering via cluster events: **removido**
- Apenas 1 modo de autenticação: **JWT** (em vez de 3 modos: standalone, plugin, single-user)
- Desktop: **Electron** (em vez de 3 apps nativos: macOS Swift, Windows WPF, Linux Go)

## Consequências

### Positivas
- Código significativamente reduzido (removido ~1800 referências a Mattermost)
- Arquitetura mais simples: 1 modo de operação, 1 modo de auth
- Menos dependências externas (sem mattermost/server SDK)
- Desktop unificado (Electron cross-platform vs 3 apps nativos)

### Negativas
- Perde integração nativa com Mattermost (channel sync, notificações)
- Perde clusterização via Mattermost
- Usuários do ecossistema Mattermost precisam de adaptação
