# Continuation of test2b - query block heights of both chains




echo "block height in the larger network"
curl http://127.0.0.1:3030/testnet3/latest/height
echo " "

echo "block height in the smaller network"
curl http://127.0.0.1:3045/testnet3/latest/height
echo " "
echo " "
