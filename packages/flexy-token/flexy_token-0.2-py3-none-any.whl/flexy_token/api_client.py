import requests
from datetime import timezone
import jwt

class APIClient:
    def __init__(self, account_sid, api_secret,api_key,identity):
        self.account_sid = account_sid
        self.api_secret = api_secret
        self.api_key= api_key
        self.identity=identity
        

def AccessToken(account_sid,api_secret,api_key,identity=""):
		try:
		
			payload = {
				'account_sid': account_sid,
				'api_key': api_key,
				'api_secret': api_secret,
				'identity': identity,
				
			}   
			token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')
			
			print (token,'tokentt')

			return token

		except Exception as e:
			return f"Token unable to generate because of an exception"

			


 
