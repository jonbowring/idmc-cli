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



@main.command('login')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def login(debug, pretty):
    """Used to login to Informatica Cloud and return the login details."""
    if pretty:
        click.echo(json.dumps(api.login(debug), indent=4))
    else:    
        click.echo(json.dumps(api.login(debug)))

###################################
# User commands section
###################################

@main.group()
def users():
    """User management commands."""
    pass

@users.command('get')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='(Optional) Filter by user id. Use this option or the --username option.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='(Optional) Filter by user name. Use this option or the --id option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def getUsers(id, username, debug, pretty):
    """Returns users"""
    if pretty:
        click.echo(json.dumps(api.getUsers(id, username, debug), indent=4))
    else:    
        click.echo(json.dumps(api.getUsers(id, username, debug)))


@users.command('delete')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='User id to be deleted. Use this option or the --username option.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='User name to be deleted. Use this option or the --id option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def deleteUser(id, username, debug, pretty):
    """Deletes a user"""
    if pretty:
        click.echo(json.dumps(api.deleteUser(id, username, debug), indent=4))
    else:    
        click.echo(json.dumps(api.deleteUser(id, username, debug)))
    

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
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def createUser(name, firstName, lastName, email, password, description, title, phone, forcePasswordChange, maxLoginAttempts, authentication, aliasName, roleIds, roleNames, groupIds, groupNames, debug, pretty):
    """Used to create new users"""
    if pretty:
        click.echo(json.dumps(api.createUser(name, firstName, lastName, email, password, description, title, phone, forcePasswordChange, maxLoginAttempts, authentication, aliasName, roleIds, roleNames, groupIds, groupNames, debug), indent=4))
    else:    
        click.echo(json.dumps(api.createUser(name, firstName, lastName, email, password, description, title, phone, forcePasswordChange, maxLoginAttempts, authentication, aliasName, roleIds, roleNames, groupIds, groupNames, debug)))
    

