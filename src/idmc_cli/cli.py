import click
import json
from idmc_cli.config import config
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
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
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
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='(Optional) Filter by user id. Use this option or the --username option.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='(Optional) Filter by user name. Use this option or the --id option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def getUsers(id, username, debug, pretty=0):
    """Returns users"""
    click.echo(json.dumps(api.getUsers(id=id, username=username, debug=debug), indent=pretty))


@users.command('delete')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='User id to be deleted. Use this option or the --username option.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='User name to be deleted. Use this option or the --id option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def deleteUser(id, username, debug, pretty=0):
    """Deletes a user"""
    click.echo(json.dumps(api.deleteUser(id=id, username=username, debug=debug), indent=pretty))
    

@users.command('create')
@click.option('--name', 'name', default=None, required=True, type=click.STRING, help='Informatica Intelligent Cloud Services user name.')
@click.option('--firstName', 'firstName', default=None, required=True, type=click.STRING, help='First name for the user account.')
@click.option('--lastName', 'lastName', default=None, required=True, type=click.STRING, help='Last name for the user account.')
@click.option('--password', 'password', default=None, required=False, type=click.STRING, help='(Optional) Informatica Intelligent Cloud Services password. If password is empty, the user receives an activation email. Maximum length is 255 characters.')
@click.option('--description', 'description', default=None, required=False, type=click.STRING, help='(Optional) Description of the user.')
@click.option('--email', 'email', default=None, required=True, type=click.STRING, help='Email address for the user.')
@click.option('--title', 'title', default=None, required=False, type=click.STRING, help='(Optional) Job title of the user.')
@click.option('--phone', 'phone', default=None, required=False, type=click.STRING, help='(Optional) Phone number for the user.')
@click.option('--forcePasswordChange', 'forcePasswordChange', default=True, required=False, type=click.BOOL, help='(Optional) Determines whether the user must reset the password after the user logs in for the first time.')
@click.option('--maxLoginAttempts', 'maxLoginAttempts', default=None, required=False, type=click.INT, help='(Optional) Number of times a user can attempt to log in before the account is locked.')
@click.option('--authentication', 'authentication', default=None, required=False, type=click.INT, help='(Optional) Determines whether the user accesses Informatica Intelligent Cloud Services through single sign-in (SAML). Use one of the following values: 0 (Native), 1 (SAML).')
@click.option('--aliasName', 'aliasName', default=None, required=False, type=click.STRING, help='(Optional) Required when authentication is not 0. The user identifier or user name in the 3rd party system.')
@click.option('--roleIds', 'roleIds', default=None, required=False, type=click.STRING, help='(Optional) Required when no group IDs are included. Comma separated list of IDs for the roles to assign to the user.')
@click.option('--roleNames', 'roleNames', default=None, required=False, type=click.STRING, help='(Optional) Required when no group IDs are included. Comma separated list of Names for the roles to assign to the user.')
@click.option('--groupIds', 'groupIds', default=None, required=False, type=click.STRING, help='(Optional) Required when no role IDs are included. Comma separated list of IDs for the user groups to assign to the user.')
@click.option('--groupNames', 'groupNames', default=None, required=False, type=click.STRING, help='(Optional) Required when no role IDs are included. Comma separated list of Names for the user groups to assign to the user.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def createUser(name, firstName, lastName, email, password, description, title, phone, forcePasswordChange, maxLoginAttempts, authentication, aliasName, roleIds, roleNames, groupIds, groupNames, debug, pretty=0):
    """Used to create new users"""
    click.echo(json.dumps(api.createUser(name=name, firstName=firstName, lastName=lastName, email=email, password=password, description=description, title=title, phone=phone, forcePasswordChange=forcePasswordChange, maxLoginAttempts=maxLoginAttempts, authentication=authentication, aliasName=aliasName, roleIds=roleIds, roleNames=roleNames, groupIds=groupIds, groupNames=groupNames, debug=debug), indent=pretty))
    

@users.command('addRoles')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --username.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --id.')
@click.option('--roleIds', 'roleIds', default=None, required=False, type=click.STRING, help='Comma separated list of role ids to be added to user. Must specify this option or --roleNames.')
@click.option('--roleNames', 'roleNames', default=None, required=False, type=click.STRING, help='Comma separated list of role names to be added to user. Must specify this option or --roleIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def addUserRoles(id, username, roleIds, roleNames, debug, pretty=0):
    """Adds role assignments to a user"""
    click.echo(json.dumps(api.addUserRoles(id=id, username=username, roleIds=roleIds, roleNames=roleNames, debug=debug), indent=pretty))


@users.command('removeRoles')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --username.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --id.')
@click.option('--roleIds', 'roleIds', default=None, required=False, type=click.STRING, help='Comma separated list of role ids to be added to user. Must specify this option or --roleNames.')
@click.option('--roleNames', 'roleNames', default=None, required=False, type=click.STRING, help='Comma separated list of role names to be added to user. Must specify this option or --roleIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def removeUserRoles(id, username, roleIds, roleNames, debug, pretty=0):
    """Removes role assignments from a user"""
    click.echo(json.dumps(api.removeUserRoles(id=id, username=username, roleIds=roleIds, roleNames=roleNames, debug=debug), indent=pretty))


@users.command('addGroups')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --username.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --id.')
@click.option('--groupIds', 'groupIds', default=None, required=False, type=click.STRING, help='Comma separated list of group ids to be added to user. Must specify this option or --groupNames.')
@click.option('--groupNames', 'groupNames', default=None, required=False, type=click.STRING, help='Comma separated list of group names to be added to user. Must specify this option or --groupIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def addUserGroups(id, username, groupIds, groupNames, debug, pretty=0):
    """Adds group assignments to a user"""
    click.echo(json.dumps(api.addUserGroups(id=id, username=username, groupIds=groupIds, groupNames=groupNames, debug=debug), indent=pretty))


@users.command('removeGroups')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --username.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --id.')
@click.option('--groupIds', 'groupIds', default=None, required=False, type=click.STRING, help='Comma separated list of group ids to be added to user. Must specify this option or --groupNames.')
@click.option('--groupNames', 'groupNames', default=None, required=False, type=click.STRING, help='Comma separated list of group names to be added to user. Must specify this option or --groupIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def removeUserGroups(id, username, groupIds, groupNames, debug, pretty=0):
    """Removes group assignments from a user"""
    click.echo(json.dumps(api.removeUserGroups(id=id, username=username, groupIds=groupIds, groupNames=groupNames, debug=debug), indent=pretty))
    

###################################
# User Groups commands section
###################################

@main.group('userGroups')
def userGroups():
    """User group management commands."""
    pass

@userGroups.command('get')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='(Optional) Filter by user group id. Use this option or the --username option.')
@click.option('--name', 'name', default=None, required=False, type=click.STRING, help='(Optional) Filter by user group name. Use this option or the --id option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def getUserGroups(id, name, debug, pretty=0):
    """Returns user groups"""
    click.echo(json.dumps(api.getUserGroups(id=id, name=name, debug=debug), indent=pretty))


@userGroups.command('create')
@click.option('--name', 'name', default=None, required=True, type=click.STRING, help='Name of the new user group.')
@click.option('--description', 'description', default=None, required=False, type=click.STRING, help='Description of the new user group.')
@click.option('--roleIds', 'roleIds', default=None, required=False, type=click.STRING, help='Comma separated list of role ids to be added to the new user group. Either this or the --roleNames group is required.')
@click.option('--roleNames', 'roleNames', default=None, required=False, type=click.STRING, help='Comma separated list of role names to be added to the new user group. Either this or the --roleIds group is required.')
@click.option('--userIds', 'userIds', default=None, required=False, type=click.STRING, help='Comma separated list of user ids to be added to the new user group.  Use this option or the --userNames option.')
@click.option('--userNames', 'userNames', default=None, required=False, type=click.STRING, help='Comma separated list of user names to be added to the new user group. Use this option or the --userIds option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def createUserGroup(name, description, roleIds, roleNames, userIds, userNames, debug, pretty=0):
    """Creates a new user group"""
    click.echo(json.dumps(api.createUserGroup(name=name, description=description, roleIds=roleIds, roleNames=roleNames, userIds=userIds, userNames=userNames, debug=debug), indent=pretty))


@userGroups.command('addRoles')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --groupname.')
@click.option('--groupname', 'groupname', default=None, required=False, type=click.STRING, help='ID of user group to be updated. Must specify this option or --id.')
@click.option('--roleIds', 'roleIds', default=None, required=False, type=click.STRING, help='Comma separated list of role ids to be added to user. Must specify this option or --roleNames.')
@click.option('--roleNames', 'roleNames', default=None, required=False, type=click.STRING, help='Comma separated list of role names to be added to user. Must specify this option or --roleIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def addUserGroupRoles(id, groupname, roleIds, roleNames, debug, pretty=0):
    """Adds role assignments to a user group"""
    click.echo(json.dumps(api.addUserGroupRoles(id=id, groupname=groupname, roleIds=roleIds, roleNames=roleNames, debug=debug), indent=pretty))


@userGroups.command('delete')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='User group id to be deleted. Use this option or the --name option.')
@click.option('--name', 'name', default=None, required=False, type=click.STRING, help='User group name to be deleted. Use this option or the --id option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
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
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='Filter by role id.')
@click.option('--name', 'name', default=None, required=False, type=click.STRING, help='Filter by role name.')
@click.option('--expand', 'expand', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='Expand role privileges.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def getRoles(id, name, expand, debug, pretty=0):
    """Returns roles"""
    click.echo(json.dumps(api.getRoles(id=id, name=name, expand=expand, debug=debug), indent=pretty))

@roles.command('create')
@click.option('--name', 'name', default=None, required=True, type=click.STRING, help='Filter by role name.')
@click.option('--description', 'description', default=None, required=False, type=click.STRING, help='Description of the new role.')
@click.option('--privilegeIds', 'privilegeIds', default=None, required=False, type=click.STRING, help='Comma separated list of privilege IDs for the new role. Must include this option or the --privilegeNames option.')
@click.option('--privilegeNames', 'privilegeNames', default=None, required=False, type=click.STRING, help='Comma separated list of privilege names for the new role. Must include this option or the --privilegeIds option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def createRole(name, description, privilegeIds, privilegeNames, debug, pretty=0):
    """Creates a new role"""
    click.echo(json.dumps(api.createRole(name=name, description=description, privilegeIds=privilegeIds, privilegeNames=privilegeNames, debug=debug), indent=pretty))

@roles.command('addRolePrivileges')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of role to be updated. Must specify this option or --name.')
@click.option('--name', 'name', default=None, required=False, type=click.STRING, help='Name of role to be updated. Must specify this option or --id.')
@click.option('--privilegeIds', 'privilegeIds', default=None, required=False, type=click.STRING, help='Comma separated list of role ids to be added to user. Must specify this option or --privilegeNames.')
@click.option('--privilegeNames', 'privilegeNames', default=None, required=False, type=click.STRING, help='Comma separated list of role names to be added to user. Must specify this option or --privilegeIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def addRolePrivileges(id, name, privilegeIds, privilegeNames, debug, pretty=0):
    """Adds privilege assignments to a role"""
    click.echo(json.dumps(api.addRolePrivileges(id=id, name=name, privilegeIds=privilegeIds, privilegeNames=privilegeNames, debug=debug), indent=pretty))


@roles.command('removeRolePrivileges')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of role to be updated. Must specify this option or --name.')
@click.option('--name', 'name', default=None, required=False, type=click.STRING, help='Name of role to be updated. Must specify this option or --id.')
@click.option('--privilegeIds', 'privilegeIds', default=None, required=False, type=click.STRING, help='Comma separated list of role ids to be added to user. Must specify this option or --privilegeNames.')
@click.option('--privilegeNames', 'privilegeNames', default=None, required=False, type=click.STRING, help='Comma separated list of role names to be added to user. Must specify this option or --privilegeIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def removeRolePrivileges(id, name, privilegeIds, privilegeNames, debug, pretty=0):
    """Remove privilege assignments from a role"""
    click.echo(json.dumps(api.removeRolePrivileges(id=id, name=name, privilegeIds=privilegeIds, privilegeNames=privilegeNames, debug=debug), indent=pretty))


@roles.command('delete')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='Role id to be deleted. Use this option or the --name option.')
@click.option('--name', 'name', default=None, required=False, type=click.STRING, help='Role name to be deleted. Use this option or the --id option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
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
@click.option('--all', 'all', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If included will return a full list of privileges, even those that are disabled or unassigned.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=4, required=False, type=click.INT, is_flag=True, help='If true, will pretty print the returned JSON.')
def getPrivileges(all, debug, pretty=0):
    """Returns roles"""
    click.echo(json.dumps(api.getPrivileges(all=all, debug=debug), indent=pretty))


if __name__ == '__main__':
    main()
