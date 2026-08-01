# System Architecture

## Overview

The system will follow a centralized server model where the player devices contact the server to update there configs and the users connect to the server to configure players.

``` mermaid
flowchart TB
    User[User]

    UI[Web UI]
    Server[Server]
    DB[(Database)]
    Content[(Content Storage)]

    Player1[Player]
    Player2[Player]
    PlayerN[Player...]

    Display1[Display]
    Display2[Display]

    User --> UI
    UI --> Server

    Server --> DB
    Server --> Content

    Server --> Player1
    Server --> Player2
    Server --> PlayerN

    Player1 --> Display1
    Player2 --> Display2
```

## Components

### Server

- Manages and provides the central source of truth for players and ui.
- Stores content and handles distribution.
- Generates configs for player devices.
- Distributes updates for devices.

### Player

- Displays scheduled content on connected displays.
- Downloads required content from server.

### Web UI

- Allows users to monitor and manage players, schedules, and configurations.
- Manages user accounts and authentication.

## Server Player API Architecture

``` mermaid
flowchart TB
    UI[Web UI]
    DM[Device Manager]
    DC[(Desired Config)]
    PS[(Player State)]
    PAPI[Player API Handler]
    SW[Sync Worker]
    P[Player]

    UI --> DM
    DM --> DC
    PS --> SW
    DC --> SW
    P --> PAPI
    PAPI --> PS
    SW --> PAPI
    PAPI --> P
```

- Server shall define the desired operating state of the Player device.
- A sync worker will ensure that the players current state matches the desired state.
- If the state doesn't match the Player API handler will issue corrections from the sync worker.
- Player device updates its state to follow api commands.
- Player will periodically report its state to the sync worker.

## Onboarding flow

``` mermaid
sequenceDiagram
    participant P as Player
    participant S as Server
    participant U as User

    P->>P: Generate device keypair
    P->>P: Generate pairing secret/code
    
    P->>P: Create encrypted pairing request
    P->>S: Submit pairing request

    P->>U: Display pairing code

    U->>S: Enter pairing code

    S->>S: Derive key from pairing code
    S->>S: Verify pairing request

    alt Pairing valid
        S->>P: Pairing approved
        P->>S: Exchange authentication information
        S->>P: Issue permanent credentials
        P->>P: Store credentials
    else Pairing invalid
        S->>U: Reject pairing
    end
```
