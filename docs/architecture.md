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
