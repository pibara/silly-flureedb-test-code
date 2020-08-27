#!/usr/bin/python3
import hashlib
import json
import random
import time
import asn1
import base58
import ecdsa

class DbSigner:
    def __init__(self, privkey, address, db, validity=120, fuel=1000):
        if len(privkey) != 64:
            privkey = base58.b58decode(privkey).hex()
        self.private_key = ecdsa.SigningKey.from_string(bytes.fromhex(privkey), curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.auth_id = address
        self.db = db
        self.validity = validity
        self.fuel = fuel
        self.decoder =  asn1.Decoder()
    def string_signature(self, datastring):
        h = hashlib.sha256()
        h.update(datastring.encode())
        digest = h.digest()
        signature = self.private_key.sign_digest(digest)
        encoder = asn1.Encoder()
        encoder.start()
        encoder.write(signature, asn1.Numbers.OctetString)
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

privkey = "bf8a7281f43918a18a3feab41d17e84f93b064c441106cf248307d87f8a60453"
address = "1AxKSFQ387AiQUX6CuF3JiBPGwYK5XzA1A"
signer = DbSigner(privkey, address, "dla/test")
free_test(signer)
