from typing import Optional


class NotFoundError(Exception):
    def __init__(self, key: str):
        super().__init__(f"secret {key} not found in the secrets store")
