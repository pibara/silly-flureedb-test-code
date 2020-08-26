#!/usr/bin/node
let fluree_utils = require('@fluree/crypto-utils');
let fluree_crypto = require('@fluree/crypto-base');
let privkey = "176d072be91c9ab3013435be21af726a84c5f2d22ced506b437a5007ac2cf82d"
let data = '[{"foo": 42, "bar": "appelvlaai"}]'
let db = "dla/demo"
let pub_key = fluree_crypto.pub_key_from_private(privkey);
let auth_id = fluree_utils.getSinFromPublicKey(pub_key);
let nonce = 2555585355567361
let expire = 1598348340937
let fuel = 100000;
let deps = null;
command = fluree_utils.signTransaction(auth_id, db, expire, fuel, nonce, privkey, data, deps);
command = JSON.stringify(command, null, '\t')
console.log(command); 

