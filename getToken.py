from authlib.jose import JsonWebKey, JsonWebToken
import uuid
import time
import requests

# Add support for proxy (through Burp for example)
proxies = {
  'http': 'http://10.1.10.100:8080',
  'https': 'http://10.1.10.100:8080',
}

# The following should be provided by the party you want to authenticate to (customer, project team)
client_id = "123455-123123123-123123123"
token_endpoint = "https://placeholder/token"
scopes = "placeholder:scope/blabla" # Seperate multiple scopes with a space
 
# Specify supplied private key below
key_data = {
  "p": "blabla",
  "kty": "RSA",
  "q": "bla-bla",
  "d": "bla-bla-bla",
  "e": "blabla",
  "use": "sig",
  "kid": "blablabla",
  "qi": "bla-bla-bla",
  "dp": "bla-bla-bla",
  "alg": "PS256",
  "dq": "bla-bla",
  "n": "blablabla"
}
 
key = JsonWebKey.import_key(key_data)
 
client_assertion = {
"iss": client_id,
"sub": client_id,
"exp": int(time.time() + 300),
"jti": str(uuid.uuid4()),
"aud": token_endpoint
}
 
jwt = JsonWebToken(algorithms=['PS256'])
header = {'alg': 'PS256'}
token = jwt.encode(header, client_assertion, key)

body = {
'grant_type': 'client_credentials',
'client_id': client_id,
'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
'client_assertion': token
}
r = requests.post(token_endpoint, data=body, proxies=proxies, verify=False) # Added verify=False in order to pass traffic through proxy (Burp etc.)
if 'access_token' in r.json():
    print(r.json()['access_token'])
else:
    print(r.content)
