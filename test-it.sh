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
