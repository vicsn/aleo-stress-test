#!/bin/bash

echo "enforce block production in the smaller network"
curl http://127.0.0.1:3039/testnet3/validation/start
curl http://127.0.0.1:3039/testnet3/validation/force

curl http://127.0.0.1:3040/testnet3/validation/start
curl http://127.0.0.1:3040/testnet3/validation/force

curl http://127.0.0.1:3041/testnet3/validation/start
curl http://127.0.0.1:3041/testnet3/validation/force

curl http://127.0.0.1:3042/testnet3/validation/start
curl http://127.0.0.1:3042/testnet3/validation/force