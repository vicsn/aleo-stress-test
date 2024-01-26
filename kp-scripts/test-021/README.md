Leo program deployment. Use the snarkOS kp/fix/stress_test_8 branch to measure the time for transaction verification.

Steps
* cd one_million_constraint_program
* WALLETADDRESS="aleo1rhgdu77hgyqd3xjj8ucu3jj9r2krwz6mnzyd80gncr5fxcwlh5rsvzp9px"
* APPNAME=one_million_constraint_program

* leo run main 1field
* PRIVATEKEY="APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH"
* RECORD=""

For local devnet:

* snarkos developer deploy "${APPNAME}.aleo" --private-key "${PRIVATEKEY}" --query "http://127.0.0.1:3030" --path "./${APPNAME}/build/" --broadcast "http://127.0.0.1:3030/testnet3/transaction/broadcast" --priority-fee 1000000