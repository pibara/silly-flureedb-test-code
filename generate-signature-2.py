#!/usr/bin/python3
import hashlib
import json
import random
import time
import base58
import eth_keys
from ellipticcurve import privateKey, ecdsa

class DbSigner:
    def __init__(self, privkey, address, db, validity=120, fuel=1000):
        if len(privkey) != 64:
            privkey = base58.b58decode(privkey).hex()
        self.private_key = privateKey.PrivateKey.fromString(bytes.fromhex(privkey))
        self.public_key = self.private_key.publicKey()
        self.auth_id = address
        self.db = db
        self.validity = validity
        self.fuel = fuel
    def string_signature(self, datastring):
        sig = ecdsa.Ecdsa.sign(datastring, self.private_key)
        derstring = sig.toDer()
        toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])
        hexder = toHex(derstring)
        command = dict()
        command["cmd"] = datastring
        command["sig"] = "1b" + hexder
        return command
    def obj_signature(self, obj):
        rval =  self.string_signature(json.dumps(obj))
        return rval
    def sign_transaction(self, transaction):
        obj = dict()
        obj["type"] = "tx"
        obj["tx"] = [] # Fixme
        obj["db"] = self.db
        obj["auth"] = self.auth_id
        obj["fuel"] = self.fuel
        nonce = random.randint(0,9007199254740991)
        obj["nonce"] = nonce
        obj["expire"] = int(time.time() + self.validity)
        rval = self.obj_signature((obj))
        return rval

def free_test(signer):
    data = '[{"foo": 42, "bar": "appelvlaai"}]'
    command = signer.sign_transaction(data)
    command = json.dumps(command, indent=4, sort_keys=True)
    print(command);

privkey = "bf8a7281f43918a18a3feab41d17e84f93b064c441106cf248307d87f8a60453"
address = "1AxKSFQ387AiQUX6CuF3JiBPGwYK5XzA1A"
signer = DbSigner(privkey, address, "dla/test")
free_test(signer)
