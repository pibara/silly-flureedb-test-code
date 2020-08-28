#!/usr/bin/python3
import sys
import bitcoinlib
import hashlib
import json
import random
import time
import asn1
import base58
from ellipticcurve import ecdsa, privateKey, signature 

class DbSigner:
    def __init__(self, privkey):
        if len(privkey) != 64:
            privkey = base58.b58decode(privkey).hex()
        self.private_key = privateKey.PrivateKey.fromString(bytes.fromhex(privkey))
        self.public_key = self.private_key.publicKey()
    def string_signature_verify(self, datastring, sigstring):
        try:
            sig = signature.Signature.fromDer(bytes.fromhex(sigstring)[1:])
            rval = ecdsa.Ecdsa.verify(datastring, sig, self.public_key)
            return rval
        except Exception as exp:
            print("ERROR from ellipticcurve (starkbank-ecdsa):", exp)
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
