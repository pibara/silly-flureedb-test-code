#!/usr/bin/python3
import sys
import bitcoinlib
import hashlib
import json
import random
import time
import asn1
import base58

class DbSigner:
    def __init__(self, privkey):
        if len(privkey) != 64:
            privkey = base58.b58decode(privkey).hex()
        self.private_key = bitcoinlib.keys.Key(privkey)
        self.public_key = self.private_key.public()
        self.auth_id = self.private_key.address()
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


privkey = "bf8a7281f43918a18a3feab41d17e84f93b064c441106cf248307d87f8a60453"
signer = DbSigner(privkey)
process_stdin(signer)
