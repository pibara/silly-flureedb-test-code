#!/usr/bin/python3
from secrets import token_bytes
from ecdsa import SigningKey, SECP256k1
from hashlib import blake2b
import hashlib
import bitcoinlib
import base58

#Some helper stuff for generating our bitcoin adress without a wallet.
def _hash( msg, algo ): hash = hashlib.new( algo ); hash. update( msg ); return hash. digest()
_sha256    = lambda v: _hash( v, 'sha256' )
_ripemd160 = lambda v: _hash( v, 'ripemd160' )
def btc_genkey(salt="NOSALT"):
    if isinstance(salt,str):
        salt = salt.encode("utf8")
    h = blake2b(digest_size=32, key=salt)
    h.update(token_bytes(128))
    seed = h.digest()
    private_key = b'\x80' + seed + b'\x01'
    private_key += _sha256( _sha256( private_key ))[ :4 ]
    b58_key = base58.b58encode(private_key).decode()
    rval = bitcoinlib.keys.Key(b58_key)
    return rval

private_key = btc_genkey()
print(private_key.private_hex)
print(private_key.address())
