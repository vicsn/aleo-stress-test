#!/bin/bash

echo "block height for validator 0"
curl http://127.0.0.1:3030/testnet3/latest/height

echo ""

echo "block height for validator 2"
curl http://127.0.0.1:3032/testnet3/latest/height

echo ""

echo "block height for validator 4"
curl http://127.0.0.1:3034/testnet3/latest/height