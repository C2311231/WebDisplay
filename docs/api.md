# API

## Command Structure

### Server Messages

#### Server Unencrypted Data

``` json
    {
        "nonce": "nonce",
        "ciphertext": "encrypted_data"
    }
```

#### Server Encrypted Payload (after decryption)

``` json
    {
        "success": true,
        "error": null,
        "timestamp": 999999,
        "message_id": "uuid",
        "payload": {}
    }
```

### Player Messages

#### Player Unencrypted Data

``` json
    {
        "player_id": "uuid",
        "nonce": "nonce",
        "ciphertext": "encrypted_data"
    }

```

#### Player Encrypted Payload (after decryption)

``` json
    {
        "success": true,
        "error": null,
        "timestamp": 999999,
        "message_id": "uuid",
        "payload": {}
    }
```

### UI Messages

``` json

```