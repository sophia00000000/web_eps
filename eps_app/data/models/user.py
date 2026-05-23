from dataclasses import dataclass


@dataclass
class User:
    id: int | None
    username: str
    password: str
    rol: str
    activo: int = 1