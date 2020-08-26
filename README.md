# silly-flureedb-test-code
Trying to figure out how to sign transactions for FlureeDB from Python, temporary repo

## Experiment for figuring out Fluree transaction signing with Python

This directory contains four scripts. A transaction signer and verifyer in python (using bitcoinlib, hashlib and asn1) and and javascript (using the crypto-utils and crypto-base libs from fluree).


Both signers are supposed to do the exact same thing.

1) Take a JSON transaction
2) Use it to create a JSON command string
3) Take the SHA2-256 hash of the command string
4) Create a ECDSA-SECP256k1 signature from the hash.
5) DER-encode the result
6) Create a command JSON containing the command and the signature.

Currently it seems either step 4 or step 5 is considerably different in the Python code than it is in je JavaScipt code.
Unfortunately the Fluree crypto-base library seems only available packed, so its kinda hard figuring out what it is doing differently from the Python code.

### Signing code

```javasctip
command = fluree_utils.signTransaction(auth_id, db, expire, fuel, nonce, privkey, data, deps);
```
vs

```python
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
        
signer = DbSigner(privkey, "mydbs/test")
command = signer.sign_transaction(data)

```
### script result

```bash
#!/bin/sh
echo "##########################################"
echo "########     TESTING JS -> JS     ########"
./generate-signature.js |./validate-signature.js
echo "######## TESTING PYTHON -> PYTHON ########"
./generate-signature.py |./validate-signature.py
echo "########   TESTING JS -> PYTHON   ########"
./generate-signature.js |./validate-signature.py
echo "########   TESTING PYTHON -> JS   ########"
./generate-signature.py |./validate-signature.js
echo "################ DONE ####################"
```

```
##########################################
########     TESTING JS -> JS     ########
OK
######## TESTING PYTHON -> PYTHON ########
DEBUG: signature length 64
OK
########   TESTING JS -> PYTHON   ########
DEBUG: signature length 48
ERROR from bitcoinlib: Signature length must be 64 bytes or 128 character hexstring
FAIL
########   TESTING PYTHON -> JS   ########
FAIL: Unknown signature header
################ DONE ####################
```