@users.command('addRoles')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --username.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --id.')
@click.option('--roleIds', 'roleIds', default=None, required=False, type=click.STRING, help='Comma separated list of role ids to be added to user. Must specify this option or --roleNames.')
@click.option('--roleNames', 'roleNames', default=None, required=False, type=click.STRING, help='Comma separated list of role names to be added to user. Must specify this option or --roleIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def addUserRoles(id, username, roleIds, roleNames, debug, pretty):
    """Adds role assignments to a user"""
    if pretty:
        click.echo(json.dumps(api.addUserRoles(id, username, roleIds, roleNames, debug), indent=4))
    else:    
        click.echo(json.dumps(api.addUserRoles(id, username, roleIds, roleNames, debug)))


@users.command('removeRoles')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --username.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --id.')
@click.option('--roleIds', 'roleIds', default=None, required=False, type=click.STRING, help='Comma separated list of role ids to be added to user. Must specify this option or --roleNames.')
@click.option('--roleNames', 'roleNames', default=None, required=False, type=click.STRING, help='Comma separated list of role names to be added to user. Must specify this option or --roleIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def removeUserRoles(id, username, roleIds, roleNames, debug, pretty):
    """Removes role assignments from a user"""
    if pretty:
        click.echo(json.dumps(api.removeUserRoles(id, username, roleIds, roleNames, debug), indent=4))
    else:    
        click.echo(json.dumps(api.removeUserRoles(id, username, roleIds, roleNames, debug)))


@users.command('addGroups')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --username.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --id.')
@click.option('--groupIds', 'groupIds', default=None, required=False, type=click.STRING, help='Comma separated list of group ids to be added to user. Must specify this option or --groupNames.')
@click.option('--groupNames', 'groupNames', default=None, required=False, type=click.STRING, help='Comma separated list of group names to be added to user. Must specify this option or --groupIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def addUserGroups(id, username, groupIds, groupNames, debug, pretty):
    """Adds group assignments to a user"""
    if pretty:
        click.echo(json.dumps(api.addUserGroups(id, username, groupIds, groupNames, debug), indent=4))
    else:    
        click.echo(json.dumps(api.addUserGroups(id, username, groupIds, groupNames, debug)))


@users.command('removeGroups')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --username.')
@click.option('--username', 'username', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --id.')
@click.option('--groupIds', 'groupIds', default=None, required=False, type=click.STRING, help='Comma separated list of group ids to be added to user. Must specify this option or --groupNames.')
@click.option('--groupNames', 'groupNames', default=None, required=False, type=click.STRING, help='Comma separated list of group names to be added to user. Must specify this option or --groupIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def removeUserGroups(id, username, groupIds, groupNames, debug, pretty):
    """Removes group assignments from a user"""
    if pretty:
        click.echo(json.dumps(api.removeUserGroups(id, username, groupIds, groupNames, debug), indent=4))
    else:    
        click.echo(json.dumps(api.removeUserGroups(id, username, groupIds, groupNames, debug)))
    

###################################
# User Groups commands section
###################################

@main.group()
def usergroups():
    """User group management commands."""
    pass

@usergroups.command('get')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='(Optional) Filter by user group id. Use this option or the --username option.')
@click.option('--name', 'name', default=None, required=False, type=click.STRING, help='(Optional) Filter by user group name. Use this option or the --id option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def getUserGroups(id, name, debug, pretty):
    """Returns user groups"""
    if pretty:
        click.echo(json.dumps(api.getUserGroups(id, name, debug), indent=4))
    else:    
        click.echo(json.dumps(api.getUserGroups(id, name, debug)))


@usergroups.command('create')
@click.option('--name', 'name', default=None, required=True, type=click.STRING, help='Name of the new user group.')
@click.option('--description', 'description', default=None, required=False, type=click.STRING, help='Description of the new user group.')
@click.option('--roleIds', 'roleIds', default=None, required=False, type=click.STRING, help='Comma separated list of role ids to be added to the new user group. Either this or the --roleNames group is required.')
@click.option('--roleNames', 'roleNames', default=None, required=False, type=click.STRING, help='Comma separated list of role names to be added to the new user group. Either this or the --roleIds group is required.')
@click.option('--userIds', 'userIds', default=None, required=False, type=click.STRING, help='Comma separated list of user ids to be added to the new user group.  Use this option or the --userNames option.')
@click.option('--userNames', 'userNames', default=None, required=False, type=click.STRING, help='Comma separated list of user names to be added to the new user group. Use this option or the --userIds option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def createUserGroup(name, description, roleIds, roleNames, userIds, userNames, debug, pretty):
    """Creates a new user group"""
    if pretty:
        click.echo(json.dumps(api.createUserGroup(name, description, roleIds, roleNames, userIds, userNames, debug), indent=4))
    else:    
        click.echo(json.dumps(api.createUserGroup(name, description, roleIds, roleNames, userIds, userNames, debug)))


@usergroups.command('addRoles')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='ID of user to be updated. Must specify this option or --groupname.')
@click.option('--groupname', 'groupname', default=None, required=False, type=click.STRING, help='ID of user group to be updated. Must specify this option or --id.')
@click.option('--roleIds', 'roleIds', default=None, required=False, type=click.STRING, help='Comma separated list of role ids to be added to user. Must specify this option or --roleNames.')
@click.option('--roleNames', 'roleNames', default=None, required=False, type=click.STRING, help='Comma separated list of role names to be added to user. Must specify this option or --roleIds.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def addUserGroupRoles(id, groupname, roleIds, roleNames, debug, pretty):
    """Adds role assignments to a user group"""
    if pretty:
        click.echo(json.dumps(api.addUserGroupRoles(id, groupname, roleIds, roleNames, debug), indent=4))
    else:    
        click.echo(json.dumps(api.addUserGroupRoles(id, groupname, roleIds, roleNames, debug)))


@usergroups.command('delete')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='User group id to be deleted. Use this option or the --name option.')
@click.option('--name', 'name', default=None, required=False, type=click.STRING, help='User group name to be deleted. Use this option or the --id option.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def deleteUserGroup(id, name, debug, pretty):
    """Deletes a user group"""
    if pretty:
        click.echo(json.dumps(api.deleteUserGroup(id, name, debug), indent=4))
    else:    
        click.echo(json.dumps(api.deleteUserGroup(id, name, debug)))
    

###################################
# Role commands section
###################################

@main.group()
def roles():
    """Role management commands."""
    pass

@roles.command('get')
@click.option('--id', 'id', default=None, required=False, type=click.STRING, help='Filter by role id.')
@click.option('--name', 'name', default=None, required=False, type=click.STRING, help='Filter by role name.')
@click.option('--expand', 'expand', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='Expand role privileges.')
@click.option('--debug', 'debug', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will print the API request details to console.')
@click.option('--pretty', 'pretty', flag_value=True, required=False, type=click.BOOL, is_flag=True, help='If true, will pretty print the returned JSON.')
def getRoles(id, name, expand, debug, pretty):
    """Returns roles"""
    if pretty:
        click.echo(json.dumps(api.getRoles(id, name, expand, debug), indent=4))
    else:    
        click.echo(json.dumps(api.getRoles(id, name, expand, debug)))


if __name__ == '__main__':
    main()
