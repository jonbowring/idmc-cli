import click
import json
from idmc_cli.config import config
from idmc_cli.i18n import i18n
from idmc_cli.api import api

@click.group()
def main():
    """Informatica Cloud CLI Utility"""
    pass

###################################
# Admin commands section
###################################

@main.command('configure')
def configure():
    """Used to configure the global parameters for the CLI."""

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



@main.command('login')
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def login(debug, pretty=0):
    """Used to login to Informatica Cloud and return the login details."""
    click.echo(json.dumps(api.login(debug=debug), indent=pretty))

###################################
# User commands section
###################################

@main.group('users')
def users():
    """User management commands."""
    pass

@users.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'get', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'get', 'username'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getUsers(id, username, debug, pretty=0):
    """Returns users"""
    click.echo(json.dumps(api.getUsers(id=id, username=username, debug=debug), indent=pretty))


@users.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'delete', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'delete', 'username'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def deleteUser(id, username, debug, pretty=0):
    """Deletes a user"""
    click.echo(json.dumps(api.deleteUser(id=id, username=username, debug=debug), indent=pretty))
    

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
def createUser(name, first_name, last_name, email, password, description, title, phone, force_password_change, max_login_attempts, authentication, alias_name, role_ids, role_names, group_ids, group_names, debug, pretty=0):
    """Used to create new users"""
    click.echo(json.dumps(api.createUser(name=name, firstName=first_name, lastName=last_name, email=email, password=password, description=description, title=title, phone=phone, forcePasswordChange=force_password_change, maxLoginAttempts=max_login_attempts, authentication=authentication, aliasName=alias_name, roleIds=role_ids, roleNames=role_names, groupIds=group_ids, groupNames=group_names, debug=debug), indent=pretty))
    

