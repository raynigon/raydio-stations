import click
from typing import List

def print_validation(errors: List[str]):
    if len(errors) > 0:
        click.secho("[ERROR] Database contains errors:", fg='red')
        for error in errors:
            click.secho(f"[ERROR] {error}", fg='red')
    click.echo(f"[INFO] Database is valid")