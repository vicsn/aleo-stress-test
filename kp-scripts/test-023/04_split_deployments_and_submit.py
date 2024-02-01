import os

number_of_programs = 16
number_of_validators = 8

programs_per_validator = number_of_programs // number_of_validators

deployment_txt_path = os.path.join(os.getcwd(), "programs_to_deploy", "res", "deployments.txt")

deployments_split_folder_path = os.path.join(os.getcwd(), "programs_to_deploy", "res_split")

# create the folder if it does not exist
if not os.path.exists(deployments_split_folder_path):
    os.makedirs(deployments_split_folder_path)

# read deployment_txt_path
with open(deployment_txt_path, "r") as f:
    deployments = f.readlines()

deployment_counter = 0
for i in range(number_of_validators):
    deployment_path = os.path.join(deployments_split_folder_path, f"deployment_{i}.txt")
    # if the file exists, delete it
    if os.path.exists(deployment_path):
        os.remove(deployment_path)

    for j in range(programs_per_validator):
        # append deployment to deployment_path file
        with open(deployment_path, "a") as f:
            f.write(deployments[deployment_counter])
        
        deployment_counter += 1

# read ip_addresses.txt
ip_addresses_path = os.path.join(os.getcwd(), "ip_addresses.txt")
with open(ip_addresses_path, "r") as f:
    ip_addresses = f.readlines()

for i in range(number_of_validators):
    ip = ip_addresses[i].strip()
    a = 0

    # execute the command: tx-cannon batch-send --manifest programs_to_deploy/res_split/deployments_i.txt -e http://ip:3033
    cmd = f"tx-cannon batch-send --manifest programs_to_deploy/res_split/deployment_{i}.txt -e http://{ip}:3033"
    os.system(cmd)
    print(f"Executed {cmd}")

print("Done")