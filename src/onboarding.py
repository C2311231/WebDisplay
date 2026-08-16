"""
Webdisplay Onboarding System

Handles the onboarding flow of new players into the system.

License: MIT license

Author: C2311231

Notes:
"""

import secrets
import time
from cryptography.fernet import Fernet
import requests
from argon2.low_level import hash_secret_raw, Type
import logging
from encryption_handler import *

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def derive_key(pairing_code: str, salt: bytes) -> bytes:
    """
    Convert a human-readable pairing code into a 256-bit encryption key.
    """
    return hash_secret_raw(
        secret=pairing_code.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,  # 64 MB
        parallelism=4,
        hash_len=32,
        type=Type.ID,
    )

class OnboardingHandler:
    """
    Handles the onboarding flow of new players into the system.
    """

    def __init__(self, device_id: str, device_platform: str, device_capabilities: list[str], servers: list[str]):
        """
        Initializes the OnboardingHandler.
        """
        self.device_id = device_id
        self.device_platform = device_platform
        self.device_capabilities = device_capabilities
        self.pairing_code = self.generate_pairing_code()
        self.servers = []
        
        self.last_server_check_time = 0 

        # Possible states: not_paired, pairing_in_progress, paired
        self.pairing_state = "not_paired"

        self.encryption_key = Fernet.generate_key()

        for server in servers:
            # Store server URL and last contact time
            self.servers.append([server, 0])

    def start_onboarding(self):
        """
        Starts the onboarding process for a new player.

        """

        self.pairing_state = "pairing_in_progress"

        # Diplay pairing code on screen eventually, for now just print it
        print(f"Pairing Code: {self.pairing_code}")

        for server in self.servers:
            self.send_pairing_request(server)

    def send_pairing_request(self, server: list):
        # Send pairing code to server
        logging.info(f"Sending pairing request to server: {server[0]}")

        encrypted_data = encrypt_pairing_data(self.pairing_code, {
            "encryption_key": self.encryption_key.decode(),
            "pairing_code": self.pairing_code,
        })

        requests.post(f"{server[0]}/api/v1/onboarding/pairing", json={"device_id": self.device_id,
                      "platform": self.device_platform, "capabilities": self.device_capabilities,
                                                            "encrypted_data": encrypted_data})

        server[1] = time.time()  # Update last contact time

    def update(self):
        """
        Updates the onboarding process, checking for server responses.
        """
        if self.pairing_state == "pairing_in_progress":
            # Update pairing requests to servers
            for server in self.servers:
                if time.time() - server[1] > 3:  # Check every 3 seconds
                    self.send_pairing_request(server)
            
            if time.time() - self.last_server_check_time > 5:  # Check every 5 seconds
                self.last_server_check_time = time.time()
                for server in self.servers:
                    logging.debug(
                        f"Checking for pairing response from server: {server[0]}")
                    response = requests.get(
                        f"{server[0]}/api/v1/onboarding/pairing", params={"device_id": self.device_id})
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("status") == "awaiting_verification" and data.get("pairing_code") == self.pairing_code:
                            response = requests.get(f"{server[0]}/api/v1/onboarding/register", params={"device_id": self.device_id, "data": encrypt_msg(self.encryption_key, self.encryption_key)})
                            if response.status_code == 200:
                                logging.info(
                                    f"Device paired successfully with server: {server[0]}")
                                self.pairing_state = "paired"
                            return
                    server[1] = time.time()  # Update last contact time

    def generate_pairing_code(self, length=8):
        return "".join(
            secrets.choice(ALPHABET)
            for _ in range(length)
        )
