#!/usr/bin/python3
import sys
import bitcoinlib
from ecdsa import SigningKey, SECP256k1
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
    def string_signature_verify(self, datastring, sigstring):
        h = hashlib.sha256()
        h.update(datastring.encode())
        digest = h.digest()
        sigbytes = bytes.fromhex(sigstring)
        self.decoder.start(sigbytes)
        tag, value = self.decoder.read()
        print("DEBUG: signature length", len(value))
        try:
            rval = bitcoinlib.keys.verify(digest, value, self.public_key)
            return rval
        except bitcoinlib.keys.BKeyError as exp:
            print("ERROR from bitcoinlib:", exp)
            return False

def process_stdin(signer):
    obj = json.loads(sys.stdin.read())
    cmd = obj["cmd"]
    sig = obj["sig"]
    if signer.string_signature_verify(cmd, sig):
        print("OK")
    else:
        print("FAIL")


privkey = "176d072be91c9ab3013435be21af726a84c5f2d22ced506b437a5007ac2cf82d"
signer = DbSigner(privkey, "dla/test")
process_stdin(signer)
