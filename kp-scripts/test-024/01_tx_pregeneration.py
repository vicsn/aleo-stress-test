import os, subprocess, time, signal

# Let the user input the number of nodes (default: 4)
number_of_nodes = 4
number_of_nodes = int(input(f"Number of nodes (default: {number_of_nodes}): ") or number_of_nodes)

# Let the user input the name of the program file (default: programs_to_deploy.txt) in the programs_to_deploy fikder
program_file = "program_original.txt"
program_file = input(f"Name of the program file in the programs_to_deploy folder (default: {program_file}): ") or program_file

# Let the user input the number of program deployments to generate (default: number_of_nodes*2)
number_of_program_deployments = number_of_nodes*50
number_of_program_deployments = int(input(f"Number of program deployments to generate (default: {number_of_program_deployments}): ") or number_of_program_deployments)

# Let the user input the start index of the program deployments (default: 0)
start_index = 0
start_index = int(input(f"Start index of the program deployments (default: {start_index}): ") or start_index)

# Let the user input the number of proofs to generate in parallel (default: 2)
number_of_proofs_in_parallel = 8
number_of_proofs_in_parallel = int(input(f"Number of proofs to generate in parallel (default: {number_of_proofs_in_parallel}): ") or number_of_proofs_in_parallel)

# run the following command in the background: snarkos start --nodisplay --dev 1 --dev-num-validators number_of_nodes --validator --logfile .logs/validator-1.log --metrics
cmd = f"snarkos start --nodisplay --dev 1 --dev-num-validators {number_of_nodes} --validator --logfile .logs/validator-1.log --metrics"
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

print(f"Executed {cmd}")
print("Waiting for 1 minute")
time.sleep(30)

program_original_path = os.path.join(os.getcwd(), "programs_to_deploy", program_file)
program_original = open(program_original_path, "r").read()

generated_programs_path = os.path.join(os.getcwd(), "programs_to_deploy", "generated_programs")
# create the generated_programs folder if it does not exist
if not os.path.exists(generated_programs_path):
    os.makedirs(generated_programs_path)

def get_program_name(i):
    name = ''
    while i >= 0:
        name = chr(ord('a') + i % 26) + name
        i = i // 26 - 1
    return name

i = start_index

program_paths = []
program_indices = []

while i < start_index + number_of_program_deployments:
    num_programs_this_iteration = min(number_of_program_deployments-i, number_of_proofs_in_parallel)
    program_path = os.path.join(generated_programs_path, f"program-{i}-to-{i+num_programs_this_iteration}.txt")
    program_paths.append(program_path)
    program_indices.append((i, i+num_programs_this_iteration))

    program_file_content = ""
    for j in range(num_programs_this_iteration):
        program_file_content += program_original.replace("programname", f"program_{get_program_name(i+j)}")+"\n"

    with open(program_path, "w") as f:
        f.write(program_file_content)
    i = i+number_of_proofs_in_parallel
    a = 0

print(f"Generated {len(program_paths)} program files")
print("Now starting the transaction generation")

