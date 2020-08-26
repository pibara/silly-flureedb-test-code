#!/usr/bin/node
let fluree_utils = require('@fluree/crypto-utils');
let fluree_crypto = require('@fluree/crypto-base');
let privkey = "176d072be91c9ab3013435be21af726a84c5f2d22ced506b437a5007ac2cf82d"
let pub_key = fluree_crypto.pub_key_from_private(privkey);
var fs = require('fs');
var obj = JSON.parse(fs.readFileSync(0, 'utf-8'));
var payload = obj["cmd"];
var signature = obj["sig"];
try {
    if (fluree_crypto.verify_signature(pub_key, payload, signature)) {
        console.log("OK");
    } else {
        console.log("FAIL");
    }
} 
catch (err) {
    console.log("FAIL:", err.message)
}

