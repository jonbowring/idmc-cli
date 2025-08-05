import click
from idmc_cli.config import config
from idmc_cli.api import api

@click.group()
def main():
    """Informatica Cloud CLI Utility"""
    pass



@main.command()
def configure():
    """Used to configure the global parameters for the CLI."""

    # Get and set the username
    user = config.get("username")
    user = input(f"Username [{ user }]: ") or user
    config.set("username", user)

    # Get and set the password
    password = config.get("password")
    if password:
        password = '************' + password[-3:]
    password = input(f"Password [{ password }]: ") or password
    config.set("password", password)

    # Get and set the pod
    pod = config.get("pod")
    pod = input(f"Pod [{ pod }]: ") or pod
    config.set("pod", pod)

    # Get and set the region
    region = config.get("region")
    region = input(f"Region [{ region }]: ") or region
    config.set("region", region)



@main.command()
def login():
    """Used to login to Informatica Cloud and return the login details."""
    click.echo(api.login())

# User commands section

@main.group()
def users():
    """User management commands."""
    pass

@users.command()
def get():
    """Returns users"""
    click.echo(api.getUsers())


# Role commands section

@main.group()
def roles():
    """Role management commands."""
    pass

@roles.command()
def get():
    """Returns roles"""
    click.echo("Getting a role")


if __name__ == '__main__':
    main()
