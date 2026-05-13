# Flowchart — Módulo `webapp/src/store`

> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Fluxo de Card Sorting

```mermaid
flowchart TD
    A[sortCards] --> B{sortOptions.length > 0?}
    B -->|Não| C[Manual sort via cardOrder]
    C --> D[titleOrCreatedOrder fallback]

    B -->|Sim| E[Para cada sortOption:]

    E --> F{propertyId === __title?}
    F -->|Sim| G[titleOrCreatedOrder]

    F -->|Não| H[Busca template no board.cardProperties]
    H --> I{template encontrado?}
    I -->|Não| J[return cards, logError]

    I -->|Sim| K[Switch template.type]

    K -->|number / date| L[Empty no final, Number(a) - Number(b)]
    K -->|createdBy| M[usersById[a.createdBy].username]
    K -->|updatedBy| N[usersById[a.modifiedBy].username]
    K -->|createdTime| O[a.createAt - b.createAt]
    K -->|updatedTime| P[max(updateAt, lastComment) -> subtract]
    K -->|select / multiSelect| Q[lookup option.value pelo ID]
    K -->|multiPerson| R[map IDs → usernames → toString]
    K -->|others| S[aValue.localeCompare(bValue)]

    L --> T{result === 0?}
    M --> T
    N --> T
    O --> T
    P --> T
    Q --> T
    R --> T
    S --> T

    T -->|Sim| U[titleOrCreatedOrder desempate]
    T -->|Não| V[sortOption.reversed ? -result : result]
    U --> V
```

## Fluxo de Card Search/Filter

```mermaid
flowchart TD
    A[searchFilterCards cards, board, searchText] --> B[toLocaleLowerCase]
    B --> C{searchText vazio?}
    C -->|Sim| D[return cards.slice]
    C -->|Não| E[filter cada card:]

    E --> F{title contém searchText?}
    F -->|Sim| G[keep]

    F -->|Não| H[Itera card.fields.properties]
    H --> I{propertyTemplate.type?}
    I -->|select| J[lookup option.value → includes?]
    I -->|multiSelect| K[lookup options → includes?]
    I -->|date| L[pula]
    I -->|others| M[toString → includes?]

    J -->|Sim| G
    K -->|Sim| G
    M -->|Sim| G

    J -->|Não| N[próxima property]
    K -->|Não| N
    M -->|Não| N

    N --> O{mais properties?}
    O -->|Sim| H
    O -->|Não| P[discard]
```

## Fluxo de Board Members Update

```mermaid
flowchart TD
    A[updateMembersHandler state, action] --> B{payload vazio?}
    B -->|Sim| C[return]
    B -->|Não| D[boardId = payload[0].boardId]
    D --> E[boardMembers = membersInBoards[boardId] || {}]

    E --> F[Para cada member:]
    F --> G{!schemeAdmin && !schemeEditor<br/>&& !schemeViewer && !schemeCommenter?}
    G -->|Sim| H[delete boardMembers[member.userId]]
    G -->|Não| I[boardMembers[member.userId] = member]

    I --> J[Verifica myBoardMemberships]
    H --> J
    J --> K{member.userId === myBoardMembership.userId?}
    K -->|Sim, sem permissões| L[delete myBoardMemberships[boardId]]
    K -->|Sim, com permissões| M[myBoardMemberships[boardId] = member]
    K -->|Não| N[próximo]
```

## Fluxo de Inicialização

```mermaid
flowchart TD
    A[initialLoad] --> B[Promise.all: getMe, getMyConfig,<br/>getTeam, getTeams, getBoards,<br/>getMyBoardMemberships, getTeamTemplates,<br/>getBoardsCloudLimits]

    B --> C{me == null?}
    C -->|Sim| D[throw ErrorId.NotLoggedIn]
    C -->|Não| E{team == null?}
    E -->|Sim| F[throw ErrorId.TeamUndefined]
    E -->|Não| G[dispatch fulfilled<br/>team, teams, boards,<br/>boardsMemberships, boardTemplates,<br/>limits, myConfig]

    subgraph Reducers triggered
        G --> H[boards: preenche boards + templates + myBoardMemberships]
        G --> I[cards: seta limitTimestamp]
        G --> J[teams: seta current + allTeams]
        G --> K[limits: seta BoardsCloudLimits]
        G --> L[users: parseia myConfig]
    end
```
