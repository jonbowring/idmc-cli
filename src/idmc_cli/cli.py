import click
import json
import polars as pl
from pathlib import Path
from idmc_cli.config import config
from idmc_cli.i18n import i18n
from idmc_cli.api import api

###################################
# Utility section
###################################

# Define the allowed output file types
out_types = ['.csv','.xlsx','.json']

def flatten_resp(resp):
    
    if isinstance(resp, list):
        flat_list = []
        for row in resp:
            flat_dict = {}
            for key, value in row.items():
                if isinstance(value, dict) or isinstance(value, list):
                    flat_dict[key] = json.dumps(value)
                else:
                    flat_dict[key] = value
            flat_list.append(flat_dict)
        return flat_list
    
    else:
        flat_dict = {}
        for key, value in resp.items():
            if isinstance(value, dict) or isinstance(value, list):
                flat_dict[key] = json.dumps(value)
            else:
                flat_dict[key] = value
        return flat_dict
    

def write_output(output, pretty, result):

    out_path = Path(output)
    
    if out_path.suffix == '.csv':
        result = flatten_resp(result)
        df = pl.from_dicts(result)
        df.write_csv(out_path, separator=',', quote_style='always')
    elif out_path.suffix == '.xlsx':
        df = pl.from_dicts(result)
        df.write_excel(workbook=out_path)
    elif out_path.suffix == '.json':
        with open(out_path, 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=pretty)

###################################
# Admin commands section
###################################

@click.group()
def idmc():
    """Informatica Cloud CLI Utility"""
    pass

@idmc.command('configure')
def configure():
    """Used to configure the global parameters for the CLI."""

    # Log out of current session
    api.logout()

    # Get and set the username
    user = config.get("username")
    user = input(f"Username [{ user }]: ") or user
    config.set("username", user)

    # Get and set the password
    password = config.get("password")
    if password:
        masked = '************' + password[-3:]
    else:
        masked = None
    password = input(f"Password [{ masked }]: ") or password
    config.set("password", password)

    # Get and set the pod
    pod = config.get("pod")
    pod = input(f"Pod [{ pod }]: ") or pod
    config.set("pod", pod)

    # Get and set the region
    region = config.get("region")
    region = input(f"Region [{ region }]: ") or region
    config.set("region", region)



@idmc.command('login')
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def login(debug, output, pretty=0):
    """Used to login to Informatica Cloud and return the login details."""

    result = api.login(debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@idmc.command('logout')
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def logout(debug, output, pretty=0):
    """Used to logout from Informatica Cloud."""

    result = api.logout(debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

###################################
# User commands section
###################################

@idmc.group('users')
def users():
    """User management commands."""
    pass

@users.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'get', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'get', 'username'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getUsers(id, username, debug, output, pretty=0):
    """Returns users"""
    
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    result = api.getUsers(id=id, username=username, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@users.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'delete', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'delete', 'username'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def deleteUser(id, username, debug, output, pretty=0):
    """Deletes a user"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and username is None:
        raise click.BadParameter(i18n.getErrorText('users', 'delete', 'id-uname-missing'))

    result = api.deleteUser(id=id, username=username, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))
    

@users.command('create')
@click.option('--name', '-n', 'name', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'name'))
@click.option('--first-name', '-f', 'first_name', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'first_name'))
@click.option('--last-name', '-l', 'last_name', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'last_name'))
@click.option('--password', '-p', 'password', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'password'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'description'))
@click.option('--email', '-e', 'email', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'email'))
@click.option('--title', '-t', 'title', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'title'))
@click.option('--phone', '-ph', 'phone', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'phone'))
@click.option('--force-password-change', '-fp', 'force_password_change', default=True, required=False, type=click.BOOL, help=i18n.getHelpOption('users', 'create', 'force_password_change'))
@click.option('--max-login-attempts', '-ml', 'max_login_attempts', default=None, required=False, type=click.INT, help=i18n.getHelpOption('users', 'create', 'max_login_attempts'))
@click.option('--authentication', '-a', 'authentication', default=None, required=False, type=click.INT, help=i18n.getHelpOption('users', 'create', 'authentication'))
@click.option('--alias-name', '-an', 'alias_name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'alias_name'))
@click.option('--role-ids', '-ri', 'role_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'role_ids'))
@click.option('--role-names', '-rn', 'role_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'role_names'))
@click.option('--group-ids', '-gi', 'group_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'group_ids'))
@click.option('--group-names', '-gn', 'group_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'create', 'group_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def createUser(name, first_name, last_name, email, password, description, title, phone, force_password_change, max_login_attempts, authentication, alias_name, role_ids, role_names, group_ids, group_names, debug, output, pretty=0):
    """Used to create new users"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if role_ids is None and role_names is None and group_ids is None and group_names is None:
        raise click.BadParameter(i18n.getErrorText('users', 'create', 'rid-rname-gid-gname-missing'))

    result = api.createUser(name=name, firstName=first_name, lastName=last_name, email=email, password=password, description=description, title=title, phone=phone, forcePasswordChange=force_password_change, maxLoginAttempts=max_login_attempts, authentication=authentication, aliasName=alias_name, roleIds=role_ids, roleNames=role_names, groupIds=group_ids, groupNames=group_names, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))
    

@users.command('add-roles')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-roles', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-roles', 'username'))
@click.option('--role-ids', '-ri', 'role_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-roles', 'role_ids'))
@click.option('--role-names', '-rn', 'role_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-roles', 'role_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def addUserRoles(id, username, role_ids, role_names, debug, output, pretty=0):
    """Adds role assignments to a user"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and username is None:
        raise click.BadParameter(i18n.getErrorText('users', 'add-roles', 'id-uname-missing'))
    elif role_ids is None and role_names is None:
        raise click.BadParameter(i18n.getErrorText('users', 'add-roles', 'rid-rname-missing'))

    result = api.addUserRoles(id=id, username=username, roleIds=role_ids, roleNames=role_names, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@users.command('remove-roles')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-roles', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-roles', 'username'))
@click.option('--role-ids', '-ri', 'role_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-roles', 'role_ids'))
@click.option('--role-names', '-rn', 'role_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-roles', 'role_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def removeUserRoles(id, username, role_ids, role_names, debug, output, pretty=0):
    """Removes role assignments from a user"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and username is None:
        raise click.BadParameter(i18n.getErrorText('users', 'remove-roles', 'id-uname-missing'))
    elif role_ids is None and role_names is None:
        raise click.BadParameter(i18n.getErrorText('users', 'remove-roles', 'rid-rname-missing'))

    result = api.removeUserRoles(id=id, username=username, roleIds=role_ids, roleNames=role_names, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@users.command('add-groups')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-groups', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-groups', 'username'))
