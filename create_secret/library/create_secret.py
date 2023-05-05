#!/usr/bin/python

from ansible.module_utils.basic import *

import csv
import yaml
import copy
import base64

SECRET_BASE = {
    "apiVersion": "v1",
    "stringData": {},
    "data": {},
    "kind": "Secret",
    "type": "Opaque",
    "metadata":{
        "name": "",
        "namespace": ""
    }
}

def createSecret():
    secrets = {}
    with open('secrets.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["SECRET_NAME"] not in secrets:
                secrets[row["SECRET_NAME"]] = copy.deepcopy(SECRET_BASE)
                secrets[row["SECRET_NAME"]]["metadata"]["name"] = row["SECRET_NAME"]
                secrets[row["SECRET_NAME"]]["metadata"]["namespace"] = row["NAMESPACE"]
                #secrets[row["SECRET_NAME"]]["data"][row["SECRET_KEY_REF"]] = str(base64.b64encode(bytes(row["SECRET_KEY_VALUE"], 'utf-8')), 'utf-8')
                secrets[row["SECRET_NAME"]]["stringData"][row["SECRET_KEY_REF"]] = row["SECRET_KEY_VALUE"]
            else:
                #secrets[row["SECRET_NAME"]]["data"][row["SECRET_KEY_REF"]] = str(base64.b64encode(bytes(row["SECRET_KEY_VALUE"], 'utf-8')), 'utf-8')
                secrets[row["SECRET_NAME"]]["stringData"][row["SECRET_KEY_REF"]] = row["SECRET_KEY_VALUE"]

    for key, secret in secrets.items():
        #print(secret)
        f = open('secrets.yaml', 'a+')
        yaml.dump(secret, f, allow_unicode=True)
        f.write("---\n")

    return secrets
    
def main():
    module = AnsibleModule(argument_spec={})
    secrets = createSecret()
    module.exit_json(changed=False, meta=secrets)

if __name__ == '__main__':
    main()
