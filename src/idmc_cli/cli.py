import click
from idmc_cli.config import config

@click.group()
def main():
    """Informatica Cloud CLI Utility"""
    pass

@main.command()
@click.argument('asset_id')
def manage_assets(asset_id):
    """Manage an Informatica Cloud asset given an asset ID."""
    # Here, you'd call your API wrapper to manage the asset
    click.echo(f"Managing asset with ID: {asset_id}")

@main.command()
@click.argument('function_name')
def run_function(function_name):
    """Run a function on Informatica Cloud by name."""
    # Here, you'd call your API wrapper to run the function
    click.echo(f"Running function: {function_name}")

@main.command()
def configure():
    """Run a function on Informatica Cloud by name."""
    # Here, you'd call your API wrapper to run the function
    #click.echo(f"Starting configuration...")

    # Get and set the username
    user = config.get(key="username")
    user = input(f"Username [{ user }]: ") or user
    config.set("username", user)

    # Get and set the password
    password = config.get(key="password")
    password = input(f"Password [{ password }]: ") or password
    config.set("password", password)

    # Get and set the pod
    pod = config.get(key="pod")
    pod = input(f"Pod [{ pod }]: ") or pod
    config.set("pod", pod)

    # Get and set the region
    region = config.get(key="region")
    region = input(f"Region [{ region }]: ") or region
    config.set("region", region)

if __name__ == '__main__':
    main()
