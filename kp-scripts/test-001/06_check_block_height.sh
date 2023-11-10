#!/bin/bash

echo "block height larger network"
curl http://127.0.0.1:3030/testnet3/latest/height

echo -e "\nblock height smaller network"
curl http://127.0.0.1:3040/testnet3/latest/height