@users.command('add-roles')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-roles', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-roles', 'username'))
@click.option('--role-ids', '-ri', 'role_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-roles', 'role_ids'))
@click.option('--role-names', '-rn', 'role_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-roles', 'role_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def addUserRoles(id, username, roleIds, roleNames, debug, pretty=0):
    """Adds role assignments to a user"""
    click.echo(json.dumps(api.addUserRoles(id=id, username=username, roleIds=roleIds, roleNames=roleNames, debug=debug), indent=pretty))


@users.command('remove-roles')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-roles', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-roles', 'username'))
@click.option('--role-ids', '-ri', 'role_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-roles', 'role_ids'))
@click.option('--role-names', '-rn', 'role_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-roles', 'role_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def removeUserRoles(id, username, role_ids, role_names, debug, pretty=0):
    """Removes role assignments from a user"""
    click.echo(json.dumps(api.removeUserRoles(id=id, username=username, roleIds=role_ids, roleNames=role_names, debug=debug), indent=pretty))


@users.command('add-groups')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-groups', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-groups', 'username'))
@click.option('--group-ids', '-gi', 'group_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-groups', 'group_ids'))
@click.option('--group-names', '-gn', 'group_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'add-groups', 'group_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def addUserGroups(id, username, group_ids, group_names, debug, pretty=0):
    """Adds group assignments to a user"""
    click.echo(json.dumps(api.addUserGroups(id=id, username=username, groupIds=group_ids, groupNames=group_names, debug=debug), indent=pretty))


@users.command('remove-groups')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-groups', 'id'))
@click.option('--username', '-u', 'username', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-groups', 'username'))
@click.option('--group-ids', '-gi', 'group_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-groups', 'group_ids'))
@click.option('--group-names', '-gn', 'group_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('users', 'remove-groups', 'group_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def removeUserGroups(id, username, group_ids, group_names, debug, pretty=0):
    """Removes group assignments from a user"""
    click.echo(json.dumps(api.removeUserGroups(id=id, username=username, groupIds=group_ids, groupNames=group_names, debug=debug), indent=pretty))
    

###################################
# User Groups commands section
###################################

@main.group('user-groups')
def userGroups():
    """User group management commands."""
    pass

@userGroups.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'get', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'get', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getUserGroups(id, name, debug, pretty=0):
    """Returns user groups"""
    click.echo(json.dumps(api.getUserGroups(id=id, name=name, debug=debug), indent=pretty))


@userGroups.command('create')
@click.option('--name', '-n', 'name', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'description'))
@click.option('--role-ids', '-ri', 'role_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'role_ids'))
@click.option('--role-names', '-rn', 'role_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'role_names'))
@click.option('--user-ids', '-ui', 'user_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'user_ids'))
@click.option('--user-names', '-un', 'user_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'create', 'user_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def createUserGroup(name, description, role_ids, role_names, user_ids, user_names, debug, pretty=0):
    """Creates a new user group"""
    click.echo(json.dumps(api.createUserGroup(name=name, description=description, roleIds=role_ids, roleNames=role_names, userIds=user_ids, userNames=user_names, debug=debug), indent=pretty))


@userGroups.command('add-roles')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'add-roles', 'id'))
@click.option('--group-name', '-gn', 'group_name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'add-roles', 'group_name'))
@click.option('--role-ids', '-ri', 'role_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'add-roles', 'role_ids'))
@click.option('--role-names', '-rn', 'role_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'add-roles', 'role_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def addUserGroupRoles(id, group_name, role_ids, role_names, debug, pretty=0):
    """Adds role assignments to a user group"""
    click.echo(json.dumps(api.addUserGroupRoles(id=id, groupname=group_name, roleIds=role_ids, roleNames=role_names, debug=debug), indent=pretty))


@userGroups.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'delete', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('user-groups', 'delete', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def deleteUserGroup(id, name, debug, pretty=0):
    """Deletes a user group"""
    click.echo(json.dumps(api.deleteUserGroup(id=id, name=name, debug=debug), indent=pretty))
    

###################################
# Role commands section
###################################

@main.group('roles')
def roles():
    """Role management commands."""
    pass

@roles.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'get', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'get', 'name'))
@click.option('--expand', '-e', 'expand', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('roles', 'get', 'expand'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getRoles(id, name, expand, debug, pretty=0):
    """Returns roles"""
    click.echo(json.dumps(api.getRoles(id=id, name=name, expand=expand, debug=debug), indent=pretty))

@roles.command('create')
@click.option('--name', '-n', 'name', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('roles', 'create', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'create', 'description'))
@click.option('--privilege-ids', '-pi', 'privilege_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'create', 'privilege_ids'))
@click.option('--privilege-names', '-pn', 'privilege_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'create', 'privilege_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def createRole(name, description, privilege_ids, privilege_names, debug, pretty=0):
    """Creates a new role"""
    click.echo(json.dumps(api.createRole(name=name, description=description, privilegeIds=privilege_ids, privilegeNames=privilege_names, debug=debug), indent=pretty))

@roles.command('add-privileges')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'add-privileges', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'add-privileges', 'name'))
@click.option('--privilege-ids', '-pi', 'privilege_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'add-privileges', 'privilege_ids'))
@click.option('--privilege-names', '-pn', 'privilege_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'add-privileges', 'privilege_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def addRolePrivileges(id, name, privilege_ids, privilege_names, debug, pretty=0):
    """Adds privilege assignments to a role"""
    click.echo(json.dumps(api.addRolePrivileges(id=id, name=name, privilegeIds=privilege_ids, privilegeNames=privilege_names, debug=debug), indent=pretty))


@roles.command('remove-privileges')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'remove-privileges', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'remove-privileges', 'name'))
@click.option('--privilege-ids', '-pi', 'privilege_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'remove-privileges', 'privilege_ids'))
@click.option('--privilege-names', '-pn', 'privilege_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'remove-privileges', 'privilege_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def removeRolePrivileges(id, name, privilege_ids, privilege_names, debug, pretty=0):
    """Remove privilege assignments from a role"""
    click.echo(json.dumps(api.removeRolePrivileges(id=id, name=name, privilegeIds=privilege_ids, privilegeNames=privilege_names, debug=debug), indent=pretty))


@roles.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'delete', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('roles', 'delete', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def deleteRole(id, name, debug, pretty=0):
    """Deletes a role"""
    click.echo(json.dumps(api.deleteRole(id=id, name=name, debug=debug), indent=pretty))



###################################
# Privileges commands section
###################################

@main.group('privileges')
def privileges():
    """Privilege management commands."""
    pass

@privileges.command('get')
@click.option('--all', 'all', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('privileges', 'get', 'all'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getPrivileges(all, debug, pretty=0):
    """Returns privileges"""
    click.echo(json.dumps(api.getPrivileges(all=all, debug=debug), indent=pretty))

###################################
# Lookup commands section
###################################

@main.group('lookup')
def lookup():
    """Lookup objects."""
    pass

@lookup.command('object')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('lookup', 'object', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('lookup', 'object', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('lookup', 'object', 'type'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def lookupObject(id, path, type, debug, pretty=0):
    """Lookup a single object"""
    click.echo(json.dumps(api.lookupObject(id=id, path=path, type=type, debug=debug), indent=pretty))

@lookup.command('objects')
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('lookup', 'objects', 'body'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def lookupObjects(body, debug, pretty=0):
    """Lookup multiple objects"""
    click.echo(json.dumps(api.lookupObjects(body=body, debug=debug), indent=pretty))

###################################
# Object commands section
###################################

@main.group('objects')
def objects():
    """Object management commands."""
    pass

@objects.command('add-tags')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'add-tags', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'add-tags', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'add-tags', 'type'))
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'add-tags', 'body'))
@click.option('--tags', '-T', 'tags', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'add-tags', 'tags'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def tagObject(id, path, type, body, tags, debug, pretty=0):
    """Adds one or more tags to an object"""
    if body:
        click.echo(json.dumps(api.tagObjects(body=body, debug=debug), indent=pretty))
    else:
        click.echo(json.dumps(api.tagObject(id=id, path=path, type=type, tags=tags, debug=debug), indent=pretty))


@objects.command('remove-tags')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'remove-tags', 'id'))
@click.option('--path', '-p' 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'remove-tags', 'path'))
@click.option('--type', '-t' 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'remove-tags', 'type'))
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'remove-tags', 'body'))
@click.option('--tags', '-T', 'tags', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('objects', 'remove-tags', 'tags'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def tagObject(id, path, type, body, tags, debug, pretty=0):
    """Removes one or more tags from an object"""
    if body:
        click.echo(json.dumps(api.untagObjects(body=body, debug=debug), indent=pretty))
    else:
        click.echo(json.dumps(api.untagObject(id=id, path=path, type=type, tags=tags, debug=debug), indent=pretty))


###################################
# Project commands section
###################################

@main.group('projects')
def projects():
    """Project management commands."""
    pass

@projects.command('create')
@click.option('--name', '-n', 'name', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('projects', 'create', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'create', 'description'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def createProject(name, description, debug, pretty=0):
    """Creates a project"""
    click.echo(json.dumps(api.createProject(name=name, description=description, debug=debug), indent=pretty))

@projects.command('update')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'update', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'update', 'path'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'update', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'update', 'description'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def createProject(id, name, path, description, debug, pretty=0):
    """Updates a project"""
    click.echo(json.dumps(api.updateProject(id=id, path=path, name=name, description=description, debug=debug), indent=pretty))

@projects.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'delete', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('projects', 'delete', 'path'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def deleteProject(id, path, debug, pretty=0):
    """Deletes a project"""
    click.echo(json.dumps(api.deleteProject(id=id, path=path, debug=debug), indent=pretty))

###################################
# Folder commands section
###################################

@main.group('folders')
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
def createFolder(project_id, project_name, name, description, debug, pretty=0):
    """Creates a folder"""
    click.echo(json.dumps(api.createFolder(projectId=project_id, projectName=project_name, name=name, description=description, debug=debug), indent=pretty))

@folders.command('update')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'update', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'update', 'path'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'update', 'name'))
@click.option('--description', '-d', 'description', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'update', 'description'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def createProject(id, name, path, description, debug, pretty=0):
    """Updates a folder"""
    click.echo(json.dumps(api.updateFolder(id=id, path=path, name=name, description=description, debug=debug), indent=pretty))

@folders.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'delete', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('folders', 'delete', 'path'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def deleteFolder(id, path, debug, pretty=0):
    """Deletes a folder"""
    click.echo(json.dumps(api.deleteFolder(id=id, path=path, debug=debug), indent=pretty))


###################################
# Source control commands section
###################################

@main.group('source-control')
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
def checkInObject(summary, description, id, path, type, include_container, body, debug, pretty=0):
    """Checks in one or more objects"""
    if body:
        click.echo(json.dumps(api.checkInObjects(summary=summary, description=description, body=body, debug=debug), indent=pretty))
    else:
        click.echo(json.dumps(api.checkInObject(summary=summary, description=description, id=id, path=path, type=type, includeContainer=include_container, debug=debug), indent=pretty))

@sourceControl.command('check-out')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-out', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-out', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-out', 'type'))
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'check-out', 'body'))
@click.option('--include-container', '-I', 'include_container', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'check-out', 'include_container'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def checkOutObject(id, path, type, include_container, body, debug, pretty=0):
    """Checks out one or more objects"""
    if body:
        click.echo(json.dumps(api.checkOutObjects(body=body, debug=debug), indent=pretty))
    else:
        click.echo(json.dumps(api.checkOutObject(id=id, path=path, type=type, includeContainer=include_container, debug=debug), indent=pretty))

@sourceControl.command('undo-check-out')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'undo-check-out', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'undo-check-out', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'undo-check-out', 'type'))
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'undo-check-out', 'body'))
@click.option('--include-container', '-I', 'include_container', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'undo-check-out', 'include_container'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def undoCheckOutObject(id, path, type, include_container, body, debug, pretty=0):
    """Undo check out for one or more objects"""
    if body:
        click.echo(json.dumps(api.undoCheckOutObjects(body=body, debug=debug), indent=pretty))
    else:
        click.echo(json.dumps(api.undoCheckOutObject(id=id, path=path, type=type, includeContainer=include_container, debug=debug), indent=pretty))

@sourceControl.command('pull')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull', 'type'))
@click.option('--hash', '-h', 'hash', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull', 'hash'))
@click.option('--relax-validation', '-r', 'relax_validation', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'pull', 'relax_validation'))
@click.option('--body', '-b', 'body', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull', 'body'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def pullObjects(id, path, type, hash, relax_validation, body, debug, pretty=0):
    """Pulls one or more objects"""
    if body:
        click.echo(json.dumps(api.pullObjects(body=body, hash=hash, relaxValidation=relax_validation, debug=debug), indent=pretty))
    else:
        click.echo(json.dumps(api.pullObject(id=id, path=path, type=type, hash=hash, relaxValidation=relax_validation, debug=debug), indent=pretty))

@sourceControl.command('pull-commit-hash')
@click.option('--hash', '-h', 'hash', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull-commit-hash', 'hash'))
@click.option('--search', '-s', 'search', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'pull-commit-hash', 'search'))
@click.option('--repo-id', '-ri', 'repo_id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'pull-commit-hash', 'repo_id'))
@click.option('--relax-validation', '-r', 'relax_validation', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'pull-commit-hash', 'relax_validation'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def checkOutObject(hash, search, repo_id, relax_validation, debug, pretty=0):
    """Pulls all objects in a commit hash"""
    click.echo(json.dumps(api.pullByCommitHash(hash=hash, search=search, repoId=repo_id, relaxValidation=relax_validation, debug=debug), indent=pretty))

@sourceControl.command('status')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'status', 'id'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getSourceStatus(id, debug, pretty=0):
    """Gets the status of a source control action"""
    click.echo(json.dumps(api.getSourceStatus(id=id, debug=debug), indent=pretty))

@sourceControl.command('repo-details')
@click.option('--project-ids', '-i', 'project_ids', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'repo-details', 'project_ids'))
@click.option('--project-names', '-n', 'project_names', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'repo-details', 'project_names'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getSourceStatus(project_ids, project_names, debug, pretty=0):
    """Gets the source control repository details"""
    click.echo(json.dumps(api.getRepoConnection(projectIds=project_ids, projectNames=project_names, debug=debug), indent=pretty))

@sourceControl.command('commit-history')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-history', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-history', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-history', 'type'))
@click.option('--branch', '-b', 'branch', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-history', 'branch'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getCommitHistory(id, path, type, branch, debug, pretty=0):
    """Gets the commit history for an asset"""
    click.echo(json.dumps(api.getCommitHistory(id=id, path=path, type=type, branch=branch, debug=debug), indent=pretty))

@sourceControl.command('commit-details')
@click.option('--hash', '-h', 'hash', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-details', 'hash'))
@click.option('--search-all', '-s', 'search_all', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('source-control', 'commit-details', 'search_all'))
@click.option('--repo-id', '-r', 'repo_id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-details', 'repo_id'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getCommitDetails(hash, search_all, repo_id, debug, pretty=0):
    """Gets the details for a commit"""
    click.echo(json.dumps(api.getCommitDetails(hash=hash, searchAllRepos=search_all, repoId=repo_id, debug=debug), indent=pretty))

@sourceControl.command('compare-versions')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'commit-history', 'id'))
@click.option('--path', '-p', 'path', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'compare-versions', 'path'))
@click.option('--type', '-t', 'type', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'compare-versions', 'type'))
@click.option('--old-version', '-o', 'old_version', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'compare-versions', 'old_version'))
@click.option('--new-version', '-n', 'new_version', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'compare-versions', 'new_version'))
@click.option('--format', '-f', 'format', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('source-control', 'compare-versions', 'format'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def compareVersions(id, path, type, old_version, new_version, format, debug, pretty=0):
    """Used to compare two versions of an asset."""
    if format == 'JSON':
        click.echo(json.dumps(api.compareVersions(id=id, path=path, type=type, oldVersion=old_version, newVersion=new_version, format=format, debug=debug), indent=pretty))
    else:
        click.echo(api.compareVersions(id=id, path=path, type=type, oldVersion=old_version, newVersion=new_version, format=format, debug=debug))

###################################
# Log commands section
###################################

@main.group('logs')
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
def getSecurityLogs(category, actor, name, time_from, time_to, debug, pretty=0):
    """Gets the security logs"""
    click.echo(json.dumps(api.getSecurityLogs(category=category, actor=actor, name=name, time_from=time_from, time_to=time_to, debug=debug), indent=pretty))

###################################
# Secure agent commands section
###################################

@main.group('agents')
def agents():
    """Secure Agent management commands."""
    pass

@agents.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'get', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'get', 'name'))
@click.option('--unassigned', '-u', 'unassigned', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('agents', 'get', 'unassigned'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getAgents(id, name, unassigned, debug, pretty=0):
    """Gets Secure Agents"""
    click.echo(json.dumps(api.getAgents(id=id, name=name, unassigned=unassigned, debug=debug), indent=pretty))

@agents.command('delete')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'delete', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'delete', 'name'))
@click.option('--unassigned', '-u', 'unassigned', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('agents', 'delete', 'unassigned'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def deleteAgent(id, name, unassigned, debug, pretty=0):
    """Deletes a secure agent"""
    click.echo(json.dumps(api.deleteAgent(id=id, name=name, unassigned=unassigned, debug=debug), indent=pretty))

@agents.command('status')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'status', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agents', 'status', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getAgentStatus(id, name, debug, pretty=0):
    """Gets Secure Agent Status"""
    click.echo(json.dumps(api.getAgentStatus(id=id, name=name, debug=debug), indent=pretty))

@agents.group('groups')
def agentGroup():
    """Secure Agent Group service management commands."""
    pass

@agentGroup.command('get')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'get', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('agentGroup', 'get', 'name'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getAgents(id, name, debug, pretty=0):
    """Gets Secure Agent Groups"""
    click.echo(json.dumps(api.getAgentGroups(id=id, name=name, debug=debug), indent=pretty))

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
def getAgents(id, name, service, debug, pretty=0):
    """Stops a service on a secure agent"""
    click.echo(json.dumps(api.execAgentService(id=id, name=name, service=service, action='stop', debug=debug), indent=pretty))

@service.command('start')
@click.option('--id', '-i', 'id', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('services', 'start', 'id'))
@click.option('--name', '-n', 'name', default=None, required=False, type=click.STRING, help=i18n.getHelpOption('services', 'start', 'name'))
@click.option('--service', '-s', 'service', default=None, required=True, type=click.STRING, help=i18n.getHelpOption('services', 'start', 'service'))
@click.option('--debug', '-D', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help=i18n.getHelpOption('common', None, 'debug'))
@click.option('--pretty', '-P', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help=i18n.getHelpOption('common', None, 'pretty'))
def getAgents(id, name, service, debug, pretty=0):
    """Starts a service on a secure agent"""
    click.echo(json.dumps(api.execAgentService(id=id, name=name, service=service, action='start', debug=debug), indent=pretty))
        

if __name__ == '__main__':
    main()
