import hashlib
import hmac
import json
import requests

# API info
API_HOST = 'https://api.bitkub.com'
API_KEY = '2e287fa51f6276ed010209fe13700a57'
API_SECRET = b'59f341c69e2a68660c0048fe77b6cb19'

def json_encode(data):
	return json.dumps(data, separators=(',', ':'), sort_keys=True)

def sign(data):
	j = json_encode(data)
	print('Signing payload: ' + j)
	h = hmac.new(API_SECRET, msg=j.encode(), digestmod=hashlib.sha256)
	return h.hexdigest()

# check server time
response = requests.get(API_HOST + '/api/servertime')
ts = int(response.text)
print('Server time: ' + response.text)

# check balances
header = {
	'Accept': 'application/json',
	'Content-Type': 'application/json',
	'X-BTK-APIKEY': API_KEY,
}
data = {
	'ts': ts,
}
signature = sign(data)
data['sig'] = signature

print('Payload with signature: ' + json_encode(data))
response = requests.post(API_HOST + '/api/market/balances', headers=header, data=json_encode(data))

print('Balances: ' + response.text)
