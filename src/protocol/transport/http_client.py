"""
Webdisplay Server
Server Communication Client
License: MIT license

Author: C2311231

Notes:
"""
import requests
import protocol.encryption_handler as encryption_handler
import protocol.schemas as schemas

##TODO: Add handling for expired timestamps and message_id's to prevent replay attacks
##TODO: Add handling for validation errors.

class ServerClient():
    def __init__(self, server_address: str, player_id: str, encryption_key: bytes) -> None:
        self.server_address = server_address
        self.player_id = player_id
        self.encryption_key = encryption_key

    def get(self, path: str, data: dict = {}):
        player_payload = schemas.PlayerPayload.model_validate(data)

        nonce, encrypted_data = encryption_handler.encrypt_msg(self.encryption_key, player_payload.model_dump())
        
        packet = schemas.PlayerResponse.model_validate({
            "player_id": self.player_id,
            "ciphertext": encrypted_data,
            "nonce": nonce
        })

        responce = requests.get(path, json=packet.model_dump())
        if responce.ok:
            response_model = schemas.ServerResponse.model_validate(responce.json())
            payload = schemas.ServerPayload.model_validate(encryption_handler.decrypt_msg(self.encryption_key, response_model.nonce, response_model.ciphertext))
            return payload.model_dump()
        
        else:
            raise ValueError(f"An abnormal responce was recived: {responce.status_code}")
        
        
    def post(self, path: str, data: dict = {}):
        player_payload = schemas.PlayerPayload.model_validate(data)

        nonce, encrypted_data = encryption_handler.encrypt_msg(self.encryption_key, player_payload.model_dump())
        
        packet = schemas.PlayerResponse.model_validate({
            "player_id": self.player_id,
            "ciphertext": encrypted_data,
            "nonce": nonce
        })

        responce = requests.post(path, json=packet.model_dump())
        if responce.ok:
            response_model = schemas.ServerResponse.model_validate(responce.json())
            payload = schemas.ServerPayload.model_validate(encryption_handler.decrypt_msg(self.encryption_key, response_model.nonce, response_model.ciphertext))
            return payload.model_dump()
        
        else:
            raise ValueError(f"An abnormal responce was recived: {responce.status_code}")
