import requests
import json
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

# Expose the class as a variable
api = InformaticaCloudAPI()