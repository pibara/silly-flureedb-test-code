#!/usr/bin/python3
import sys
import hashlib
import json
import random
import time
import asn1
import base58
import ecdsa

class DbSigner:
    def __init__(self, privkey, address):
        if len(privkey) != 64:
            privkey = base58.b58decode(privkey).hex()
        self.private_key = ecdsa.SigningKey.from_string(bytes.fromhex(privkey), curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.auth_id = address
        self.decoder =  asn1.Decoder()
    def string_signature_verify(self, datastring, sigstring):
        h = hashlib.sha256()
        h.update(datastring.encode())
        digest = h.digest()
        sigbytes = bytes.fromhex(sigstring)
        self.decoder.start(sigbytes)
        tag, value = self.decoder.read()
        print("DEBUG: signature length", len(value))
        try:
            rval = self.public_key.verify_digest(value, digest)
            return rval
        except Exception as exp:
            print("ERROR from ecdsa lib:", exp)
            return False

def process_stdin(privkey):
    obj = json.loads(sys.stdin.read())
    cmd = obj["cmd"]
    sig = obj["sig"]
    obj = json.loads(cmd)
    address = obj["auth"]
    signer = DbSigner(privkey, address)
    if signer.string_signature_verify(cmd, sig):
        print("OK")
    else:
        print("FAIL")


privkey = "bf8a7281f43918a18a3feab41d17e84f93b064c441106cf248307d87f8a60453"
process_stdin(privkey)
