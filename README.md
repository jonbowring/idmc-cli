# idmc-cli
A CLI utility for interacting with Informatica Cloud

# How to activate the virtual environment

## Windows:
.venv\Scripts\activate

## Unix/macOS:
source .venv/bin/activate

# How to install the CLI
pip install -e .

# Example how to run the CLI
idmc-cli manage-assets 12345
idmc-cli run-function myFunction

# Known issues
This command works for passing a JSON string:

    idmc lookup test --body '{\"msg\": \"hello world\"}'

But this command does not:

    idmc lookup test --body '{\"msg\":\"hello world\"}'

It seems that without the space before the \ python or powershell is not able to properly interpret it