# devnet private keys
private_keys=["APrivateKey1zkp8CZNn3yeCseEtxuVPbDCwSyhGW6yZKUYKfgXmcpoGPWH","APrivateKey1zkp2RWGDcde3efb89rjhME1VYA8QMxcxep5DShNBR6n8Yjh","APrivateKey1zkp2GUmKbVsuc1NSj28pa1WTQuZaK5f1DQJAT6vPcHyWokG","APrivateKey1zkpBjpEgLo4arVUkQmcLdKQMiAKGaHAQVVwmF8HQby8vdYs","APrivateKey1zkp3J6rRrDEDKAMMzSQmkBqd3vPbjp4XTyH7oMKFn7eVFwf","APrivateKey1zkp6w2DLUBBAGTHUK4JWqFjEHvqhTAWDB5Ex3XNGByFsWUh","APrivateKey1zkpEBzoLNhxVp6nMPoCHGRPudASsbCScHCGDe6waPRm87V1","APrivateKey1zkpBZ9vQGe1VtpSXnhyrzp9XxMfKtY3cPopFC9ZB6EYFays","APrivateKey1zkpHqcqMzArwGX3to2x1bDVFDxo7uEWL4FGVKnstphnybZq","APrivateKey1zkp6QYrYZGxnDmwvQSg7Nw6Ye6WUeXHvs3wtj5Xa9LArc7p","APrivateKey1zkp9AZwPkk4gYUCRtkaX5ZSfBymToB7azBJHmJkSvfyfcn4","APrivateKey1zkp2jCDeE8bPnKXKDrXcKaGQRVfoZ1WFUiVorbTwDrEv6Cg","APrivateKey1zkp7St3ztS3cag91PpyQbBffTc8YLmigCGB97Sf6bkQwvpg","APrivateKey1zkpGcGacddZtDLRc8RM4cZb6cm3GoUwpJjSCQcf2mfeY6Do","APrivateKey1zkp4ZXEtPR4VY7vjkCihYcSZxAn68qhr6gTdw8br95vvPFe","APrivateKey1zkpH7XEPZDUrEBnMtq1JyCR6ipwjFQ5jiHnTCe7Z7heyxff","APrivateKey1zkpA9S3Epe8mzDnMuAXBmdxyRXgB8yp7PuMrs2teh8xNcVe","APrivateKey1zkp5neB5iVnXMTrR6y8P6wndGE9xWhQzBf3Qoht9yQ17a5o","APrivateKey1zkp4u1cUbvkC2r3n3Gz3eNzth1TvffGbFeLgaYyk8efsT4e","APrivateKey1zkpBs9zc9FChKZAkoHsf1TERcd9EQhe43NS1xuNSnyJSH1K","APrivateKey1zkp3sh4dSfCXd9g86DGHx6PAQG7WrMxE8bMbJxCrpPKSUw3","APrivateKey1zkpApK3vKdDDwbf62K5Mh7JsPNksud3ypZEXvuoYPcazStS","APrivateKey1zkp2uS6cU4M4J8z2fE3uMuQHkg87AgrMnDQ8NZzGAnpiEXm","APrivateKey1zkp8za2Nc39VHQFzBQFH6rhKuB9LqPaoVw1SgUPG8pSGAAn"]
private_keys = private_keys[:number_of_nodes]

# ensure the program_deployments folder exists
program_deployments_path = os.path.join(os.getcwd(), "program_deployments")
if not os.path.exists(program_deployments_path):
    os.makedirs(program_deployments_path)

deployment_paths = []
for i, program_path in enumerate(program_paths):
    private_key = private_keys[i % len(private_keys)]
    # use this command: tx-cannon batch-deploy --manifest program_path -k private_key -e http://127.0.0.1:3031 -s program_deployments
    cmd = f"tx-cannon batch-deploy --manifest {program_path} -k {private_key} -e http://127.0.0.1:3031 -s program_deployments"
    os.system(cmd)
    deployment_txt_path = os.path.join(program_deployments_path, "deployments.txt")
    # rename the deployment file to numbers similar to the program file
    program_index = program_indices[i]
    deployment_txt_path_new = os.path.join(program_deployments_path, f"deployment-{program_index[0]}-to-{program_index[1]}.txt")
    os.rename(deployment_txt_path, deployment_txt_path_new)
    deployment_paths.append(deployment_txt_path_new)
    print("Created deployment for", program_path)
    print("Progress:", i+1, "/", len(program_paths))

# merge all deployment files into one named "all_deployments.txt"
all_deployments_path = os.path.join(program_deployments_path, "all_deployments.txt")
with open(all_deployments_path, "w") as f:
    for deployment_path in deployment_paths:
        f.write(open(deployment_path, "r").read())

print("Created all_deployments.txt")

# stop the devnet
os.kill(process.pid, signal.SIGTERM)  # Send the SIGTERM signal to gracefully terminate the process
print("Stopped the devnet, sleep for 10 seconds")
time.sleep(10)

# run snarkos clean
cmd = f"snarkos clean"
os.system(cmd)
print("Executed", cmd)
print("Completed")