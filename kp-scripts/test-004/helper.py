
import subprocess
import json
import paramiko


addresses=("aleo1rhgdu77hgyqd3xjj8ucu3jj9r2krwz6mnzyd80gncr5fxcwlh5rsvzp9px" "aleo1s3ws5tra87fjycnjrwsjcrnw2qxr8jfqqdugnf0xzqqw29q9m5pqem2u4t" "aleo1ashyu96tjwe63u0gtnnv8z5lhapdu4l5pjsl2kha7fv7hvz2eqxs5dz0rg" "aleo12ux3gdauck0v60westgcpqj7v8rrcr3v346e4jtq04q7kkt22czsh808v2" "aleo1p9sg8gapg22p3j42tang7c8kqzp4lhe6mg77gx32yys2a5y7pq9sxh6wrd" "aleo1l4z0j5cn5s6u6tpuqcj6anh30uaxkdfzatt9seap0atjcqk6nq9qnm9eqf" "aleo1aukf3jeec42ssttmq964udw0efyzt77hc4ne93upsu2plgz0muqsg62t68" "aleo1y4s2sjw03lkg3htlcpg683ec2j9waprljc657tfu4wl6sd67juqqvrg04a" "aleo1xh2lnryvtzxcvlz8zzgranu6yldaq5257cac44de4v0aasgu45yq3yk3yv" "aleo19ljgqpwy98l9sz4f6ly028rl8j8r4grlnetp9e2nwt2xwyfawuxq5yd0tj" "aleo1s2tyzgqr9p95sxtj9t0s38cmz9pa26edxp4nv0s8mk3tmdzmqgzsctqhxg" "aleo1sufp275hshd7srrkxwdf7yczmc89em6e5ly933ftnaz64jlq8qysnuz88d" "aleo1mwcjkpm5hpqapnsyddnwtmd873lz2kpp6uqayyuvstr4ky2ycv9sglne5m" "aleo1khukq9nkx5mq3eqfm5p68g4855ewqwg7mk0rn6ysfru73krvfg8qfvc4dt" "aleo1masuagxaduf9ne0xqvct06gpf2tmmxzcgq5w2el3allhu9dsv5pskk7wvm" "aleo10w89dpq8tqzeghq35nxtk2k66pskxm8vhrdl3vx6r4j9hkgf2qqs3936q6")
private_keys=("APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH" "APrivateKey1zkp2RWGDcde3efb89rjhME1VYA8QMxcxep5DShNBR6n8Yjh" "APrivateKey1zkp2GUmKbVsuc1NSj28pa1WTQuZaK5f1DQJAT6vPcHyWokG" "APrivateKey1zkpBjpEgLo4arVUkQmcLdKQMiAKGaHAQVVwmF8HQby8vdYs" "APrivateKey1zkp3J6rRrDEDKAMMzSQmkBqd3vPbjp4XTyH7oMKFn7eVFwf" "APrivateKey1zkp6w2DLUBBAGTHUK4JWqFjEHvqhTAWDB5Ex3XNGByFsWUh" "APrivateKey1zkpEBzoLNhxVp6nMPoCHGRPudASsbCScHCGDe6waPRm87V1" "APrivateKey1zkpBZ9vQGe1VtpSXnhyrzp9XxMfKtY3cPopFC9ZB6EYFays" "APrivateKey1zkpHqcqMzArwGX3to2x1bDVFDxo7uEWL4FGVKnstphnybZq" "APrivateKey1zkp6QYrYZGxnDmwvQSg7Nw6Ye6WUeXHvs3wtj5Xa9LArc7p" "APrivateKey1zkp9AZwPkk4gYUCRtkaX5ZSfBymToB7azBJHmJkSvfyfcn4" "APrivateKey1zkp2jCDeE8bPnKXKDrXcKaGQRVfoZ1WFUiVorbTwDrEv6Cg" "APrivateKey1zkp7St3ztS3cag91PpyQbBffTc8YLmigCGB97Sf6bkQwvpg" "APrivateKey1zkpGcGacddZtDLRc8RM4cZb6cm3GoUwpJjSCQcf2mfeY6Do" "APrivateKey1zkp4ZXEtPR4VY7vjkCihYcSZxAn68qhr6gTdw8br95vvPFe" "APrivateKey1zkpH7XEPZDUrEBnMtq1JyCR6ipwjFQ5jiHnTCe7Z7heyxff")


def get_ec2_instances():
    cmd = "aws ec2 describe-instances --filters \"Name=instance-state-name,Values=running\" --query 'Reservations[*].Instances[*].[InstanceId, PublicIpAddress]' --output json"
    output = subprocess.check_output(cmd, shell=True)
    output = json.loads(output)
    output = output[0]
    return output



def get_block_height(IP):
    # call on IP port 3033/testnet3/latest/height
    cmd = "curl " + IP + ":3033/testnet3/latest/height"
    output = subprocess.check_output(cmd, shell=True)
    return output



def get_committee(IP):
    # call on IP port 3033/testnet3/latest/height
    cmd = "curl " + IP + ":3033/testnet3/committee/latest"
    output = subprocess.check_output(cmd, shell=True)
    output = json.loads(output)
    return output