from typing import Dict
import click


@click.command()
@click.option("--text", help="text")
def capitalize(text: str) -> Dict[str, str]:
    message: Dict[str, str] = {"message": text.capitalize()}
    print(message)
    return message


if __name__ == "__main__":
    capitalize()
