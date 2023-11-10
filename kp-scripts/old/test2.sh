# Unbond validators from the smaller network - script is not complete

# private keys
#APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH (0)
#APrivateKey1zkp2RWGDcde3efb89rjhME1VYA8QMxcxep5DShNBR6n8Yjh (1)
#APrivateKey1zkp2GUmKbVsuc1NSj28pa1WTQuZaK5f1DQJAT6vPcHyWokG (2)
#APrivateKey1zkpBjpEgLo4arVUkQmcLdKQMiAKGaHAQVVwmF8HQby8vdYs (3)
#APrivateKey1zkp3J6rRrDEDKAMMzSQmkBqd3vPbjp4XTyH7oMKFn7eVFwf (4)
#APrivateKey1zkp6w2DLUBBAGTHUK4JWqFjEHvqhTAWDB5Ex3XNGByFsWUh (5)
#APrivateKey1zkpEBzoLNhxVp6nMPoCHGRPudASsbCScHCGDe6waPRm87V1 (6)
#APrivateKey1zkpBZ9vQGe1VtpSXnhyrzp9XxMfKtY3cPopFC9ZB6EYFays (7)
#APrivateKey1zkpHqcqMzArwGX3to2x1bDVFDxo7uEWL4FGVKnstphnybZq (8)
#APrivateKey1zkp6QYrYZGxnDmwvQSg7Nw6Ye6WUeXHvs3wtj5Xa9LArc7p (9)
#APrivateKey1zkp9AZwPkk4gYUCRtkaX5ZSfBymToB7azBJHmJkSvfyfcn4 (10)
#APrivateKey1zkp2jCDeE8bPnKXKDrXcKaGQRVfoZ1WFUiVorbTwDrEv6Cg (11)
#APrivateKey1zkp7St3ztS3cag91PpyQbBffTc8YLmigCGB97Sf6bkQwvpg (12)

# addresses
# ...
#aleo1mwcjkpm5hpqapnsyddnwtmd873lz2kpp6uqayyuvstr4ky2ycv9sglne5m (12)

echo "block height in the larger network"
curl http://127.0.0.1:3030/testnet3/latest/height

echo "block height in the smaller network"
curl http://127.0.0.1:3040/testnet3/latest/height


curl http://localhost:3033/testnet3/program/credits.aleo/mapping/bonded/aleo1mwcjkpm5hpqapnsyddnwtmd873lz2kpp6uqayyuvstr4ky2ycv9sglne5m
curl http://localhost:3033/testnet3/program/credits.aleo/mapping/bonded/aleo1mwcjkpm5hpqapnsyddnwtmd873lz2kpp6uqayyuvstr4ky2ycv9sglne5m | cut -d':' -f2- | cut -d':' -f2- | sed 's/u64\\n}"//g'
snarkos developer execute credits.aleo unbond_public 100000u64 --private-key ${approver_private_key} --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast"

