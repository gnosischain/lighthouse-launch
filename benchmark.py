import yaml
import requests
import time
import json

with open('./validators/api-token.txt') as f:
    token = f.read()
    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


for i in range(256):
    validators = requests.get('http://localhost:5062/lighthouse/validators', headers=headers).json()['data']
    print('Got some validators: ', len(validators))

    for v in validators:
        if not v['enabled']:
            print('Enabling some validator: ', v['voting_pubkey'])
            data = json.dumps({'enabled': True})
            requests.patch('http://localhost:5062/lighthouse/validators/' + v['voting_pubkey'], data=data, headers=headers)
            break

    time.sleep(60)
