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
