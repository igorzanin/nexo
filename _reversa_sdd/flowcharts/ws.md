# Flowchart — Módulo `server/ws`

> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Fluxo de Conexão WebSocket

```mermaid
flowchart TD
    A[HTTP Upgrade Request] --> B{Upgrade OK?}
    B -->|Sim| C[Cria websocketSession vazia<br/>userID='', teams=[], blocks=[]]
    B -->|Não| D[Log ERROR + return]
    
    C --> E{isMattermostAuth?}
    E -->|Sim| F[Seta userID = Header<br/>Mattermost-User-Id]
    E -->|Não| G[userID permanece vazio]
    
    F --> H[addListener → registra no<br/>mapa listeners]
    G --> H
    
    H --> I[defer: removeListener + conn.Close]
    I --> J[Mensagem loop]
    
    J --> K[ReadMessage]
    K --> L{Erro?}
    L -->|Sim| M[removeListener + break]
    L -->|Não| N[Unmarshal JSON]
    
    N --> O{Unmarshal erro?}
    O -->|Sim| P[Log ERROR JSON + continue]
    O -->|Não| Q{Ação == AUTH?}
    
    Q -->|Sim| R[authenticateListener]
    R --> J
    
    Q -->|Não| S{Ação == SUBSCRIBE_BLOCKS<br/>ou UNSUBSCRIBE_BLOCKS?}
    S -->|Sim| T{readToken válido?}
    T -->|Sim| U[subscribe/unsubscribe blocks]
    T -->|Não| V[Log ERROR + continue]
    U --> J
    V --> J
    
    S -->|Não| W{isAuthenticated?}
    W -->|Não| X[Log ERROR + continue]
    
    W -->|Sim| Y[Switch action]
    
    Y --> ZA[SUBSCRIBE_TEAM]
    Y --> ZB[UNSUBSCRIBE_TEAM]
    Y --> ZC[default: ERROR]
    
    ZA --> ZA1{SingleUser?}
    ZA1 -->|Sim, userID==SingleUser| ZA2[subscribeListenerToTeam]
    ZA1 -->|Sim, userID!=SingleUser| ZA3[continue]
    ZA1 -->|Não| ZA4{DoesUserHaveTeamAccess?}
    ZA4 -->|Sim| ZA2
    ZA4 -->|Não| ZA5[Log ERROR + continue]
    ZA2 --> J
    
    ZB --> ZB1[unsubscribeListenerFromTeam]
    ZB1 --> J
    ZC --> J
```

## Fluxo de Broadcast (Standalone Server)

```mermaid
flowchart TD
    A[BroadcastBlockChange] --> B[Cria UpdateBlockMsg]
    B --> C[getListenersForTeamAndBoard]
    C --> D[Mais getListenersForBlock<br/>para block.ID e block.ParentID]
    D --> E[Deduplica listeners]
    E --> F[Para cada listener:]
    F --> G{WriteJSON OK?}
    G -->|Sim| H[Próximo listener]
    G -->|Não| I[conn.Close]
    H --> F
```

## Fluxo de Broadcast (PluginAdapter)

```mermaid
flowchart TD
    A[BroadcastBlockChange] --> B[Cria UpdateBlockMsg]
    B --> C[sendBoardMessage team, boardID]
    
    C --> D_local[sendBoardMessageSkipCluster]
    C --> D_cluster[sendMessageToCluster em goroutine]
    
    D_local --> E[getUserIDsForTeamAndBoard]
    E --> F[Intersecção: usuários conectados<br/>que são membros do board]
    F --> G[sendUserMessageSkipCluster<br/>PublishWebSocketEvent por userID]
    
    D_cluster --> H[ClusterMessage → json.Marshal]
    H --> I[PublishPluginClusterEvent]
    I --> J[HandleClusterEvent nó remoto]
    J --> K{BoardID != ''?}
    K -->|Sim| L[sendBoardMessageSkipCluster]
    K -->|Não| M{UserID != ''?}
    M -->|Sim| N[sendUserMessageSkipCluster]
    M -->|Não| O[sendTeamMessageSkipCluster]
```

## Ciclo de Vida do PluginAdapterClient

```mermaid
flowchart LR
    A[OnWebSocketConnect] --> B{webConnID existe?}
    B -->|Sim| C[Reativa: inactiveAt = 0]
    B -->|Não| D[Cria PluginAdapterClient]
    D --> E[addListener]
    E --> F[removeExpiredForUserID]
    
    C --> G[OnWebSocketDisconnect]
    F --> G
    G --> H[Seta inactiveAt = now]
    H --> I{isActive?}
    I -->|inactiveAt == 0| J[Ativo]
    I -->|inactiveAt > 0| K{hasExpired?}
    K -->|Sim| L[removeListener]
    K -->|Não| M[Aguardando reconexão]
```

## Fluxo de Autenticação

```mermaid
flowchart TD
    A[authenticateListener] --> B{isAuthenticated?}
    B -->|Sim| C[Re-auth ignorada: retorna]
    B -->|Não| D[getUserIDForToken]
    
    D --> E{singleUserToken > 0?}
    E -->|Sim| F{token == singleUserToken?}
    F -->|Sim| G[return SingleUser]
    F -->|Não| H[return '']
    
    E -->|Não| I[auth.GetSession]
    I --> J{session == nil ou erro?}
    J -->|Sim| K[return '']
    J -->|Não| L[return session.UserID]
    
    G --> M{userID == ''?}
    H --> M
    K --> M
    L --> N[Seta wsSession.userID = userID]
    M -->|Sim| O[conn.Close + return]
    M -->|Não| N
```
