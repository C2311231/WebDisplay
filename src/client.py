"""
Webdisplay Server
Server Communication Client
License: MIT license

Author: C2311231

Notes:
"""
import requests
import time
import encryption_handler

class ServerClient():
    def __init__(self, server_address: str, player_id: str, encryption_key: bytes) -> None:
        self.server_address = server_address
        self.player_id = player_id
        self.encryption_key = encryption_key
        self.message_id = 0

    def _get(self, path: str, data: dict = {}):
        data["timestamp"] = time.time()
        data["message_id"] = self.message_id
        self.message_id += 1
        
        nonce, encrypted_data = encryption_handler.encrypt_msg(self.encryption_key, data)
        packet = {
            "player_id": self.player_id,
            "data": encrypted_data,
            "nonce": nonce
        }
        
        responce = requests.get(path, json=packet)
        
        if responce.ok:
            return responce.json()
        
        else:
            raise ValueError(f"An abnormal responce was recived: {responce.status_code}")
        
        
    def _post(self, path: str, data: dict = {}):
        data["timestamp"] = time.time()
        data["message_id"] = self.message_id
        self.message_id += 1
        
        nonce, encrypted_data = encryption_handler.encrypt_msg(self.encryption_key, data)
        packet = {
            "player_id": self.player_id,
            "data": encrypted_data,
            "nonce": nonce
        }
        
        responce = requests.post(path, json=packet)
        
        if responce.ok:
            return responce.json()
        
        else:
            raise ValueError(f"An abnormal responce was recived: {responce.status_code}")