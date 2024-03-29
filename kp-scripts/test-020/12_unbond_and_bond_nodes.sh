#!/bin/bash

addresses=("aleo1rhgdu77hgyqd3xjj8ucu3jj9r2krwz6mnzyd80gncr5fxcwlh5rsvzp9px" "aleo1s3ws5tra87fjycnjrwsjcrnw2qxr8jfqqdugnf0xzqqw29q9m5pqem2u4t" "aleo1ashyu96tjwe63u0gtnnv8z5lhapdu4l5pjsl2kha7fv7hvz2eqxs5dz0rg" "aleo12ux3gdauck0v60westgcpqj7v8rrcr3v346e4jtq04q7kkt22czsh808v2" "aleo1p9sg8gapg22p3j42tang7c8kqzp4lhe6mg77gx32yys2a5y7pq9sxh6wrd" "aleo1l4z0j5cn5s6u6tpuqcj6anh30uaxkdfzatt9seap0atjcqk6nq9qnm9eqf" "aleo1aukf3jeec42ssttmq964udw0efyzt77hc4ne93upsu2plgz0muqsg62t68" "aleo1y4s2sjw03lkg3htlcpg683ec2j9waprljc657tfu4wl6sd67juqqvrg04a" "aleo1xh2lnryvtzxcvlz8zzgranu6yldaq5257cac44de4v0aasgu45yq3yk3yv" "aleo19ljgqpwy98l9sz4f6ly028rl8j8r4grlnetp9e2nwt2xwyfawuxq5yd0tj" "aleo1s2tyzgqr9p95sxtj9t0s38cmz9pa26edxp4nv0s8mk3tmdzmqgzsctqhxg" "aleo1sufp275hshd7srrkxwdf7yczmc89em6e5ly933ftnaz64jlq8qysnuz88d" "aleo1mwcjkpm5hpqapnsyddnwtmd873lz2kpp6uqayyuvstr4ky2ycv9sglne5m" "aleo1khukq9nkx5mq3eqfm5p68g4855ewqwg7mk0rn6ysfru73krvfg8qfvc4dt" "aleo1masuagxaduf9ne0xqvct06gpf2tmmxzcgq5w2el3allhu9dsv5pskk7wvm" "aleo10w89dpq8tqzeghq35nxtk2k66pskxm8vhrdl3vx6r4j9hkgf2qqs3936q6"  "aleo1sfu3p7g8rppusft8re7v88ujjhz5sx6pwc5609vdgnr0pdmhkyyqrrsjkm"  "aleo1ry0wc384qthrdna5xtzsjqvxg42zwfezpna6keeqa6netv3qmyxszhh8z8"  "aleo1ps4dhhfn5vgfj9lyjra2xnv9a8cc2a2l9jnr585h6tvj4gnlqgfqyszcv3"  "aleo15a34a3dtpj879frvndndp0605vqnxsfdedwyrtu5u6xfd7fv5ufqryavc4"  "aleo1mpn4enrfm2dqjg8lqh09t2zcatkujq3qr3kq8kcnrd7uaqrc3c9qngcp5l"  "aleo1axy39ux5lhaypf039zp7fuhg57qkfqtafu2fa3e2vwgqugeq05qsm2kfl4"  "aleo1zzpl369camggvj5qm2nhnpfhe3epcera3xvdra4ze7scg35zmuzsl7kwyh"  "aleo1j2fhcu3qkvn4k0vrf53jmuv8d0fz5guz9tzdy0egjjjttdhsxszqfdfwfk")
private_keys=("APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH" "APrivateKey1zkp2RWGDcde3efb89rjhME1VYA8QMxcxep5DShNBR6n8Yjh" "APrivateKey1zkp2GUmKbVsuc1NSj28pa1WTQuZaK5f1DQJAT6vPcHyWokG" "APrivateKey1zkpBjpEgLo4arVUkQmcLdKQMiAKGaHAQVVwmF8HQby8vdYs" "APrivateKey1zkp3J6rRrDEDKAMMzSQmkBqd3vPbjp4XTyH7oMKFn7eVFwf" "APrivateKey1zkp6w2DLUBBAGTHUK4JWqFjEHvqhTAWDB5Ex3XNGByFsWUh" "APrivateKey1zkpEBzoLNhxVp6nMPoCHGRPudASsbCScHCGDe6waPRm87V1" "APrivateKey1zkpBZ9vQGe1VtpSXnhyrzp9XxMfKtY3cPopFC9ZB6EYFays" "APrivateKey1zkpHqcqMzArwGX3to2x1bDVFDxo7uEWL4FGVKnstphnybZq" "APrivateKey1zkp6QYrYZGxnDmwvQSg7Nw6Ye6WUeXHvs3wtj5Xa9LArc7p" "APrivateKey1zkp9AZwPkk4gYUCRtkaX5ZSfBymToB7azBJHmJkSvfyfcn4" "APrivateKey1zkp2jCDeE8bPnKXKDrXcKaGQRVfoZ1WFUiVorbTwDrEv6Cg" "APrivateKey1zkp7St3ztS3cag91PpyQbBffTc8YLmigCGB97Sf6bkQwvpg" "APrivateKey1zkpGcGacddZtDLRc8RM4cZb6cm3GoUwpJjSCQcf2mfeY6Do" "APrivateKey1zkp4ZXEtPR4VY7vjkCihYcSZxAn68qhr6gTdw8br95vvPFe" "APrivateKey1zkpH7XEPZDUrEBnMtq1JyCR6ipwjFQ5jiHnTCe7Z7heyxff"  "APrivateKey1zkpA9S3Epe8mzDnMuAXBmdxyRXgB8yp7PuMrs2teh8xNcVe"  "APrivateKey1zkp5neB5iVnXMTrR6y8P6wndGE9xWhQzBf3Qoht9yQ17a5o"  "APrivateKey1zkp4u1cUbvkC2r3n3Gz3eNzth1TvffGbFeLgaYyk8efsT4e"  "APrivateKey1zkpBs9zc9FChKZAkoHsf1TERcd9EQhe43NS1xuNSnyJSH1K"  "APrivateKey1zkp3sh4dSfCXd9g86DGHx6PAQG7WrMxE8bMbJxCrpPKSUw3"  "APrivateKey1zkpApK3vKdDDwbf62K5Mh7JsPNksud3ypZEXvuoYPcazStS"  "APrivateKey1zkp2uS6cU4M4J8z2fE3uMuQHkg87AgrMnDQ8NZzGAnpiEXm"  "APrivateKey1zkp8za2Nc39VHQFzBQFH6rhKuB9LqPaoVw1SgUPG8pSGAAn")





while :
do
    for i in {6..9}
    do
        echo "unbonding node ${i}"
        snarkos developer execute credits.aleo unbond_public 1200000000000u64 --private-key ${private_keys[i]} --query "http://127.0.0.1:3033" --broadcast "http://127.0.0.1:3033/testnet3/transaction/broadcast"
    done

    sleep 30

    for i in {6..9}
    do
        echo "bonding node ${i}"                                           
        snarkos developer execute credits.aleo bond_public ${addresses[i]} 1200000000000u64 --private-key ${private_keys[i]} --query "http://127.0.0.1:3033" --broadcast "http://127.0.0.1:3033/testnet3/transaction/broadcast"
    done

    sleep 40


done









