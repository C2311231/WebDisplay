# Software Requirements

    To be defined at begaining of each stage of development.

## v2.0.0-dev.2

1. Player devices shall maintain a unique persistant identifier.
2. Player devices shall notify the server that they are ready to connect during onboarding.
3. Player devices shall provide the server with information including:

    - Device id
    - Software version
    - Platform
    - IP Address

4. Server shall create persistant records of registered players.
5. Server shall record the time of last communication with each player.
6. Players shall authenticate itself prior to connection.
7. Server shall approve or deny connections.
8. Players shall retry authentication if server communication fails.
9. Registration and authentication api shall be versioned and extendable.
10. Players and server shall not require any intervention to recover from network interuptions.
