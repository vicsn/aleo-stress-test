Batch program deployment

project aborted due to changes in tx-cannon design and continued in test-023

Steps:

Set up testnet locally with one node:

snarkos start --nodisplay --dev 0 --dev-num-validators 8 --validator --logfile .logs-20240131142502/validator-0.log --metrics

tx-cannon batch-deploy --manifest programs2.txt -k APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH -e http://127.0.0.1:3030 -s abcd --threads 6

tx-cannon batch-send --manifest programs_to_deploy/res_split/deployment_0.txt -e http://18.224.199.236:3033
tx-cannon batch-send --manifest res_split/deployment_0.txt -e http://18.224.199.236:3033
