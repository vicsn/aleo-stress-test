# ToDo split the network into f and 2f+1

spender_tester_private_key="APrivateKey1zkp4aaUAYt2uuQzNXenZTTnv8jts1efQjv8XboJMU2y1NrP"
spender_tester_view_key="AViewKey1jGCzaWqEZQDejdsB41detVWR6qWKqaLptDjUHAirVoYv"
spender_tester_address="aleo1vl0zuh5lun7mgsutnnegh40dv5tz2dz00uydlkegdgmsc7tlwupqlm25l6"

spender_tester_private_key2a="APrivateKey1zkpAA2PHBdPDwJxo7K9qiyMykz9tenBw7Fjy5WKrytRd7jo"
spender_tester_view_key2a="AViewKey1hi36prBGKFh4sUsZYPJSw2MjNBmry6GRb6qhEQS1eyRA"
spender_tester_address2a="aleo1tdr35vnju3c5yqcmlyph6s9fqdcv9m0sj3ct38dq0jdmktl6evyq7r3swh"

spender_tester_private_key2b="APrivateKey1zkpHKeL7kC9gTkPXnUzmuv4KrhpdiPqAM1fSToemUxZ1BxD"
spender_tester_view_key2b="AViewKey1eu5oeiD5xYTKHVQbHnGzAKnfEF7TirWMhPYZmUMjuZeZ"
spender_tester_address2b="aleo1smz425h257n5g0lla5dnes5s30f3rcuhgftvvnzr8a4kmusr8qysvysyaz"

# Scan for the record
records=$(snarkos developer scan -v ${spender_tester_view_key} --start 0 --endpoint "http://localhost:3030")
echo ${records}
first_record=$(echo $records | jq -j '.[0]')

echo "found record: " $first_record













## Spend record once
snarkos developer execute credits.aleo transfer_private "${first_record}" ${spender_tester_address2a} 1000000000u64 --private-key ${spender_tester_private_key} --query "http://localhost:3030" --broadcast "http://localhost:3030/testnet3/transaction/broadcast"

## Spend record another time on the other network
snarkos developer execute credits.aleo transfer_private "${first_record}" ${spender_tester_address2b} 1000000000u64 --private-key ${spender_tester_private_key} --query "http://localhost:3040" --broadcast "http://localhost:3040/testnet3/transaction/broadcast"



## unbond so the little network can produce blocks

## merge the network

