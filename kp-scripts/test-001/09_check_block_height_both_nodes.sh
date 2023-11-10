#!/bin/bash

echo "block height on an old larger network node"
curl http://127.0.0.1:3030/testnet3/latest/height

echo -e "\nblock height on an old smaller network node"
curl http://127.0.0.1:3040/testnet3/latest/height