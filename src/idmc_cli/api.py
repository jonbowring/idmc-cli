import requests
import json
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
from idmc_cli.config import config

class InformaticaCloudAPI:
    def __init__(self):
        self.pod = config.get("pod")
        self.region = config.get("region")
        self.username = config.get("username")
        self.password = config.get("password")
        self.session_id = config.get("sessionId")
        self.max_attempts = config.get("maxAttempts")
        self.page_size = config.get("pageSize")
    
    #############################
    # Admin section
    #############################

    def debugRequest(self, r, attempts=0):
        print('\n')
        print('Attempts: ' + str(attempts))
        print('Method: ' + r.request.method)
        print('Headers: ' + str(r.request.headers))
        print('URL: ' + r.request.url)
        print('Body: ' + str(r.request.body))
        print('Hooks: ' + str(r.request.hooks))
        print('Status: ' + str(r.status_code))
        print('Response: ' + r.text)
        print('\n')
    
    def login(self, debug=False):
        """This function logs in to IDMC"""

        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Execute the API call
        url = f'https://{ self.region }.informaticacloud.com/saas/public/core/v3/login'
        headers = { 'Accept': 'application/json', 'Content-Type': 'application/json' }
        data = { 'username': self.username, 'password': self.password }
        r = requests.post(url, json=data, headers=headers)

        if debug:
            self.debugRequest(r)

        if r.status_code < 200 or r.status_code > 299:
            resp = {
                'status': r.status_code,
                'text': r.text
            }
        else:
            resp = r.json()
        
            # Save the session ID
            session_id = resp['userInfo']['sessionId']
            self.session_id = session_id
            config.set('sessionId', session_id)

        return resp
    
    #############################
    # Users section
    #############################

    def getUsers(self, id=None, username=None, debug=False):
        """This function returns IDMC users"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0
        skip = 0
        pages = []
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/users'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            params = { 'limit': self.page_size, 'skip': skip }
            if id:
                params['q'] = f'userId=="{ id }"'
            elif username:
                params['q'] = f'userName=="{ username }"'
            r = requests.get(url, headers=headers, params=params)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                pages.append(resp)
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # If there is still some data then continue onto the next page
            elif len(r.json()) > 0:
                resp = r.json()
                pages.append(resp)
                skip = skip + self.page_size
                continue
            # Break when there are no pages left
            else:
                break
        
        return pages
    

    def deleteUser(self, id=None, username=None, debug=False):
        """This function deletes an IDMC user"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the user id if needed
        if username:
            lookup = self.getUsers(username=username, debug=debug)
            try:
                id = lookup[0][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find user for id { username }'
                }
        
        attempts = 0
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/users/{ quote(id) }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.delete(url, headers=headers)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'User deleted' }
                break
            # Break when there are no pages left
            else:
                break
        
        return resp


    def createUser(self, name, firstName, lastName, email, password=None, description=None, title=None, phone=None, forcePasswordChange=None, maxLoginAttempts=None, authentication=None, aliasName=None, roleIds=None, roleNames=None, groupIds=None, groupNames=None, debug=False):
        """This function creates a new user"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the role ids if needed
        if roleNames:
            roleIds = []
            roles = roleNames.split(',')
            for role in roles:
                lookup = self.getRoles(name=role, debug=debug)
                try:
                    roleId = lookup[0]['id']
                    roleIds.append(roleId)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find role for id { role }'
                    }
        elif roleIds:
            roleIds = roleIds.split(',')
        
        # Lookup the group ids if needed
        if groupNames:
            groupIds = []
            groups = groupNames.split(',')
            for group in groups:
                lookup = self.getUserGroups(name=group, debug=debug)
                try:
                    groupId = lookup[0][0]['id']
                    groupIds.append(groupId)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find group id for { group }'
                    }
        elif groupIds:
            groupIds = groupIds.split(',')

        while True:
        
            # Prepare the mandatory fields
            data = {
                'name': name,
                'firstName': firstName,
                'lastName': lastName,
                'email': email
            }

            # Prepare the optional fields
            if password:
                data['password'] = password
            if description:
                data['description'] = description
            if title:
                data['title'] = title
            if phone:
                data['phone'] = phone
            if forcePasswordChange:
                data['forcePasswordChange'] = forcePasswordChange
            if maxLoginAttempts:
                data['maxLoginAttempts'] = maxLoginAttempts
            if authentication:
                data['authentication'] = authentication
            if aliasName:
                data['aliasName'] = aliasName
            if roleIds:
                data['roles'] = roleIds
            if groupIds:
                data['groups'] = groupIds
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/users'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            else:
                resp = r.json()
                break
        
        return resp
    


    def addUserRoles(self, id, username, roleIds, roleNames, debug=False):
        """This function adds roles to a user"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the user id if needed
        if username:
            lookup = self.getUsers(username=username, debug=debug)
            try:
                id = lookup[0][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find user for id { username }'
                    }
        
        # Lookup the role ids if needed
        if roleIds:
            roleNames = []
            roles = roleIds.split(',')
            for role in roles:
                lookup = self.getRoles(id=role, debug=debug)
                try:
                    roleName = lookup[0]['roleName']
                    roleNames.append(roleName)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find role for id { role }'
                    }
        elif roleNames:
            roleNames = roleNames.split(',')

        while True:
        
            # Prepare the mandatory fields
            data = {
                'roles': roleNames
            }
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/users/{ quote( id ) }/addRoles'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.put(url, headers=headers, json=data)
            
            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'User updated' }
                break
            else:
                resp = r.json()
                break
        
        return resp
    

    def removeUserRoles(self, id, username, roleIds, roleNames, debug=False):
        """This function removes roles from a user"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the user id if needed
        if username:
            lookup = self.getUsers(username=username, debug=debug)
            try:
                id = lookup[0][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find user for id { role }'
                    }
        
        # Lookup the role ids if needed
        if roleIds:
            roleNames = []
            roles = roleIds.split(',')
            for role in roles:
                lookup = self.getRoles(id=role, debug=debug)
                try:
                    roleName = lookup[0]['roleName']
                    roleNames.append(roleName)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find role for id { role }'
                    }
        elif roleNames:
            roleNames = roleNames.split(',')

        while True:
        
            # Prepare the mandatory fields
            data = {
                'roles': roleNames
            }
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/users/{ quote( id ) }/removeRoles'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.put(url, headers=headers, json=data)
            
            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'User updated' }
                break
            else:
                resp = r.json()
                break
        
        return resp
    

    def addUserGroups(self, id, username, groupIds, groupNames, debug=False):
        """This function adds groups to a user"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the user id if needed
        if username:
            lookup = self.getUsers(username=username, debug=debug)
            try:
                id = lookup[0][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find user id for { username }'
                    }
        
        # Lookup the group ids if needed
        if groupIds:
            groupNames = []
            groups = groupIds.split(',')
            for group in groups:
                lookup = self.getUserGroups(id=group, debug=debug)
                try:
                    groupName = lookup[0][0]['userGroupName']
                    groupNames.append(groupName)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find group for id { group }'
                    }
        elif groupNames:
            groupNames = groupNames.split(',')

        while True:
        
            # Prepare the mandatory fields
            data = {
                'groups': groupNames
            }
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/users/{ quote( id ) }/addGroups'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.put(url, headers=headers, json=data)
            
            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'User updated' }
                break
            else:
                resp = r.json()
                break
        
        return resp



    def removeUserGroups(self, id, username, groupIds, groupNames, debug=False):
        """This function removes groups from a user"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the user id if needed
        if username:
            lookup = self.getUsers(username=username, debug=debug)
            try:
                id = lookup[0][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find user id for { username }'
                    }
        
        # Lookup the group ids if needed
        if groupIds:
            groupNames = []
            groups = groupIds.split(',')
            for group in groups:
                lookup = self.getUserGroups(id=group, debug=debug)
                try:
                    groupName = lookup[0][0]['userGroupName']
                    groupNames.append(groupName)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find group for id { group }'
                    }
        elif groupNames:
            groupNames = groupNames.split(',')

        while True:
        
            # Prepare the mandatory fields
            data = {
                'groups': groupNames
            }
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/users/{ quote( id ) }/removeGroups'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.put(url, headers=headers, json=data)
            
            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'User updated' }
                break
            else:
                resp = r.json()
                break
        
        return resp


    #############################
    # Roles section
    #############################

    def getRoles(self, id=None, name=None, expand=None, debug=False):
        """This function returns IDMC roles"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0
        resp = ''
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/roles'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            params = {}
            if id:
                params['q'] = f'roleId=="{ id }"'
            elif name:
                params['q'] = f'roleName=="{ name }"'
            if expand:
                params['expand'] = f'privileges'
            r = requests.get(url, headers=headers, params=params)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                break
        
        return resp
    

    def createRole(self, name, description, privilegeIds=None, privilegeNames=None, debug=False):
        """This function creates a new role"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the role ids if needed
        if privilegeNames:
            privilegeIds = []
            privileges = privilegeNames.split(',')
            for privilege in privileges:
                lookup = self.getPrivileges(all=True, debug=debug)
                try:
                    privilegeId = [item for item in lookup if item['name'] == privilege][0]['id']
                    privilegeIds.append(privilegeId)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find privilege id for { privilege }'
                    }
        elif privilegeIds:
            privilegeIds = privilegeIds.split(',')
        

        while True:
        
            # Prepare the mandatory fields
            data = {
                'name': name,
                'privileges': privilegeIds
            }

            # Prepare the optional fields
            if description:
                data['description'] = description
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/roles'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            else:
                resp = r.json()
                break
        
        return resp
    

    def addRolePrivileges(self, id, name, privilegeIds, privilegeNames, debug=False):
        """This function adds privileges to a role"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the user group id if needed
        if name:
            lookup = self.getRoles(name=name, debug=debug)
            try:
                id = lookup[0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find role id for { name }'
                    }
        
        # Lookup the privilege ids if needed
        if privilegeIds:
            privilegeNames = []
            privileges = privilegeIds.split(',')
            for privilege in privileges:
                lookup = self.getPrivileges(id=privilege, debug=debug)
                try:
                    privilegeName = lookup[0]['name']
                    privilegeNames.append(privilegeName)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find privilege id { privilege }'
                    }
        elif privilegeNames:
            privilegeNames = privilegeNames.split(',')

        while True:
        
            # Prepare the mandatory fields
            data = {
                'privileges': privilegeNames
            }
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/roles/{ quote( id ) }/addPrivileges'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.put(url, headers=headers, json=data)
            
            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'User group updated' }
                break
            else:
                resp = r.json()
                break
        
        return resp
    

    def removeRolePrivileges(self, id, name, privilegeIds, privilegeNames, debug=False):
        """This function removes privileges from a role"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the role id if needed
        if name:
            lookup = self.getRoles(name=name, debug=debug)
            try:
                id = lookup[0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find role id for { name }'
                    }
        
        # Lookup the privilege ids if needed
        if privilegeIds:
            privilegeNames = []
            privileges = privilegeIds.split(',')
            for privilege in privileges:
                lookup = self.getPrivileges(id=privilege, debug=debug)
                try:
                    privilegeName = lookup[0]['name']
                    privilegeNames.append(privilegeName)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find privilege id { privilege }'
                    }
        elif privilegeNames:
            privilegeNames = privilegeNames.split(',')

        while True:
        
            # Prepare the mandatory fields
            data = {
                'privileges': privilegeNames
            }
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/roles/{ quote( id ) }/removePrivileges'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.put(url, headers=headers, json=data)
            
            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'User group updated' }
                break
            else:
                resp = r.json()
                break
        
        return resp
    

    def deleteRole(self, id=None, name=None, debug=False):
        """This function deletes an IDMC role"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the role id if needed
        if name:
            lookup = self.getRoles(name=name, debug=debug)
            try:
                id = lookup[0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find role id for { name }'
                    }
        
        attempts = 0
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/roles/{ quote(id) }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.delete(url, headers=headers)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'Role deleted' }
                break
            # Break when there are no pages left
            else:
                break
        
        return resp
    

    #############################
    # Privileges section
    #############################

    def getPrivileges(self, all=False, debug=False):
        """This function returns IDMC roles"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0
        resp = ''
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/privileges'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            params = {}
            if all:
                params['q'] = f'status==All'
            r = requests.get(url, headers=headers, params=params)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                break
        
        return resp
    
    #############################
    # Groups section
    #############################

    def getUserGroups(self, id=None, name=None, debug=False):
        """This function returns IDMC user groups"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0
        skip = 0
        pages = []
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/userGroups'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            params = { 'limit': self.page_size, 'skip': skip }
            if id:
                params['q'] = f'userGroupId=="{ id }"'
            elif name:
                params['q'] = f'userGroupName=="{ name }"'
            r = requests.get(url, headers=headers, params=params)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                pages.append(resp)
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # If there is still some data then continue onto the next page
            elif len(r.json()) > 0:
                resp = r.json()
                pages.append(resp)
                skip = skip + self.page_size
                continue
            # Break when there are no pages left
            else:
                break
        
        return pages
    


    def createUserGroup(self, name, description, roleIds=None, roleNames=None, userIds=None, userNames=None, debug=False):
        """This function creates a new user group"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the role ids if needed
        if roleNames:
            roleIds = []
            roles = roleNames.split(',')
            for role in roles:
                lookup = self.getRoles(name=role, debug=debug)
                try:
                    roleId = lookup[0]['id']
                    roleIds.append(roleId)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find role for id { role }'
                    }
        elif roleIds:
            roleIds = roleIds.split(',')
        
        # Lookup the user ids if needed
        if userNames:
            userIds = []
            users = userNames.split(',')
            for user in users:
                lookup = self.getUsers(username=user, debug=debug)
                try:
                    userId = lookup[0][0]['id']
                    userIds.append(userId)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find user id for { user }'
                    }
        elif userIds:
            userIds = userIds.split(',')

        while True:
        
            # Prepare the mandatory fields
            data = {
                'name': name,
                'roles': roleIds
            }

            # Prepare the optional fields
            if description:
                data['description'] = description
            if userIds:
                data['users'] = userIds
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/userGroups'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            else:
                resp = r.json()
                break
        
        return resp
    

    def addUserGroupRoles(self, id, groupname, roleIds, roleNames, debug=False):
        """This function adds roles to a user group"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the user group id if needed
        if groupname:
            lookup = self.getUserGroups(name=groupname, debug=debug)
            try:
                id = lookup[0][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find user group id for { groupname }'
                    }
        
        # Lookup the role ids if needed
        if roleIds:
            roleNames = []
            roles = roleIds.split(',')
            for role in roles:
                lookup = self.getRoles(id=role, debug=debug)
                try:
                    roleName = lookup[0]['roleName']
                    roleNames.append(roleName)
                except Exception as e:
                    return {
                        'status': 500,
                        'text': f'Unable to find role for id { role }'
                    }
        elif roleNames:
            roleNames = roleNames.split(',')

        while True:
        
            # Prepare the mandatory fields
            data = {
                'roles': roleNames
            }
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/userGroups/{ quote( id ) }/addRoles'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.put(url, headers=headers, json=data)
            
            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'User group updated' }
                break
            else:
                resp = r.json()
                break
        
        return resp
    

    def deleteUserGroup(self, id=None, name=None, debug=False):
        """This function deletes an IDMC user group"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the user id if needed
        if name:
            lookup = self.getUserGroups(name=name, debug=debug)
            try:
                id = lookup[0][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find user group id for { name }'
                }
        
        attempts = 0
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/userGroups/{ quote(id) }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.delete(url, headers=headers)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'User group deleted' }
                break
            # Break when there are no pages left
            else:
                break
        
        return resp
    

    #############################
    # Lookup section
    #############################

    def lookupObject(self, id=None, path=None, type=None, debug=False):
        """This function is used to lookup objects"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/lookup'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            data = {
                'objects': []
            }
            obj = {}
            if id:
                obj['id'] = id
            if type:
                obj['type'] = type
            if path:
                obj['path'] = path
            data['objects'].append(obj)

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                resp = r.json()
                break
        
        return resp
    
    def lookupObjects(self, body, debug=False):
        """This function is used to lookup objects"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/lookup'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            data = json.loads(body)

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                resp = r.json()
                break
        
        return resp
    
    #############################
    # Tags section
    #############################

    def tagObject(self, id, path, type, tags, debug=False):
        """This function is used to add tags to an object"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        # Lookup the object id if needed
        if path and type:
            lookup = self.lookupObject(path=path, type=type, debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type { type }'
                }
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/TagObjects'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            data = []
            obj = {
                'id': id,
                'tags': tags.split(',')
            }
            data.append(obj)

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'Object updated' }
                break
            # Return the response
            else:
                break
        
        return resp
    

    def tagObjects(self, body, debug=False):
        """This function is used to add tags to multiple objects"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        data = []
        for obj in json.loads(body):
            path = None
            type = None
            tags = obj['tags']

            if 'path' in obj and 'type' in obj:
                path = obj['path']
                type = obj['type']

            # Lookup the object id if needed
            if path and type:
                lookup = self.lookupObject(path=path, type=type, debug=debug)
                try:
                    id = lookup['objects'][0]['id']
                except Exception as e:
                    return {
                            'status': 500,
                            'text': f'Unable to find object id for path { path } and type { type }'
                    }
            # Else use the IDs
            else:
                id = obj['id']
            
            # Finally include the tags and add to the list
            data.append({
                'id': id,
                'tags': tags
            })
            
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/TagObjects'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'Object updated' }
                break
            # Return the response
            else:
                break
        
        return resp
    

    def untagObject(self, id, path, type, tags, debug=False):
        """This function is used to add remove tags from an object"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        # Lookup the object id if needed
        if path and type:
            lookup = self.lookupObject(path=path, type=type, debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type { type }'
                }
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/UntagObjects'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            data = []
            obj = {
                'id': id,
                'tags': tags.split(',')
            }
            data.append(obj)

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'Object updated' }
                break
            # Return the response
            else:
                break
        
        return resp
    

    def untagObjects(self, body, debug=False):
        """This function is used to remove tags from multiple objects"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        data = []
        for obj in json.loads(body):
            path = None
            type = None
            tags = obj['tags']

            if 'path' in obj and 'type' in obj:
                path = obj['path']
                type = obj['type']

            # Lookup the object id if needed
            if path and type:
                lookup = self.lookupObject(path=path, type=type, debug=debug)
                try:
                    id = lookup['objects'][0]['id']
                except Exception as e:
                    return {
                            'status': 500,
                            'text': f'Unable to find object id for path { path } and type { type }'
                    }
            # Else use the IDs
            else:
                id = obj['id']
            
            # Finally include the tags and add to the list
            data.append({
                'id': id,
                'tags': tags
            })
            
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/UntagObjects'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'Object updated' }
                break
            # Return the response
            else:
                break
        
        return resp
    

    #############################
    # Projects section
    #############################
    
    def createProject(self, name, description, debug=False):
        """This function creates a new project"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0

        while True:
        
            # Prepare the mandatory fields
            data = {
                'name': name
            }

            # Prepare the optional fields
            if description:
                data['description'] = description
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/projects'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            else:
                resp = r.json()
                break
        
        return resp
    

    def updateProject(self, id, path, name, description=None, debug=False):
        """This function is used to update a project"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the project id if needed
        if path:
            lookup = self.lookupObject(path=path, type='PROJECT', debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type PROJECT'
                    }

        while True:
        
            # Prepare the update fields
            data = {}
            if name:
                data['name'] = name
            if description:
                data['description'] = description
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/projects/{ quote( id ) }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.patch(url, headers=headers, json=data)
            
            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'Project updated' }
                break
            else:
                resp = r.json()
                break
        
        return resp
    

    def deleteProject(self, id, path, debug=False):
        """This function is used to delete a project"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the project id if needed
        if path:
            lookup = self.lookupObject(path=path, type='PROJECT', debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type PROJECT'
                    }

        while True:
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/projects/{ quote( id ) }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.delete(url, headers=headers)
            
            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'Project deleted' }
                break
            else:
                break
        
        return resp
    

    #############################
    # Folders section
    #############################
    
    def createFolder(self, projectId, projectName, name, description, debug=False):
        """This function creates a new folder"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the project id if needed
        if projectName:
            lookup = self.lookupObject(path=projectName, type='PROJECT', debug=debug)
            try:
                projectId = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { projectName } and type PROJECT'
                    }
        
        resp = ''
        attempts = 0

        while True:
        
            # Prepare the mandatory fields
            data = {
                'name': name
            }

            # Prepare the optional fields
            if description:
                data['description'] = description
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/projects/{ projectId }/folders'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            else:
                resp = r.json()
                break
        
        return resp
    
    def updateFolder(self, id, path, name, description, debug=False):
        """This function is used to update a folder"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the folder id if needed
        if path:
        
            # Get the folder ID
            lookup = self.lookupObject(path=path, type='FOLDER', debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type FOLDER'
                    }


        while True:
        
            # Prepare the update fields
            data = {}
            if name:
                data['name'] = name
            if description:
                data['description'] = description
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/folders/{ quote( id ) }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.patch(url, headers=headers, json=data)
            
            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'Folder updated' }
                break
            else:
                break
        
        return resp
    

    def deleteFolder(self, id, path, debug=False):
        """This function is used to delete a folder"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        resp = ''
        attempts = 0
        
        # Lookup the folder id if needed
        if path:
        
            # Get the folder ID
            lookup = self.lookupObject(path=path, type='FOLDER', debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type FOLDER'
                    }

        while True:
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/folders/{ quote( id ) }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.delete(url, headers=headers)
            
            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            elif r.status_code == 204:
                resp = { 'message': 'Folder deleted' }
                break
            else:
                break
        
        return resp
    

    #############################
    # Source control section
    #############################

    def checkInObject(self, summary, description, id, path, type, includeContainer, debug=False):
        """This function is used to check an object into a git repository"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        # Lookup the object id if needed
        if path and type:
            lookup = self.lookupObject(path=path, type=type, debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type { type }'
                }
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/checkin'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            
            # Include the mandatory fields
            data = {
                'objects': [
                    {
                        'id': id
                    }
                ],
                'summary': summary
            }

            # Include the optional fields if needed
            if description:
                data['description'] = description
            if includeContainer:
                data['objects'][0]['includeContainerAssets'] = includeContainer

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                resp = r.json()
                break
        
        return resp
    

    def checkInObjects(self, summary, description, body, debug=False):
        """This function is used to check in one or more objects into a git repository"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        objects = []
        for obj in json.loads(body):
            path = None
            type = None
            tmp = {}

            if 'path' in obj and 'type' in obj:
                path = obj['path']
                type = obj['type']
            if 'includeContainerAssets' in obj:
                tmp['includeContainerAssets'] = obj['includeContainerAssets']

            # Lookup the object id if needed
            if path and type:
                lookup = self.lookupObject(path=path, type=type, debug=debug)
                try:
                    id = lookup['objects'][0]['id']
                except Exception as e:
                    return {
                            'status': 500,
                            'text': f'Unable to find object id for path { path } and type { type }'
                    }
            # Else use the IDs
            else:
                id = obj['id']
            
            # Finally include the id and add to the list
            tmp['id'] = id
            objects.append(tmp)
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/checkin'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            
            # Include the mandatory fields
            data = {
                'objects': objects,
                'summary': summary
            }

            # Include the optional fields if needed
            if description:
                data['description'] = description

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                resp = r.json()
                break
        
        return resp
    

    def checkOutObject(self, id, path, type, includeContainer, debug=False):
        """This function is used to check out an object from a git repository"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        # Lookup the object id if needed
        if path and type:
            lookup = self.lookupObject(path=path, type=type, debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type { type }'
                }
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/checkout'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            
            # Include the mandatory fields
            data = {
                'objects': [
                    {
                        'id': id
                    }
                ]
            }

            # Include the optional fields if needed
            if includeContainer:
                data['objects'][0]['includeContainerAssets'] = includeContainer

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                resp = r.json()
                break
        
        return resp
    

    def checkOutObjects(self, body, debug=False):
        """This function is used to check out one or more objects from a git repository"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        objects = []
        for obj in json.loads(body):
            path = None
            type = None
            tmp = {}

            if 'path' in obj and 'type' in obj:
                path = obj['path']
                type = obj['type']
            if 'includeContainerAssets' in obj:
                tmp['includeContainerAssets'] = obj['includeContainerAssets']

            # Lookup the object id if needed
            if path and type:
                lookup = self.lookupObject(path=path, type=type, debug=debug)
                try:
                    id = lookup['objects'][0]['id']
                except Exception as e:
                    return {
                            'status': 500,
                            'text': f'Unable to find object id for path { path } and type { type }'
                    }
            # Else use the IDs
            else:
                id = obj['id']
            
            # Finally include the id and add to the list
            tmp['id'] = id
            objects.append(tmp)
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/checkout'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            
            # Include the mandatory fields
            data = {
                'objects': objects
            }

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                resp = r.json()
                break
        
        return resp
    

    def pullObject(self, id, path, type, hash, relaxValidation, debug=False):
        """This function pulls an object from a git repository"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        # Lookup the object id if needed
        if path and type:
            lookup = self.lookupObject(path=path, type=type, debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type { type }'
                }
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/pull'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            
            # Include the mandatory fields
            data = {
                'commitHash': hash,
                'objects': [
                    {
                        'id': id
                    }
                ]
            }

            # Include the optional fields if needed
            if relaxValidation:
                data['relaxObjectSpecificationValidation'] = relaxValidation

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                resp = r.json()
                break
        
        return resp
    

    def pullObjects(self, body, hash, relaxValidation, debug=False):
        """This function is used to pull one or more objects from a git repository"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        objects = []
        for obj in json.loads(body):
            path = None
            type = None
            tmp = {}

            if 'path' in obj and 'type' in obj:
                path = obj['path']
                type = obj['type']

            # Lookup the object id if needed
            if path and type:
                lookup = self.lookupObject(path=path, type=type, debug=debug)
                try:
                    id = lookup['objects'][0]['id']
                except Exception as e:
                    return {
                            'status': 500,
                            'text': f'Unable to find object id for path { path } and type { type }'
                    }
            # Else use the IDs
            else:
                id = obj['id']
            
            # Finally include the id and add to the list
            tmp['id'] = id
            objects.append(tmp)
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/pull'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            
            # Include the mandatory fields
            data = {
                'commitHash': hash,
                'objects': objects
            }
            if relaxValidation:
                data['relaxObjectSpecificationValidation'] = relaxValidation

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                resp = r.json()
                break
        
        return resp
    

    def pullByCommitHash(self, hash, search, repoId, relaxValidation, debug=False):
        """This function pulls all objects in a commit hash from a git repository"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/pullByCommitHash'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            
            # Include the mandatory fields
            data = {
                'commitHash': hash
            }

            # Include the optional fields if needed
            if search:
                data['searchCustomRepositories'] = search
            if repoId:
                data['repoConnectionId'] = repoId
            if relaxValidation:
                data['relaxObjectSpecificationValidation'] = relaxValidation

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                resp = r.json()
                break
        
        return resp
    

    def undoCheckOutObject(self, id, path, type, includeContainer, debug=False):
        """This function is used to undo a check out of an object from a git repository"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        # Lookup the object id if needed
        if path and type:
            lookup = self.lookupObject(path=path, type=type, debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type { type }'
                }
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/undoCheckout'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            
            # Include the mandatory fields
            data = {
                'objects': [
                    {
                        'id': id
                    }
                ]
            }

            # Include the optional fields if needed
            if includeContainer:
                data['objects'][0]['includeContainerAssets'] = includeContainer

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                resp = r.json()
                break
        
        return resp
    

    def undoCheckOutObjects(self, body, debug=False):
        """This function is used to undo check out of one or more objects from a git repository"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0

        objects = []
        for obj in json.loads(body):
            path = None
            type = None
            tmp = {}

            if 'path' in obj and 'type' in obj:
                path = obj['path']
                type = obj['type']
            if 'includeContainerAssets' in obj:
                tmp['includeContainerAssets'] = obj['includeContainerAssets']

            # Lookup the object id if needed
            if path and type:
                lookup = self.lookupObject(path=path, type=type, debug=debug)
                try:
                    id = lookup['objects'][0]['id']
                except Exception as e:
                    return {
                            'status': 500,
                            'text': f'Unable to find object id for path { path } and type { type }'
                    }
            # Else use the IDs
            else:
                id = obj['id']
            
            # Finally include the id and add to the list
            tmp['id'] = id
            objects.append(tmp)
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/undoCheckout'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            
            # Include the mandatory fields
            data = {
                'objects': objects
            }

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                resp = r.json()
                break
        
        return resp

    def getSourceStatus(self, id, debug=False):
        """This function returns the status for a source control action"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/sourceControlAction/{ quote(id) }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.get(url, headers=headers)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                break
        
        return resp
    

    def getRepoConnection(self, projectIds, projectNames, debug=False):
        """This function returns the details of a git repository for an org or projects"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/repositoryConnection'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }

            # Populate the optional fields if needed
            params = {}
            if projectIds:
                params['projectIds'] = projectIds
            if projectNames:
                params['projectNames'] = projectNames

            r = requests.get(url, headers=headers, params=params)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                break
        
        return resp
    

    def getCommitHistory(self, id, path, type, branch, debug=False):
        """This function returns the git history for an asset"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the object id if needed
        if path and type:
            lookup = self.lookupObject(path=path, type=type, debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type { type }'
                }
        
        attempts = 0
        page = 1
        pages = []
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/commitHistory'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }

            # Initialise the query
            params = { 'perPage': self.page_size, 'page': page, 'q': f'id=="{ id }"' }
            if branch:
                params['q'] += f' and branch=="{ branch }"'

            r = requests.get(url, headers=headers, params=params)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                pages.append(resp)
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                pages.append(resp)
                break
            # If there is still some data then continue onto the next page
            elif len(r.json()['commits']) > 0:
                resp = r.json()
                pages.append(resp)
                page +=1
                continue
            # Break when there are no pages left
            else:
                break
        
        return pages
    

    def getCommitDetails(self, hash, searchAllRepos, repoId, debug=False):
        """This function returns the details of a git commit"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/commit/{ hash }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }

            # Populate the optional fields if needed
            params = {}
            if searchAllRepos:
                params['searchCustomRepositories'] = searchAllRepos
            if repoId:
                params['repoConnectionId'] = repoId

            r = requests.get(url, headers=headers, params=params)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                break
        
        return resp
    

    def compareVersions(self, id, path, type, oldVersion, newVersion, format, debug=False):
        """This function is used to compare asset versions"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the object id if needed
        if path and type:
            lookup = self.lookupObject(path=path, type=type, debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find object id for path { path } and type { type }'
                }

        attempts = 0
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/compare/{ id }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            
            # Include the mandatory fields
            data = {
                'source': oldVersion,
                'destination': newVersion,
                'outputFormat': format
            }

            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Return the response
            else:
                if format == 'JSON':
                    resp = r.json()
                else:
                    resp = r.text
                break
        
        return resp
    
    #############################
    # Logs section
    #############################

    def getSecurityLogs(self, category, actor, name, time_from='1970-01-01T00:00:01.000Z', time_to='9999-31-12T00:00:01.000Z', debug=False):
        """This function returns the git history for an asset"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        now = datetime.now(timezone.utc)
        past = now - timedelta(days=14)
        if time_to is None:
            time_to = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        if time_from is None:
            time_from = past.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        attempts = 0
        skip = 0
        pages = []
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/securityLog'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }

            # Initialise the query
            params = { 'limit': self.page_size, 'skip': skip, 'q': f'entryTime>="{ time_from }" and entryTime<="{ time_to }"' }
            if category:
                params['q'] += f';actionCategory=="{ category }"'
            if actor:
                params['q'] += f';actor=="{ actor }"'
            if name:
                params['q'] += f';objectName=="{ name }"'

            r = requests.get(url, headers=headers, params=params)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                pages.append(resp)
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                pages.append(resp)
                break
            # If there is still some data then continue onto the next page
            elif len(r.json()['entries']) > 0:
                resp = r.json()
                pages.append(resp)
                skip += self.page_size
                continue
            # Break when there are no pages left
            else:
                break
        
        return pages
    

    #############################
    # Secure agent section
    #############################
    
    def getAgents(self, id=None, name=None, unassigned=None, debug=False):
        """This function returns secure agents"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the agent id if needed
        if name:
            lookup = self.getAgents(unassigned=unassigned, debug=debug)
            try:
                id = [obj for obj in lookup if obj['name'] == name][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { name }'
                    }
        
        attempts = 0
        resp = ''
        
        while True:
        
            params = {}
            if unassigned:
                params['includeUnassignedOnly'] = unassigned
            
            # Execute the API call
            if id:
                url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/agent/{ quote(id) }'
            else:
                url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/agent'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.get(url, headers=headers, params=params)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                break
        
        return resp
    
    def getAgentStatus(self, id=None, name=None, debug=False):
        """This function returns secure agents"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the agent id if needed
        if name:
            lookup = self.getAgents(debug=debug)
            try:
                id = [obj for obj in lookup if obj['name'] == name][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { name }'
                    }
        
        attempts = 0
        resp = ''
        
        while True:
            
            # Execute the API call
            if id:
                url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/agent/details/{ quote(id) }'
            else:
                url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/agent/details'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.get(url, headers=headers)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                break
        
        return resp
    
    def deleteAgent(self, id=None, name=None, unassigned=None, debug=False):
        """This function returns secure agents"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the agent id if needed
        if name:
            lookup = self.getAgents(unassigned=unassigned, debug=debug)
            try:
                id = [obj for obj in lookup if obj['name'] == name][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { name }'
                    }
        
        attempts = 0
        resp = ''
        
        while True:
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/agent/{ quote(id) }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.delete(url, headers=headers)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = {
                    'status': r.status_code,
                    'text': 'Agent deleted'
                }
                break
        
        return resp
    
    def getAgentGroups(self, id=None, name=None, debug=False):
        """This function returns secure agent groups"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the runtime env id if needed
        if name:
            lookup = self.getAgentGroups(debug=debug)
            try:
                id = [obj for obj in lookup if obj['name'] == name][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { name }'
                    }
        
        attempts = 0
        resp = ''
        
        while True:
        
            # Execute the API call
            if id:
                url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment/{ quote(id) }'
            else:
                url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.get(url, headers=headers)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                break
        
        return resp
    

    def createAgentGroup(self, name=None, shared=None, debug=False):
        """This function creates a new secure agent group"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        attempts = 0
        resp = ''
        
        while True:
        
            data = {
                '@type': 'runtimeEnvironment',
                'name': name
            }
            if shared:
                data['isShared'] = shared
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                break
        
        return resp
    

    def addAgent(self, groupId, groupName, agentId, agentName, debug=False):
        """This function adds a secure agent to a secure agent group"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the agent group
        if groupName:
            lookup = self.getAgentGroups(debug=debug)
            try:
                groupId = [obj for obj in lookup if obj['name'] == groupName][0]['id']
                shared = [obj for obj in lookup if obj['name'] == groupName][0]['isShared']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { groupName }'
                    }
        else:
            lookup = self.getAgentGroups(id=groupId, debug=debug)
            try:
                groupName = lookup['name']
                shared = lookup['isShared']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { groupId }'
                    }
        
        # Lookup the agent id if needed
        agents = []
        if len(agentName) > 0:
            
            for agent in agentName:
                try:
                    lookup = self.getAgents(unassigned=False, debug=debug)
                    filter = [obj for obj in lookup if obj['name'] == agent]
                    
                    if len(filter) == 0:
                        lookup = self.getAgents(unassigned=True, debug=debug)
                        agentId = [obj for obj in lookup if obj['name'] == agent][0]['id']
                        orgId = [obj for obj in lookup if obj['name'] == agent][0]['orgId']
                    else:
                        agentId = filter[0]['id']
                        orgId = filter[0]['orgId']

                    agents.append({
                        '@type': 'agent',
                        'id': agentId,
                        'orgId': orgId
                    })
                except Exception as e:
                    return {
                            'status': 500,
                            'text': f'Unable to find id for runtime environment { agent }'
                        }
        else:
            for agent in agentId:
                try:
                    lookup = self.getAgents(id=agent, unassigned=False, debug=debug)
                    
                    if lookup is None:
                        lookup = self.getAgents(id=agent, unassigned=True, debug=debug)
                    orgId = lookup['orgId']

                    agents.append({
                        '@type': 'agent',
                        'id': agent,
                        'orgId': orgId
                    })
                except Exception as e:
                    return {
                            'status': 500,
                            'text': f'Unable to find id for runtime environment { agent }'
                        }

        attempts = 0
        resp = ''
        
        while True:
        
            data = {
                '@type': 'runtimeEnvironment',
                'name': groupName,
                'isShared': shared,
                'agents': agents
            }
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment/{ quote(groupId) }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                break
        
        return resp
    

    def deleteAgentGroup(self, id=None, name=None, debug=False):
        """This function deletes a secure agent group"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the agent group
        if name:
            lookup = self.getAgentGroups(name=name, debug=debug)
            try:
                id = lookup['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { name }'
                    }
        
        attempts = 0
        resp = ''
        
        while True:
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment/{ quote(id) }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.delete(url, headers=headers)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = {
                    'status': r.status_code,
                    'text': 'Agent group deleted'
                }
                break
        
        return resp
    

    def getAgentGroupComponents(self, id=None, name=None, includeAll=None, debug=False):
        """This function returns secure agent group component details"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the runtime env id if needed
        if name:
            lookup = self.getAgentGroups(debug=debug)
            try:
                id = [obj for obj in lookup if obj['name'] == name][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { name }'
                    }
        
        attempts = 0
        resp = ''
        
        while True:
        
            # Execute the API call
            if includeAll:
                url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment/{ quote(id) }/selections/details'
            else:
                url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment/{ quote(id) }/selections'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.get(url, headers=headers)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                break
        
        return resp
    

    def updateAgentGroupComponents(self, id=None, name=None, enable=None, services=None, connectors=None, additional=None, debug=False):
        """This function returns secure agent group component details"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the runtime env id if needed
        if name:
            lookup = self.getAgentGroups(debug=debug)
            try:
                id = [obj for obj in lookup if obj['name'] == name][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { name }'
                    }
        
        # Lookup the components for the agent group
        components = self.getAgentGroupComponents(id=id, includeAll=True, debug=debug)

        connectorObjs = []
        serviceObjs = []
        additionalObjs = []

        # Loop through the connectors, lookup the id's and add them to the list
        for cnx in connectors:
            try:
                lookup = [obj for obj in components['connectors']['selections'] if obj['name'] == cnx][0]
            except Exception as e:
                print(f'Error: Unable to find connector "{ cnx }"')
                continue
            connectorObjs.append({
                'id': lookup['id'],
                'name': cnx,
                'enabled': enable
            })

        # Loop through the services, lookup the id's and add them to the list
        for svc in services:
            try:
                lookup = [obj for obj in components['services']['selections'] if obj['name'] == svc][0]
            except Exception as e:
                print(f'Error: Unable to find service "{ svc }"')
                continue
            serviceObjs.append({
                'id': lookup['id'],
                'name': svc,
                'enabled': enable
            })

        # Loop through the additional services, lookup the id's and add them to the list
        for svc in additional:
            try:
                lookup = [obj for obj in components['additionalServices']['selections'] if obj['name'] == svc][0]
            except Exception as e:
                print(f'Error: Unable to find service "{ svc }"')
                continue
            additionalObjs.append({
                'id': lookup['id'],
                'name': svc,
                'enabled': enable
            })

        if len(connectorObjs) == 0 and len(serviceObjs) == 0 and len(additionalObjs) == 0:
            raise Exception('Unable to find relevant service, connector or additional service') 

        attempts = 0
        resp = ''
        
        while True:
        
            data = {
                'services': {
                    'selections': serviceObjs
                },
                'connectors': {
                    'selections': connectorObjs
                },
                'additionalServices': {
                    'selections': additionalObjs
                },
            }
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment/{ quote(id) }/selections'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.put(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = {
                        'status': r.status_code,
                        'text': f'Components updated'
                    }
                break
        
        return resp
    

    def getAgentGroupProps(self, id=None, name=None, service=None, type=None, property=None, overridden=None, platform=None, debug=False):
        """This function returns secure agent group property details"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the runtime env id if needed
        if name:
            lookup = self.getAgentGroups(debug=debug)
            try:
                id = [obj for obj in lookup if obj['name'] == name][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { name }'
                    }
            
        # Include the platform if set
        if platform:
            platform = '/' + platform
        else:
            platform = ''
        
        attempts = 0
        resp = ''
        
        while True:
        
            # Execute the API call
            if overridden:
                url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment/{ quote(id) }/configs{ platform }'
            else:
                url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment/{ quote(id) }/configs/details{ platform }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.get(url, headers=headers)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = r.json()
                
                # Apply the response filters if needed
                if service:
                    resp = { 
                        service: resp[service]
                     }
                    
                    if type:
                        filtered = [obj for obj in resp[service] if type in obj]
                        resp[service] = filtered

                        if property:
                            filtered = [obj for obj in resp[service][0][type] if property == obj['name']]
                            resp[service][0][type] = filtered

                break
        
        return resp
    

    def updateAgentGroupProps(self, id=None, name=None, service=None, type=None, property=None, value=None, platform=None, custom=None, sensitive=None, debug=False):
        """This function updates secure agent group property details"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the runtime env id if needed
        if name:
            lookup = self.getAgentGroups(debug=debug)
            try:
                id = [obj for obj in lookup if obj['name'] == name][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { name }'
                    }
            
        # Include the platform if set
        if platform:
            platform = '/' + platform
        else:
            platform = ''
        
        attempts = 0
        resp = ''
        
        while True:
            
            # Prepare the mandatory fields
            data = {
                service: [
                    {
                        type: [
                            {
                                'name': property,
                                'value': value
                            }
                        ]
                    }
                ]
            }

            # Add the optional fields if needed
            if custom:
                data[service][0][type][0]['isCustom'] = 'true'
            else:
                data[service][0][type][0]['isCustom'] = 'false'
            if sensitive:
                data[service][0][type][0]['isSensitive'] = 'true'
            else:
                data[service][0][type][0]['isSensitive'] = 'false'
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment/{ quote(id) }/configs{ platform }'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.put(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = {
                    'status': r.status_code,
                    'text': 'Property updated'
                }
                break
        
        return resp
    

    def deleteAgentGroupProps(self, id=None, name=None, debug=False):
        """This function deletes secure agent group property details"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the runtime env id if needed
        if name:
            lookup = self.getAgentGroups(debug=debug)
            try:
                id = [obj for obj in lookup if obj['name'] == name][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { name }'
                    }
        
        attempts = 0
        resp = ''
        
        while True:
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/api/v2/runtimeEnvironment/{ quote(id) }/configs'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'icSessionId': self.session_id }
            r = requests.delete(url, headers=headers)

            if debug:
                self.debugRequest(r, attempts)
            
            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Break when there are no pages left
            else:
                resp = {
                    'status': r.status_code,
                    'text': 'Properties deleted'
                }
                break
        
        return resp
    
    
    def execAgentService(self, id, name, service, action, debug=False):
        """This function is used to stop or start a service on a secure agent"""
        
        # Check if cli has been configured
        if not self.username:
            return 'CLI needs to be configured. Run the command "idmc configure"'
        
        # Lookup the runtime env id if needed
        if name:
            lookup = self.lookupObject(path=name, type='AGENT', debug=debug)
            try:
                id = lookup['objects'][0]['id']
            except Exception as e:
                return {
                        'status': 500,
                        'text': f'Unable to find id for runtime environment { name }'
                    }
        
        resp = ''
        attempts = 0

        while True:
        
            # Prepare the mandatory fields
            data = {
                'serviceName': service,
                'serviceAction': action,
                'agentId': id
            }
            
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/agent/service'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            r = requests.post(url, headers=headers, json=data)

            if debug:
                self.debugRequest(r, attempts)

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            # Else if there is an unexpected error return a failure
            elif r.status_code < 200 or r.status_code > 299:
                resp = {
                    'status': r.status_code,
                    'text': r.text
                }
                break
            else:
                resp = r.json()
                break
        
        return resp

    

# Expose the class as a variable
api = InformaticaCloudAPI()