@click.option('--group-ids', '-gi', 'group_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-groups', 'group_ids'))
@click.option('--group-names', '-gn', 'group_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-groups', 'group_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def addUserGroups(id, username, group_ids, group_names, debug, output, pretty=0):
    """Adds group assignments to a user"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and username is None:
        raise click.BadParameter(i18n.getErrorText('users', 'add-groups', 'id-uname-missing'))
    elif group_ids is None and group_names is None:
        raise click.BadParameter(i18n.getErrorText('users', 'add-groups', 'gid-gname-missing'))

    result = api.addUserGroups(id=id, username=username, groupIds=group_ids, groupNames=group_names, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@users.command('remove-groups')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-groups', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-groups', 'username'))
@click.option('--group-ids', '-gi', 'group_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-groups', 'group_ids'))
@click.option('--group-names', '-gn', 'group_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-groups', 'group_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def removeUserGroups(id, username, group_ids, group_names, debug, output, pretty=0):
    """Removes group assignments from a user"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and username is None:
        raise click.BadParameter(i18n.getErrorText('users', 'remove-groups', 'id-uname-missing'))
    elif group_ids is None and group_names is None:
        raise click.BadParameter(i18n.getErrorText('users', 'remove-groups', 'gid-gname-missing'))

    result = api.removeUserGroups(id=id, username=username, groupIds=group_ids, groupNames=group_names, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


###################################
# Password commands section
###################################

@users.group('password')
def password():
    """Password management commands."""
    pass

@password.command('change')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('password', 'change', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('password', 'change', 'username'))
@click.option('--old-password', '-o', 'old_password', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('password', 'change', 'old_password'))
@click.option('--new-password', '-n', 'new_password', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('password', 'change', 'new_password'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def changePassword(id, username, old_password, new_password, debug, output, pretty=0):
    """Change a users password"""  
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and username is None:
        raise click.BadParameter(i18n.getErrorText('users', 'remove-groups', 'id-uname-missing'))

    result = api.changePassword(id=id, username=username, oldPassword=old_password, newPassword=new_password, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@password.command('reset')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('password', 'reset', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('password', 'reset', 'username'))
@click.option('--security-answer', '-s', 'security_answer', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('password', 'reset', 'security_answer'))
@click.option('--new-password', '-n', 'new_password', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('password', 'reset', 'new_password'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def resetPassword(id, username, security_answer, new_password, debug, output, pretty=0):
    """Resets a users password using their security answer"""  
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and username is None:
        raise click.BadParameter(i18n.getErrorText('users', 'remove-groups', 'id-uname-missing'))

    result = api.resetPassword(id=id, username=username, securityAnswer=security_answer, newPassword=new_password, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

###################################
# User Groups commands section
###################################

@idmc.group('user-groups')
def userGroups():
    """User group management commands."""
    pass

@userGroups.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'get', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'get', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getUserGroups(id, name, debug, output, pretty=0):
    """Returns user groups"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getUserGroups(id=id, name=name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@userGroups.command('create')
@click.option('--name', '-n', 'name', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'description'))
@click.option('--role-ids', '-ri', 'role_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'role_ids'))
@click.option('--role-names', '-rn', 'role_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'role_names'))
@click.option('--user-ids', '-ui', 'user_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'user_ids'))
@click.option('--user-names', '-un', 'user_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'user_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def createUserGroup(name, description, role_ids, role_names, user_ids, user_names, debug, output, pretty=0):
    """Creates a new user group"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if role_ids is None and role_names is None:
        raise click.BadParameter(i18n.getErrorText('user-groups', 'create', 'rid-rname-missing'))

    result = api.createUserGroup(name=name, description=description, roleIds=role_ids, roleNames=role_names, userIds=user_ids, userNames=user_names, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@userGroups.command('add-roles')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'add-roles', 'id'))
@click.option('--group-name', '-gn', 'group_name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'add-roles', 'group_name'))
@click.option('--role-ids', '-ri', 'role_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'add-roles', 'role_ids'))
@click.option('--role-names', '-rn', 'role_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'add-roles', 'role_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def addUserGroupRoles(id, group_name, role_ids, role_names, debug, output, pretty=0):
    """Adds role assignments to a user group"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and group_name is None:
        raise click.BadParameter(i18n.getErrorText('user-groups', 'add-roles', 'id-gname-missing'))
    elif role_ids is None and role_names is None:
        raise click.BadParameter(i18n.getErrorText('user-groups', 'add-roles', 'rid-rname-missing'))

    result = api.addUserGroupRoles(id=id, groupname=group_name, roleIds=role_ids, roleNames=role_names, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@userGroups.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'delete', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'delete', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def deleteUserGroup(id, name, debug, output, pretty=0):
    """Deletes a user group"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.deleteUserGroup(id=id, name=name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))
    

###################################
# Role commands section
###################################

@idmc.group('roles')
def roles():
    """Role management commands."""
    pass

@roles.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'get', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'get', 'name'))
@click.option('--expand', '-e', 'expand', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('roles', 'get', 'expand'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getRoles(id, name, expand, debug, output, pretty=0):
    """Returns roles"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getRoles(id=id, name=name, expand=expand, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@roles.command('create')
@click.option('--name', '-n', 'name', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('roles', 'create', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'create', 'description'))
@click.option('--privilege-ids', '-pi', 'privilege_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'create', 'privilege_ids'))
@click.option('--privilege-names', '-pn', 'privilege_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'create', 'privilege_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def createRole(name, description, privilege_ids, privilege_names, debug, output, pretty=0):
    """Creates a new role"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if privilege_ids is None and privilege_names is None:
        raise click.BadParameter(i18n.getErrorText('roles', 'add-privileges', 'pid-pname-missing'))

    result = api.createRole(name=name, description=description, privilegeIds=privilege_ids, privilegeNames=privilege_names, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@roles.command('add-privileges')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'add-privileges', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'add-privileges', 'name'))
@click.option('--privilege-ids', '-pi', 'privilege_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'add-privileges', 'privilege_ids'))
@click.option('--privilege-names', '-pn', 'privilege_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'add-privileges', 'privilege_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def addRolePrivileges(id, name, privilege_ids, privilege_names, debug, output, pretty=0):
    """Adds privilege assignments to a role"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))
    elif privilege_ids is None and privilege_names is None:
        raise click.BadParameter(i18n.getErrorText('roles', 'add-privileges', 'pid-pname-missing'))

    result = api.addRolePrivileges(id=id, name=name, privilegeIds=privilege_ids, privilegeNames=privilege_names, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@roles.command('remove-privileges')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'remove-privileges', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'remove-privileges', 'name'))
@click.option('--privilege-ids', '-pi', 'privilege_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'remove-privileges', 'privilege_ids'))
@click.option('--privilege-names', '-pn', 'privilege_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'remove-privileges', 'privilege_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def removeRolePrivileges(id, name, privilege_ids, privilege_names, debug, output, pretty=0):
    """Remove privilege assignments from a role"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))
    elif privilege_ids is None and privilege_names is None:
        raise click.BadParameter(i18n.getErrorText('roles', 'remove-privileges', 'pid-pname-missing'))

    result = api.removeRolePrivileges(id=id, name=name, privilegeIds=privilege_ids, privilegeNames=privilege_names, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@roles.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'delete', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'delete', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def deleteRole(id, name, debug, output, pretty=0):
    """Deletes a role"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.deleteRole(id=id, name=name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))



###################################
# Privileges commands section
###################################

@idmc.group('privileges')
def privileges():
    """Privilege management commands."""
    pass

@privileges.command('get')
@click.option('--all', 'all', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('privileges', 'get', 'all'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getPrivileges(all, debug, output, pretty=0):
    """Returns privileges"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getPrivileges(all=all, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

###################################
# Lookup commands section
###################################

@idmc.group('lookup')
def lookup():
    """Lookup objects."""
    pass

@lookup.command('object')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('lookup', 'object', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('lookup', 'object', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('lookup', 'object', 'type'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def lookupObject(id, path, type, debug, output, pretty=0):
    """Lookup a single object"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('lookup', 'object', 'id-path-type-missing'))
    elif id is None and ( path is None or type is None ):
        raise click.BadParameter(i18n.getErrorText('lookup', 'object', 'path-type-missing'))
    
    result = api.lookupObject(id=id, path=path, type=type, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@lookup.command('objects')
@click.option('--body', '-b', 'body', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('lookup', 'objects', 'body'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def lookupObjects(body, debug, output, pretty=0):
    """Lookup multiple objects"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.lookupObjects(body=body, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

###################################
# Object commands section
###################################

@idmc.group('objects')
def objects():
    """Object management commands."""
    pass

@objects.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'get', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'get', 'name'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'get', 'type'))
@click.option('--location', '-l', 'location', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'location'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getObjects(id, name, type, location, debug, output, pretty=0):
    """Used to get objects"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getObjects(id=id, name=name, type=type, location=location, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@objects.command('query')
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'type'))
@click.option('--location', '-l', 'location', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'location'))
@click.option('--tag', '-T', 'tag', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'tag'))
@click.option('--checked-out-by', '-co', 'checked_out_by', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'checked-out-by'))
@click.option('--checked-out-since', '-cos', 'checked_out_since', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'checked-out-since'))
@click.option('--checked-out-until', '-cou', 'checked_out_until', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'checked-out-until'))
@click.option('--checked-in-by', '-ci', 'checked_in_by', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'checked-in-by'))
@click.option('--checked-in-since', '-cis', 'checked_in_since', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'checked-in-since'))
@click.option('--checked-in-until', '-ciu', 'checked_in_until', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'checked-in-until'))
@click.option('--source-ctrld', '-s', 'source_cntrld', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('objects', 'query', 'source-ctrld'))
@click.option('--hash', '-h', 'hash', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'hash'))
@click.option('--published-by', '-p', 'published_by', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'published-by'))
@click.option('--published-since', '-ps', 'published_since', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'published-since'))
@click.option('--published-until', '-pu', 'published_until', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'published-until'))
@click.option('--updated-by', '-u', 'updated_by', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'updated-by'))
@click.option('--updated-since', '-us', 'updated_since', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'updated-since'))
@click.option('--updated-until', '-uu', 'updated_until', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'query', 'updated-until'))

@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def queryObjects(type, location, tag, checked_out_by, checked_out_since, checked_out_until, checked_in_by, checked_in_since, checked_in_until, source_cntrld, hash, published_by, published_since, published_until, updated_by, updated_since, updated_until, debug, output, pretty=0):
    """Used to query objects"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.queryObjects(type=type, location=location, tag=tag, hash=hash, checkedOutBy=checked_out_by, checkedOutSince=checked_out_since, checkedOutUntil=checked_out_until, checkedInBy=checked_in_by, checkedInSince=checked_in_since, checkedInUntil=checked_in_until, sourceCtrld=source_cntrld, publishedBy=published_by, publishedSince=published_since, publishedUntil=published_until, updatedBy=updated_by, updatedSince=updated_since, updatedUntil=updated_until, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@objects.command('dependencies')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'dependencies', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'dependencies', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'dependencies', 'type'))
@click.option('--ref-type', '-r', 'ref_type', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('objects', 'dependencies', 'ref_type'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getDependencies(id, path, type, ref_type, debug, output, pretty=0):
    """Returns dependencies for an object"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and ( path is None or type is None ):
        raise click.BadParameter(i18n.getErrorText('common', None, 'path-type-missing'))

    result = api.getDependencies(id=id, path=path, type=type, refType=ref_type, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@objects.command('add-tags')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'add-tags', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'add-tags', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'add-tags', 'type'))
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'add-tags', 'body'))
@click.option('--tags', '-T', 'tags', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'add-tags', 'tags'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def tagObject(id, path, type, body, tags, debug, output, pretty=0):
    """Adds one or more tags to an object"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if body is None and id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('objects', 'add-tags', 'body-id-path-type-missing'))
    elif body is None and id is None and ( path is None or type is None ):
        raise click.BadParameter(i18n.getErrorText('objects', 'add-tags', 'path-type-missing'))
    
    if body:
         result = api.tagObjects(body=body, debug=debug)
    else:
        result = api.tagObject(id=id, path=path, type=type, tags=tags, debug=debug)

    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@objects.command('remove-tags')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'remove-tags', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'remove-tags', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'remove-tags', 'type'))
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'remove-tags', 'body'))
@click.option('--tags', '-T', 'tags', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'remove-tags', 'tags'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def tagObject(id, path, type, body, tags, debug, output, pretty=0):
    """Removes one or more tags from an object"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if body is None and id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('objects', 'remove-tags', 'body-id-path-type-missing'))
    elif body is None and id is None and ( path is None or type is None ):
        raise click.BadParameter(i18n.getErrorText('objects', 'remove-tags', 'path-type-missing'))
    
    if body:
        result = api.untagObjects(body=body, debug=debug)
    else:
        result = api.untagObject(id=id, path=path, type=type, tags=tags, debug=debug)

    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@objects.group('permissions')
def permissions():
    """Permission management commands."""
    pass

@permissions.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'get', 'id'))
@click.option('--acl', '-a', 'acl', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'get', 'acl'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'get', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'get', 'type'))
@click.option('--check-access', '-c', 'check_access', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('permissions', 'get', 'check_access'))
@click.option('--check-type', '-ct', 'check_type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'get', 'check_type'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getPermissions(id, acl, path, type, check_access, check_type, debug, output, pretty=0):
    """Gets permission ACL's for an object"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-path-type-missing'))
    if check_type is not None and check_access == False:
        check_access = True

    result = api.getPermissions(id=id, acl=acl, path=path, type=type, checkAccess=check_access, checkType=check_type, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@permissions.command('create')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'create', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'create', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'create', 'type'))
@click.option('--ptype', '-pt', 'ptype', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('permissions', 'create', 'ptype'))
@click.option('--pname', '-pn', 'pname', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('permissions', 'create', 'pname'))
@click.option('--read', '-r', 'read', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('permissions', 'create', 'read'))
@click.option('--update', '-u', 'update', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('permissions', 'create', 'update'))
@click.option('--delete', '-d', 'delete', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('permissions', 'create', 'delete'))
@click.option('--execute', '-e', 'execute', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('permissions', 'create', 'execute'))
@click.option('--change', '-c', 'change', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('permissions', 'create', 'change'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def createPermission(id, path, type, ptype, pname, read, update, delete, execute, change, debug, output, pretty=0):
    """Creates a permission ACL for an object"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-path-type-missing'))

    result = api.createPermission(id=id, path=path, type=type, ptype=ptype, pname=pname, read=read, update=update, delete=delete, execute=execute, change=change, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@permissions.command('update')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'update', 'id'))
@click.option('--acl', '-a', 'acl', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'update', 'acl'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'update', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'update', 'type'))
@click.option('--ptype', '-pt', 'ptype', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('permissions', 'update', 'ptype'))
@click.option('--pname', '-pn', 'pname', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('permissions', 'update', 'pname'))
@click.option('--read', '-r', 'read', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('permissions', 'update', 'read'))
@click.option('--update', '-u', 'update', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('permissions', 'update', 'update'))
@click.option('--delete', '-d', 'delete', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('permissions', 'update', 'delete'))
@click.option('--execute', '-e', 'execute', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('permissions', 'update', 'execute'))
@click.option('--change', '-c', 'change', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('permissions', 'update', 'change'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def updatePermission(id, acl, path, type, ptype, pname, read, update, delete, execute, change, debug, output, pretty=0):
    """Updates a permission ACL for an object"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-path-type-missing'))

    result = api.updatePermission(id=id, acl=acl, path=path, type=type, ptype=ptype, pname=pname, read=read, update=update, delete=delete, execute=execute, change=change, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


@permissions.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'delete', 'id'))
@click.option('--acl', '-a', 'acl', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'delete', 'acl'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'delete', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('permissions', 'delete', 'type'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def deletePermissions(id, acl, path, type, debug, output, pretty=0):
    """Deletes permission ACL's for an object"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-path-type-missing'))

    result = api.deletePermissions(id=id, acl=acl, path=path, type=type, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


###################################
# Project commands section
###################################

@idmc.group('projects')
def projects():
    """Project management commands."""
    pass

@projects.command('create')
@click.option('--name', '-n', 'name', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('projects', 'create', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'create', 'description'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def createProject(name, description, debug, output, pretty=0):
    """Creates a project"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.createProject(name=name, description=description, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@projects.command('update')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'update', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'update', 'path'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'update', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'update', 'description'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def updateProject(id, name, path, description, debug, output, pretty=0):
    """Updates a project"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and path is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-path-missing'))

    result = api.updateProject(id=id, path=path, name=name, description=description, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@projects.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'delete', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'delete', 'path'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def deleteProject(id, path, debug, output, pretty=0):
    """Deletes a project"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and path is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-path-missing'))

    result = api.deleteProject(id=id, path=path, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

###################################
# Folder commands section
###################################

@projects.group('folders')
def folders():
    """Folder management commands."""
    pass

@folders.command('create')
@click.option('--project-id', '-pi', 'project_id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'create', 'project_id'))
@click.option('--project-name', '-pn', 'project_name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'create', 'project_name'))
@click.option('--name', '-n', 'name', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('folders', 'create', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'create', 'description'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def createFolder(project_id, project_name, name, description, debug, output, pretty=0):
    """Creates a folder"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if project_id is None and project_name is None:
        raise click.BadParameter(i18n.getErrorText('folders', 'create', 'pid-pname-missing'))

    result = api.createFolder(projectId=project_id, projectName=project_name, name=name, description=description, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@folders.command('update')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'update', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'update', 'path'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'update', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'update', 'description'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def createProject(id, name, path, description, debug, output, pretty=0):
    """Updates a folder"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and path is None:
        raise click.BadParameter(i18n.getErrorText('folders', 'update', 'id-path-missing'))

    result = api.updateFolder(id=id, path=path, name=name, description=description, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@folders.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'delete', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'delete', 'path'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def deleteFolder(id, path, debug, output, pretty=0):
    """Deletes a folder"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and path is None:
        raise click.BadParameter(i18n.getErrorText('folders', 'delete', 'id-path-missing'))

    result = api.deleteFolder(id=id, path=path, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


###################################
# Source control commands section
###################################

@idmc.group('source-control')
def sourceControl():
    """Source control management commands."""
    pass

@sourceControl.command('check-in')
@click.option('--summary', '-s', 'summary', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-in', 'summary'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-in', 'description'))
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-in', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-in', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-in', 'type'))
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-in', 'body'))
@click.option('--include-container', '-I', 'include_container', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'check-in', 'include_container'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def checkInObject(summary, description, id, path, type, include_container, body, debug, output, pretty=0):
    """Checks in one or more objects"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if body is None and id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'body-id-path-type-missing'))
    elif body is None and id is None and ( path is None or type is None ):
        raise click.BadParameter(i18n.getErrorText('common', None, 'path-type-missing'))
    
    if body:
        result = api.checkInObjects(summary=summary, description=description, body=body, debug=debug)
    else:
        result = api.checkInObject(summary=summary, description=description, id=id, path=path, type=type, includeContainer=include_container, debug=debug)

    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@sourceControl.command('check-out')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-out', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-out', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-out', 'type'))
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-out', 'body'))
@click.option('--include-container', '-I', 'include_container', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'check-out', 'include_container'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def checkOutObject(id, path, type, include_container, body, debug, output, pretty=0):
    """Checks out one or more objects"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if body is None and id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'body-id-path-type-missing'))
    elif body is None and id is None and ( path is None or type is None ):
        raise click.BadParameter(i18n.getErrorText('common', None, 'path-type-missing'))
    
    if body:
        result = api.checkOutObjects(body=body, debug=debug)
    else:
        result = api.checkOutObject(id=id, path=path, type=type, includeContainer=include_container, debug=debug)

    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@sourceControl.command('undo-check-out')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'undo-check-out', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'undo-check-out', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'undo-check-out', 'type'))
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'undo-check-out', 'body'))
@click.option('--include-container', '-I', 'include_container', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'undo-check-out', 'include_container'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def undoCheckOutObject(id, path, type, include_container, body, debug, output, pretty=0):
    """Undo check out for one or more objects"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if body is None and id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'body-id-path-type-missing'))
    elif body is None and id is None and ( path is None or type is None ):
        raise click.BadParameter(i18n.getErrorText('common', None, 'path-type-missing'))
    
    if body:
        result = api.undoCheckOutObjects(body=body, debug=debug)
    else:
        result = api.undoCheckOutObject(id=id, path=path, type=type, includeContainer=include_container, debug=debug)

    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@sourceControl.command('pull')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull', 'type'))
@click.option('--hash', '-h', 'hash', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull', 'hash'))
@click.option('--relax-validation', '-r', 'relax_validation', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'pull', 'relax_validation'))
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull', 'body'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def pullObjects(id, path, type, hash, relax_validation, body, debug, output, pretty=0):
    """Pulls one or more objects"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if body is None and id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'body-id-path-type-missing'))
    elif body is None and id is None and ( path is None or type is None ):
        raise click.BadParameter(i18n.getErrorText('common', None, 'path-type-missing'))
    
    if body:
        result = api.pullObjects(body=body, hash=hash, relaxValidation=relax_validation, debug=debug)
    else:
        result = api.pullObject(id=id, path=path, type=type, hash=hash, relaxValidation=relax_validation, debug=debug)

    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@sourceControl.command('pull-commit-hash')
@click.option('--hash', '-h', 'hash', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull-commit-hash', 'hash'))
@click.option('--search', '-s', 'search', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'pull-commit-hash', 'search'))
@click.option('--repo-id', '-ri', 'repo_id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull-commit-hash', 'repo_id'))
@click.option('--relax-validation', '-r', 'relax_validation', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'pull-commit-hash', 'relax_validation'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def checkOutObject(hash, search, repo_id, relax_validation, debug, output, pretty=0):
    """Pulls all objects in a commit hash"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.pullByCommitHash(hash=hash, search=search, repoId=repo_id, relaxValidation=relax_validation, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@sourceControl.command('status')
@click.option('--id', '-i', 'id', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('source-control', 'status', 'id'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getSourceStatus(id, debug, output, pretty=0):
    """Gets the status of a source control action"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getSourceStatus(id=id, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@sourceControl.command('repo-details')
@click.option('--project-ids', '-i', 'project_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'repo-details', 'project_ids'))
@click.option('--project-names', '-n', 'project_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'repo-details', 'project_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getSourceStatus(project_ids, project_names, debug, output, pretty=0):
    """Gets the source control repository details"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if project_ids is None and project_names is None:
        raise click.BadParameter(i18n.getErrorText('source-control', 'repo-details', 'pid-pname-missing'))

    result = api.getRepoConnection(projectIds=project_ids, projectNames=project_names, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@sourceControl.command('commit-history')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-history', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-history', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-history', 'type'))
@click.option('--branch', '-b', 'branch', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-history', 'branch'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getCommitHistory(id, path, type, branch, debug, output, pretty=0):
    """Gets the commit history for an asset"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-path-type-missing'))
    elif id is None and ( path is None or type is None ):
        raise click.BadParameter(i18n.getErrorText('common', None, 'path-type-missing'))

    result = api.getCommitHistory(id=id, path=path, type=type, branch=branch, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@sourceControl.command('commit-details')
@click.option('--hash', '-h', 'hash', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-details', 'hash'))
@click.option('--search-all', '-s', 'search_all', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'commit-details', 'search_all'))
@click.option('--repo-id', '-r', 'repo_id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-details', 'repo_id'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getCommitDetails(hash, search_all, repo_id, debug, output, pretty=0):
    """Gets the details for a commit"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getCommitDetails(hash=hash, searchAllRepos=search_all, repoId=repo_id, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@sourceControl.command('compare-versions')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-history', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'compare-versions', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'compare-versions', 'type'))
@click.option('--old-version', '-o', 'old_version', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('source-control', 'compare-versions', 'old_version'))
@click.option('--new-version', '-n', 'new_version', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('source-control', 'compare-versions', 'new_version'))
@click.option('--format', '-f', 'format', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('source-control', 'compare-versions', 'format'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def compareVersions(id, path, type, old_version, new_version, format, debug, output, pretty=0):
    """Used to compare two versions of an asset."""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and path is None and type is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-path-type-missing'))
    elif id is None and ( path is None or type is None ):
        raise click.BadParameter(i18n.getErrorText('common', None, 'path-type-missing'))

    result = api.compareVersions(id=id, path=path, type=type, oldVersion=old_version, newVersion=new_version, format=format, debug=debug)
    if output:
        write_output(output, pretty, result)
    elif format == 'JSON':
        click.echo(json.dumps(result, indent=pretty))
    else:
        click.echo(result)

###################################
# Log commands section
###################################

@idmc.group('logs')
def logs():
    """Log commands."""
    pass

@logs.command('security')
@click.option('--category', '-c', 'category', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'security', 'category'))
@click.option('--actor', '-a', 'actor', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'security', 'actor'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'security', 'name'))
@click.option('--from', '-f', 'time_from', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'security', 'time_from'))
@click.option('--to', '-t', 'time_to', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'security', 'time_to'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getSecurityLogs(category, actor, name, time_from, time_to, debug, output, pretty=0):
    """Gets the security logs"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getSecurityLogs(category=category, actor=actor, name=name, time_from=time_from, time_to=time_to, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@logs.group('activity')
def logsActivity():
    """Activity log commands."""
    pass

@logsActivity.command('completed')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'completed-activity', 'id'))
@click.option('--run-id', '-r', 'run_id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'completed-activity', 'run-id'))
@click.option('--task-id', '-t', 'task_id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'completed-activity', 'task-id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'completed-activity', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getCompletedActivityJobs(id, run_id, task_id, name, debug, output, pretty=0):
    """Gets the completed activity logs"""
    
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if run_id and task_id is None:
        raise click.BadParameter(i18n.getErrorText('logs', 'completed-activity', 'task-id-missing'))

    result = api.getCompletedActivityJobs(id=id, runId=run_id, taskId=task_id, taskName=name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@logsActivity.command('running')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'running-activity', 'id'))
@click.option('--run-id', '-r', 'run_id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'running-activity', 'run-id'))
@click.option('--task-id', '-t', 'task_id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'running-activity', 'task-id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('logs', 'running-activity', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getRunningActivityJobs(id, run_id, task_id, name, debug, output, pretty=0):
    """Gets the running activity logs"""
    
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if run_id and task_id is None:
        raise click.BadParameter(i18n.getErrorText('logs', 'running-activity', 'task-id-missing'))

    result = api.getRunningActivityJobs(id=id, runId=run_id, taskId=task_id, taskName=name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

###################################
# Secure agent commands section
###################################

@idmc.group('agents')
def agents():
    """Secure Agent management commands."""
    pass

@agents.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'get', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'get', 'name'))
@click.option('--unassigned', '-u', 'unassigned', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('agents', 'get', 'unassigned'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getAgents(id, name, unassigned, debug, output, pretty=0):
    """Gets Secure Agents"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getAgents(id=id, name=name, unassigned=unassigned, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@agents.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'delete', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'delete', 'name'))
@click.option('--unassigned', '-u', 'unassigned', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('agents', 'delete', 'unassigned'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def deleteAgent(id, name, unassigned, debug, output, pretty=0):
    """Deletes a secure agent"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.deleteAgent(id=id, name=name, unassigned=unassigned, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@agents.command('status')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'status', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'status', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getAgentStatus(id, name, debug, output, pretty=0):
    """Gets Secure Agent Status"""

    result = api.getAgentStatus(id=id, name=name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@agents.group('service')
def service():
    """Secure Agent service management commands."""
    pass

@service.command('stop')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('services', 'stop', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('services', 'stop', 'name'))
@click.option('--service', '-s', 'service', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('services', 'stop', 'service'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def stopService(id, name, service, debug, output, pretty=0):
    """Stops a service on a secure agent"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.execAgentService(id=id, name=name, service=service, action='stop', debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@service.command('start')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('services', 'start', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('services', 'start', 'name'))
@click.option('--service', '-s', 'service', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('services', 'start', 'service'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def startService(id, name, service, debug, output, pretty=0):
    """Starts a service on a secure agent"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.execAgentService(id=id, name=name, service=service, action='start', debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

###################################
# Secure agent group commands section
###################################

@agents.group('groups')
def agentGroup():
    """Secure Agent Group service management commands."""
    pass

@agentGroup.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'get', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'get', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getAgentGroups(id, name, debug, output, pretty=0):
    """Gets Secure Agent Groups"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getAgentGroups(id=id, name=name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@agentGroup.command('create')
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'create', 'name'))
@click.option('--shared', '-s', 'shared', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('agentGroup', 'create', 'shared'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def createAgentGroup(name, shared, debug, output, pretty=0):
    """Creates a secure agent group"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.createAgentGroup(name=name, shared=shared, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@agentGroup.command('add-agent')
@click.option('--group-id', '-gi', 'group_id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'add', 'group_id'))
@click.option('--group-name', '-gn', 'group_name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'add', 'group_name'))
@click.option('--agent-id', '-ai', 'agent_id', multiple=True, default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'add', 'agent_id'))
@click.option('--agent-name', '-an', 'agent_name', multiple=True, default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'add', 'agent_name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def addAgent(group_id, group_name, agent_id, agent_name, debug, output, pretty=0):
    """Add one or more agents to a secure agent group"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if group_id is None and group_name is None:
        raise click.BadParameter(i18n.getErrorText('agentGroup', 'add', 'groupid-groupname-missing'))
    if len(agent_id) == 0 and len(agent_name) == 0:
        raise click.BadParameter(i18n.getErrorText('agentGroup', 'add', 'agentid-agentname-missing'))

    result = api.addAgent(groupId=group_id, groupName=group_name, agentId=agent_id, agentName=agent_name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@agentGroup.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'delete', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'delete', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def deleteAgentGroup(id, name, debug, output, pretty=0):
    """Deletes a secure agent group"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.deleteAgentGroup(id=id, name=name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@agentGroup.group('components')
def components():
    """Secure Agent Group component management commands."""
    pass

@components.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'list-components', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'list-components', 'name'))
@click.option('--include-all', '-a', 'include_all', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('agentGroup', 'list-components', 'include_all'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getAgentGroupComponents(id, name, include_all, debug, output, pretty=0):
    """Gets Secure Agent Group components"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.getAgentGroupComponents(id=id, name=name, includeAll=include_all, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@components.command('update')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-components', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-components', 'name'))
@click.option('--enable', '-e', 'enable', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('agentGroup', 'update-components', 'enable'))
@click.option('--disable', '-d', 'disable', flag_value=False, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('agentGroup', 'update-components', 'disable'))
@click.option('--services', '-s', 'services', multiple=True, default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-components', 'services'))
@click.option('--connectors', '-c', 'connectors', multiple=True, default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-components', 'connectors'))
@click.option('--additional', '-a', 'additional', multiple=True, default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-components', 'additional'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def updateAgentGroupComponents(id, name, enable, disable, services, connectors, additional, debug, output, pretty=0):
    """Can be used to enable or disable Secure Agent Group components"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))
    
    if enable is None and disable is None:
        raise click.BadParameter(i18n.getErrorText('agentGroup', 'update-components', 'enable-disable-missing'))
    
    if len(services) == 0 and len(connectors) == 0 and len(additional) == 0:
        raise click.BadParameter(i18n.getErrorText('agentGroup', 'update-components', 'services-connectors-additional-missing'))
    
    if disable:
        enable=disable
    
    try:

        result = api.updateAgentGroupComponents(id=id, name=name, enable=enable, services=services, connectors=connectors, additional=additional, debug=debug)
        if output:
            write_output(output, pretty, result)
        else:
            click.echo(json.dumps(result, indent=pretty))
    except Exception as e:
        raise click.ClickException(e)

@agentGroup.group('properties')
def properties():
    """Secure Agent Group property management commands."""
    pass

@properties.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'list-props', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'list-props', 'name'))
@click.option('--service', '-s', 'service', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'list-props', 'service'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'list-props', 'type'))
@click.option('--property', '-k', 'property', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'list-props', 'property'))
@click.option('--overridden', '-o', 'overridden', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('agentGroup', 'list-props', 'overridden'))
@click.option('--platform', '-p', 'platform', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'list-props', 'platform'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getAgentGroupProps(id, name, overridden, platform, service, type, property, debug, output, pretty=0):
    """Gets Secure Agent Group properties"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.getAgentGroupProps(id=id, name=name, overridden=overridden, platform=platform, service=service, type=type, property=property, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@properties.command('update')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-prop', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-prop', 'name'))
@click.option('--service', '-s', 'service', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-prop', 'service'))
@click.option('--type', '-t', 'type', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-prop', 'type'))
@click.option('--property', '-k', 'property', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-prop', 'property'))
@click.option('--value', '-v', 'value', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-prop', 'value'))
@click.option('--platform', '-p', 'platform', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'update-prop', 'platform'))
@click.option('--custom', '-c', 'custom', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('agentGroup', 'update-prop', 'custom'))
@click.option('--sensitive', '-S', 'sensitive', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('agentGroup', 'update-prop', 'sensitive'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def updateAgentGroupProps(id, name, service, type, property, value, platform, custom, sensitive, debug, output, pretty=0):
    """Updates Secure Agent Group properties"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.updateAgentGroupProps(id=id, name=name, service=service, type=type, property=property, value=value, platform=platform, custom=custom, sensitive=sensitive, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@properties.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'delete-props', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'delete-props', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def deleteAgentGroupProps(id, name, debug, output, pretty=0):
    """Deletes Secure Agent Group properties"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.deleteAgentGroupProps(id=id, name=name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

###################################
# Schedules commands section
###################################

@idmc.group('schedules')
def schedules():
    """Schedule management commands."""
    pass

@schedules.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'get', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'get', 'name'))
@click.option('--status', '-s', 'status', default='enabled', required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'get', 'status'))
@click.option('--interval', '-I', 'interval', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'get', 'interval'))
@click.option('--from', '-f', 'time_from', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'get', 'time_from'))
@click.option('--to', '-t', 'time_to', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'get', 'time_to'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getSchedules(id, name, status, interval, time_from, time_to, debug, output, pretty=0):
    """Gets schedules details"""  
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getSchedules(id=id, name=name, status=status, interval=interval, time_from=time_from, time_to=time_to, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@schedules.command('create')
@click.option('--name', '-n', 'name', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'description'))
@click.option('--status', '-s', 'status', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'status'))
@click.option('--start-time', '-S', 'start_time', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'start_time'))
@click.option('--end-time', '-e', 'end_time', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'end_time'))
@click.option('--interval', '-I', 'interval', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'interval'))
@click.option('--frequency', '-f', 'frequency', default=None, required=False, type=click.INT, help=i18n.getHelpOption('schedules', 'create', 'frequency'))
@click.option('--range-start', '-rs', 'range_start', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'range_start'))
@click.option('--range-end', '-re', 'range_end', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'range_end'))
@click.option('--timezone', '-t', 'timezone', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'timezone'))
@click.option('--weekday', '-w', 'weekday', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'weekday'))
@click.option('--day-of-month', '-dm', 'day_of_month', default=None, required=False, type=click.INT, help=i18n.getHelpOption('schedules', 'create', 'day_of_month'))
@click.option('--week-of-month', '-wm', 'week_of_month', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'week_of_month'))
@click.option('--day-of-week', '-dw', 'day_of_week', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'create', 'day_of_week'))
@click.option('--sunday', '-sun', 'sun', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'create', 'sun'))
@click.option('--monday', '-mon', 'mon', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'create', 'mon'))
@click.option('--tuesday', '-tue', 'tue', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'create', 'tue'))
@click.option('--wednesday', '-wed', 'wed', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'create', 'wed'))
@click.option('--thursday', '-thu', 'thu', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'create', 'thu'))
@click.option('--friday', '-fri', 'fri', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'create', 'fri'))
@click.option('--saturday', '-sat', 'sat', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'create', 'sat'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def createSchedule(name, description, status, start_time, end_time, interval, frequency, range_start, range_end, timezone, weekday, day_of_month, week_of_month, day_of_week, sun, mon, tue, wed, thu, fri, sat, debug, output, pretty=0):
    """Creates a schedule"""
    
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    # Validate the options
    if ( sun is not None or mon is not None or tue is not None or wed is not None or thu is not None or fri is not None or sat is not None ) and interval not in ['Minutely', 'Hourly', 'Weekly', 'Biweekly']:
        raise click.BadParameter(i18n.getErrorText('schedules', 'create', 'day-missing'))
    if weekday is not None and interval != 'Daily':
        raise click.BadParameter(i18n.getErrorText('schedules', 'create', 'weekday-incorrect'))
    if ( day_of_month is not None  or day_of_week is not None or week_of_month is not None) and interval != 'Monthly':
        raise click.BadParameter(i18n.getErrorText('schedules', 'create', 'month-incorrect'))
    if frequency is not None and interval not in ['Minutely', 'Hourly', 'Daily']:
        raise click.BadParameter(i18n.getErrorText('schedules', 'create', 'frequency-incorrect'))
    if range_start is not None and interval not in ['Minutely', 'Hourly', 'Daily']:
        raise click.BadParameter(i18n.getErrorText('schedules', 'create', 'range-start-incorrect'))
    if range_end is not None and interval not in ['Minutely', 'Hourly', 'Daily']:
        raise click.BadParameter(i18n.getErrorText('schedules', 'create', 'range-end-incorrect'))
    if timezone is not None and day_of_month is None and week_of_month is None and day_of_week is None:
        raise click.BadParameter(i18n.getErrorText('schedules', 'create', 'timezone-incorrect'))

    result = api.createSchedule(name=name, description=description, status=status, startTime=start_time, endTime=end_time, interval=interval, frequency=frequency, rangeStart=range_start, rangeEnd=range_end, timezone=timezone, weekday=weekday, dayOfMonth=day_of_month, weekOfMonth=week_of_month, dayOfWeek=day_of_week, sun=sun, mon=mon, tue=tue, wed=wed, thu=thu, fri=fri, sat=sat, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@schedules.command('update')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'description'))
@click.option('--status', '-s', 'status', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'status'))
@click.option('--start-time', '-S', 'start_time', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'start_time'))
@click.option('--end-time', '-e', 'end_time', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'end_time'))
@click.option('--interval', '-I', 'interval', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'interval'))
@click.option('--frequency', '-f', 'frequency', default=None, required=False, type=click.INT, help=i18n.getHelpOption('schedules', 'update', 'frequency'))
@click.option('--range-start', '-rs', 'range_start', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'range_start'))
@click.option('--range-end', '-re', 'range_end', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'range_end'))
@click.option('--timezone', '-t', 'timezone', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'timezone'))
@click.option('--weekday', '-w', 'weekday', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'weekday'))
@click.option('--day-of-month', '-dm', 'day_of_month', default=None, required=False, type=click.INT, help=i18n.getHelpOption('schedules', 'update', 'day_of_month'))
@click.option('--week-of-month', '-wm', 'week_of_month', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'week_of_month'))
@click.option('--day-of-week', '-dw', 'day_of_week', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'update', 'day_of_week'))
@click.option('--sunday', '-sun', 'sun', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'update', 'sun'))
@click.option('--monday', '-mon', 'mon', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'update', 'mon'))
@click.option('--tuesday', '-tue', 'tue', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'update', 'tue'))
@click.option('--wednesday', '-wed', 'wed', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'update', 'wed'))
@click.option('--thursday', '-thu', 'thu', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'update', 'thu'))
@click.option('--friday', '-fri', 'fri', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'update', 'fri'))
@click.option('--saturday', '-sat', 'sat', default=None, required=False, type=click.BOOL, help=i18n.getHelpOption('schedules', 'update', 'sat'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def updateSchedule(id, name, description, status, start_time, end_time, interval, frequency, range_start, range_end, timezone, weekday, day_of_month, week_of_month, day_of_week, sun, mon, tue, wed, thu, fri, sat, debug, output, pretty=0):
    """Updates a schedule"""
    
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    # Validate the options
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))
    if ( sun is not None or mon is not None or tue is not None or wed is not None or thu is not None or fri is not None or sat is not None ) and interval not in ['Minutely', 'Hourly', 'Weekly', 'Biweekly']:
        raise click.BadParameter(i18n.getErrorText('schedules', 'update', 'day-missing'))
    if weekday is not None and interval != 'Daily':
        raise click.BadParameter(i18n.getErrorText('schedules', 'update', 'weekday-incorrect'))
    if ( day_of_month is not None  or day_of_week is not None or week_of_month is not None) and interval != 'Monthly':
        raise click.BadParameter(i18n.getErrorText('schedules', 'update', 'month-incorrect'))
    if frequency is not None and interval not in ['Minutely', 'Hourly', 'Daily']:
        raise click.BadParameter(i18n.getErrorText('schedules', 'update', 'frequency-incorrect'))
    if range_start is not None and interval not in ['Minutely', 'Hourly', 'Daily']:
        raise click.BadParameter(i18n.getErrorText('schedules', 'update', 'range-start-incorrect'))
    if range_end is not None and interval not in ['Minutely', 'Hourly', 'Daily']:
        raise click.BadParameter(i18n.getErrorText('schedules', 'update', 'range-end-incorrect'))
    if timezone is not None and day_of_month is None and week_of_month is None and day_of_week is None:
        raise click.BadParameter(i18n.getErrorText('schedules', 'update', 'timezone-incorrect'))

    result = api.updateSchedule(id=id, name=name, description=description, status=status, startTime=start_time, endTime=end_time, interval=interval, frequency=frequency, rangeStart=range_start, rangeEnd=range_end, timezone=timezone, weekday=weekday, dayOfMonth=day_of_month, weekOfMonth=week_of_month, dayOfWeek=day_of_week, sun=sun, mon=mon, tue=tue, wed=wed, thu=thu, fri=fri, sat=sat, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@schedules.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'delete', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'delete', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def deleteSchedule(id, name, debug, output, pretty=0):
    """Deletes a schedule"""
    
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    # Validate the options
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.deleteSchedule(id=id, name=name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@schedules.command('enable')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'enable', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'enable', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def enableSchedule(id, name, debug, output, pretty=0):
    """Enables a schedule"""
    
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    # Validate the options
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.updateSchedule(id=id, name=name, status='enabled', debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@schedules.command('disable')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'disable', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('schedules', 'disable', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def disableSchedule(id, name, debug, output, pretty=0):
    """Disables a schedule"""
    
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    # Validate the options
    if id is None and name is None:
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-name-missing'))

    result = api.updateSchedule(id=id, name=name, status='disabled', debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))


###################################
# Jobs commands section
###################################

@idmc.group('jobs')
def jobs():
    """Job management commands."""
    pass

@jobs.group('exp')
def jobsExp():
    """WARNING: Experimental unsupported job management commands."""
    pass

@jobsExp.command('get')
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'get', 'name'))
@click.option('--status', '-s', 'status', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'get', 'status'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'get', 'type'))
@click.option('--order-by', '-o', 'order_by', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'get', 'order-by'))
@click.option('--location', '-l', 'location', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'get', 'location'))
@click.option('--error', '-e', 'error_msg', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'get', 'error-msg'))
@click.option('--runtime', '-r', 'runtime', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'get', 'runtime'))
@click.option('--start-since', '-ss', 'start_since', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'get', 'start-since'))
@click.option('--start-until', '-su', 'start_until', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'get', 'start-until'))
@click.option('--end-since', '-es', 'end_since', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'get', 'end-since'))
@click.option('--end-until', '-eu', 'end_until', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'get', 'end-until'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getJobs(name, start_since, start_until, end_since, end_until, status, type, order_by, error_msg, location, runtime, debug, output, pretty=0):
    """Get job details from the monitor"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getMonitorJobs(type=type, name=name, status=status, errorMsg=error_msg, location=location, startSince=start_since, startUntil=start_until, endSince=end_since, endUntil=end_until, runtime=runtime, orderBy=order_by, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

@jobs.command('start')
@click.option('--ids', '-i', 'ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'start', 'ids'))
@click.option('--paths', '-p', 'paths', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'start', 'paths'))
@click.option('--type', '-t', 'type', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('jobs', 'start', 'type'))
@click.option('--callback', '-c', 'callback_url', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'start', 'callback'))
@click.option('--param-file', '-f', 'param_file', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'start', 'param-file'))
@click.option('--param-dir', '-d', 'param_dir', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'start', 'param-dir'))
@click.option('--api-names', '-a', 'api_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'start', 'api-names'))
@click.option('--wait', '-w', 'wait', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('jobs', 'start', 'wait'))
@click.option('--poll-delay', '-pd', 'poll_delay', default=3, required=False, type=click.INT, help=i18n.getHelpOption('jobs', 'start', 'poll-delay'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def startJobs(ids, paths, type, callback_url, param_file, param_dir, api_names, wait, poll_delay, debug, output, pretty=0):
    """Starts a job"""
    
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))
    
    # Validate the options
    if ids is None and paths is None and type != 'TASKFLOW':
        raise click.BadParameter(i18n.getErrorText('common', None, 'id-path-type-missing'))
    if (param_file and param_dir is None) or (param_file is None and param_dir):
        raise click.BadParameter(i18n.getErrorText('jobs', 'start', 'param-file-dir-missing'))
    if type == 'TASKFLOW' and api_names is None:
        raise click.BadParameter(i18n.getErrorText('jobs', 'start', 'api-name-missing'))
    
    if type in ['DMASK', 'DRS', 'DSS', 'MTT', 'PCS', 'WORKFLOW', 'TASKFLOW']:

        result = api.startCdiJobs(ids=ids, paths=paths, type=type, callbackUrl=callback_url, paramFile=param_file, paramDir=param_dir, apiNames=api_names, wait=wait, pollDelay=poll_delay, debug=debug)
        if output:
            write_output(output, pretty, result)
        else:
            click.echo(json.dumps(result, indent=pretty))

@jobs.command('stop')
@click.option('--ids', '-i', 'ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'stop', 'ids'))
@click.option('--names', '-n', 'names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'stop', 'names'))
@click.option('--locations', '-l', 'locations', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'stop', 'locations'))
@click.option('--types', '-t', 'types', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('jobs', 'stop', 'types'))
@click.option('--clean', '-c', 'clean', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('jobs', 'stop', 'clean'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def stopJobs(ids, names, locations, types, clean, debug, output, pretty=0):
    """Stops running jobs"""
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.stopCdiJobs(ids=ids, names=names, locations=locations, types=types, clean=clean, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

###################################
# Organisations commands section
###################################

@idmc.group('orgs')
def orgs():
    """Organisation management commands."""
    pass

@orgs.command('get')
@click.option('--suborg-id', '-i', 'sub_id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('orgs', 'get', 'sub-id'))
@click.option('--suborg-name', '-n', 'sub_name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('orgs', 'get', 'sub-name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getOrgs(sub_id, sub_name, debug, output, pretty=0):
    """Get organisation and sub-organisation details"""
    
    if output and Path(output).suffix not in out_types:
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    result = api.getOrg(subId=sub_id, subName=sub_name, debug=debug)
    if output:
        write_output(output, pretty, result)
    else:
        click.echo(json.dumps(result, indent=pretty))

###################################
# Export / Import commands section
###################################

@idmc.command('export')
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('export', None, 'name'))
@click.option('--ids', '-i', 'ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('export', None, 'ids'))
@click.option('--paths', '-p', 'paths', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('export', None, 'paths'))
@click.option('--types', '-t', 'types', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('export', None, 'types'))
@click.option('--include-dependencies', '-d', 'dependencies', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('export', None, 'dependencies'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
@click.option('--output', '-O', 'output', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('common', None, 'output'))
def getOrgs(name, ids, paths, types, dependencies, debug, output, pretty=0):
    """Used to export IDMC objects to a zip file"""
    
    if output and Path(output).suffix != '.zip':
        raise click.BadParameter(i18n.getErrorText('common', None, 'bad-file-type'))

    #result = api.startExport(ids=ids, name=name, paths=paths, types=types, dependencies=dependencies, debug=debug)
    # TODO running status = IN_PROGRESS
    #result = api.getExportStatus(id=ids, expand=True, debug=debug)
    result = api.downloadExport(id=ids, output=output, debug=debug)
    if output:
        #write_output(output, pretty, result)
        with open(output, 'wb') as file:
            file.write(result)
    else:
        click.echo(json.dumps(result, indent=pretty))

if __name__ == '__main__':
    idmc()
