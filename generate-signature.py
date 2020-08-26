#!/usr/bin/python3
import bitcoinlib
import hashlib
import json
import random
import time
import asn1
import base58

class DbSigner:
    def __init__(self, privkey, db, validity=120, fuel=1000):
        if len(privkey) != 64:
            privkey = base58.b58decode(privkey).hex()
        self.private_key = bitcoinlib.keys.Key(privkey)
        self.public_key = self.private_key.public()
        self.auth_id = self.private_key.address()
        self.db = db
        self.validity = validity
        self.fuel = fuel
        self.decoder =  asn1.Decoder()
    def string_signature(self, datastring):
        h = hashlib.sha256()
        h.update(datastring.encode())
        digest = h.digest()
        signature = bitcoinlib.keys.sign(digest, self.private_key)
        encoder = asn1.Encoder()
        encoder.start()
        encoder.write(signature.bytes(), asn1.Numbers.OctetString)
        encoded_bytes = encoder.output()
        command = dict()
        command["cmd"] = datastring
        command["sig"] = encoded_bytes.hex()
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

privkey = "176d072be91c9ab3013435be21af726a84c5f2d22ced506b437a5007ac2cf82d"
signer = DbSigner(privkey, "dla/test")
free_test(signer)
