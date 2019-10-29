import requests
import json
payload = {"username": "CHANGE_TO_USER", "password": "CHANGE_TO_PASSWORD"}
authentication = requests.post('https://CHANGE_TO_TWISTLOCK_CONSOLE:8083/api/v1/authenticate',
                               data=json.dumps(payload), headers={"Content-Type": "application/json"})
token = authentication.json()['token']
defenders_inventory = requests.get('https://CHANGE_TO_TWISTLOCK_CONSOLE:8083/api/v1/defenders/download',
                                   headers={"Content-Type": "application/json", "Authorization": "Bearer "+token})
defeder_content = defenders_inventory.text
for line in defeder_content.split('\n'):
    if 'ip-' in line:
        line_aux = line.replace('ip-', '').replace('-','.')
        print(line_aux)
    else:
        print(line)

