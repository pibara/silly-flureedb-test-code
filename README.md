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

```
### script result
```bash
#!/bin/sh
echo "##########################################"
echo "########     TESTING JS -> JS     ########"
./generate-signature.js |./validate-signature.js
echo "####### TESTING PYTHON1 -> PYTHON1 #######"
./generate-signature.py |./validate-signature.py
echo "####### TESTING PYTHON2 -> PYTHON2 #######"
./generate-signature-nobitcoinlib.py |./validate-signature-nobitcoinlib.py
echo "####### TESTING PYTHON1 -> PYTHON2 #######"
./generate-signature.py |./validate-signature-nobitcoinlib.py
echo "####### TESTING PYTHON2 -> PYTHON1 #######"
./generate-signature-nobitcoinlib.py |./validate-signature.py
echo "########  TESTING JS -> PYTHON1   ########"
./generate-signature.js |./validate-signature.py
echo "########  TESTING JS -> PYTHON2   ########"
./generate-signature.js |./validate-signature-nobitcoinlib.py
echo "#######   TESTING PYTHON1 -> JS   ########"
./generate-signature.py |./validate-signature.js
echo "#######   TESTING PYTHON2 -> JS   ########"
./generate-signature-nobitcoinlib.py |./validate-signature.js
echo "################ DONE ####################"

```

```
##########################################
########     TESTING JS -> JS     ########
OK
####### TESTING PYTHON1 -> PYTHON1 #######
DEBUG: signature length 64
OK
####### TESTING PYTHON2 -> PYTHON2 #######
DEBUG: signature length 64
OK
####### TESTING PYTHON1 -> PYTHON2 #######
DEBUG: signature length 64
OK
####### TESTING PYTHON2 -> PYTHON1 #######
DEBUG: signature length 64
OK
########  TESTING JS -> PYTHON1   ########
DEBUG: signature length 48
ERROR from bitcoinlib: Signature length must be 64 bytes or 128 character hexstring
FAIL
########  TESTING JS -> PYTHON2   ########
DEBUG: signature length 48
ERROR from ecdsa lib: ('Malformed formatting of signature', MalformedSignature('Invalid length of signature, expected 64 bytes long, provided string is 48 bytes long',))
FAIL
#######   TESTING PYTHON1 -> JS   ########
FAIL: Unknown signature header
#######   TESTING PYTHON2 -> JS   ########
FAIL: Unknown signature header
################ DONE ####################
```

