import requests
from idmc_cli.config import config

class InformaticaCloudAPI:
    def __init__(self):
        self.pod = config.get("pod")
        self.region = config.get("region")
        self.username = config.get("username")
        self.password = config.get("password")
        self.session_id = config.get("sessionId")
        self.max_attempts = config.get("maxAttempts")


    def login(self):
        """This function logs in to IDMC"""
        
        # Execute the API call
        url = f'https://{ self.region }.informaticacloud.com/saas/public/core/v3/login'
        headers = { 'Accept': 'application/json', 'Content-Type': 'application/json' }
        data = { 'username': self.username, 'password': self.password }
        r = requests.post(url, json=data, headers=headers)
        resp = r.json()
        
        # Save the session ID
        session_id = resp['userInfo']['sessionId']
        self.session_id = session_id
        config.set('sessionId', session_id)

        return resp
    
    
    def getUsers(self):
        """This function returns IDMC users""" 
        resp = ''
        attempts = 0
        limit = 1
        skip = 0
        pages = []
        
        while True:
        
            # Execute the API call
            url = f'https://{ self.pod }.{ self.region }.informaticacloud.com/saas/public/core/v3/users'
            headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'INFA-SESSION-ID': self.session_id }
            params = { 'limit': limit, 'skip': skip }
            r = requests.get(url, headers=headers, params=params)
            resp = r.json()

            # Check for expired session token
            if r.status_code == 401 and attempts <= self.max_attempts:
                self.login()
                attempts = attempts + 1
                continue
            # Abort after the maximum number of attempts
            elif attempts > self.max_attempts:
                pages.append(resp)
                break
            # If there is still some data then continue onto the next page
            elif len(resp) > 0:
                pages.append(resp)
                skip = skip + limit
                continue
            # Break when there are no pages left
            else:
                pages.append(resp)
                break
        
        return pages

# Expose the class as a variable
api = InformaticaCloudAPI()