from enum import Enum

class ApiKeyPlace(Enum):
    HEADER_AUTHORIZATION = "headers/Authorization"
    ZERO_EX = "headers/0x-api-key"
    BODY = "request.body"

class ApiKey:
    def __init__(self, place: ApiKeyPlace, value: str):
        self.place = place
        self.value = value
