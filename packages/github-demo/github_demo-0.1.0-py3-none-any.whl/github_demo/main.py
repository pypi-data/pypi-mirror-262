from typing import Dict


def say_hello() -> str:
    return "hello"


def capitalize(name: str) -> Dict[str, str]:
    return {"message": name.capitalize()}
