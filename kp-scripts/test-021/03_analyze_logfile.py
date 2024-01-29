# set the variables

import os
import pandas as pd
import matplotlib.pyplot as plt

num_validators = 6
tx_hashes = ["at1wj995qa03tcycw67ep25zsnfrxrwtlkveqw4jy8sx6z4uzna0ygswsx5pk"]
tx_hashes = ["at1xpxj8axvmg7zs0mwgspqe5q5kyz38ngrdly97nrsx46qyadxcqgslvejns", "at19u4v36pzsjuj79xufht8kshgkpsaecj9gx225f7p7wchm5ug0qgqje0333", "at1ct67p7qnrw59z64h5gy4pm7rsxp00d749veyc0jxvyyed692avqqnfwu4r"]
tx_hashes = ["at1x9d6gersxu6pej7kh5uezn3auth52p2frywadhkx4ftdt88umygs32g2tm"] # 1m, in aws-logs_one_dep
tx_hashes = ["at18yzwtsdhgyxrlgaxlf33p9q6wkhtygy62yq7xhfcs3x9kk29pqqsw6y5e2"] # 0.5m, in aws-logs-0.5

contraint_counts = [0, 499263, 999003]
contraint_counts = [499263]

log_folder_name = "aws-logs"





log_folder_name = "aws-logs-b"
contraint_counts = [499263]
tx_hashes = ["at1t72vzrvy5xppcvljtucpya0sh45kqhhkrpnthg680agp5xsypq9s2s3k68"]

log_folder_name = "aws-logs-c"
contraint_counts = [0]
tx_hashes = ["at18kmpfpk966876lxher2nzu07v8dtmn5ttty4c3evehfuzm3sluqq87uxz8"]

log_folder_name = "aws-logs-a"
contraint_counts = [999003]
tx_hashes = ["at107ry5d8h5vte7prqplztpnxths9kxhkc67q5m57crw869gnutq9q755eye"]
# the 0.5m tx has at1tl8cawqj2sun4tvvf44j5rdu4p4hcmxyctswue3rgcd7geecdupse8x5n6


log_folder_name = "aws-logs-d"
contraint_counts = [0, 499263, 999003]
tx_hashes = ["at18kmpfpk966876lxher2nzu07v8dtmn5ttty4c3evehfuzm3sluqq87uxz8", "at1hk4zwx9annzvf94vwy40lsrgjsmk8x9996atw6uzn0u268hf95zs53kafj", "at1ezxt6ylkp7mj6pacsqm5d4gxx50h2876vggufvlth3kq6yjcwurs902lm8"]


log_folder_name = "aws-logs"
contraint_counts = [0, 499263]
tx_hashes = ["at1cg2x58utvcqzc7yxqnswh0emdm9sl5w0j78pea4pctr5r5ngrqxq8d6l4z", "at188l30mqupe7esq09ytfye6t45kjx4r86nmm70s6eq22d6rrmj5fq77xz92"]


tx_gen_validator = 0
send_validator = 1



normal_validators = set(range(num_validators)) - set([tx_gen_validator, send_validator])
normal_validator_average_times = []

for j in range(len(tx_hashes)):
    tx_hash = tx_hashes[j]
    constraint_count = contraint_counts[j]

    validator_statistics = {}

    for i in range(num_validators):
        log_file_name = f"val-{i}.log"
        log_file_path = os.path.join(os.getcwd(), log_folder_name, log_file_name)

        with open(log_file_path, 'r') as file:
            lines = file.readlines()

        # Assuming each line is a new entry and has a consistent format
        # We will split each line into a timestamp and a message
        data = [line.strip().split('  INFO ', 1) for line in lines if line.strip()]

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=['Timestamp', 'Message'])

        # Filter rows that contain 'start checking transaction verification' or 'end checking transaction verification'
        filtered_df = df[df['Message'].str.contains('start checking transaction verification|end checking transaction verification', na=False)]

        # todo, define tx time
        tx_start_times = filtered_df[filtered_df['Message'].str.contains(f'start checking transaction verification for {tx_hash}', na=False)]
        tx_end_times = filtered_df[filtered_df['Message'].str.contains(f'end checking transaction verification for {tx_hash}', na=False)]

        # if length is not equal, throw an error and end the program
        if len(tx_start_times) != len(tx_end_times):
            print(f"Error: The number of start and end times are not equal for {log_file_name}")
            exit(1)

        time_diffs_seconds = []
        
        # compute the time differences
        for k in range(len(tx_start_times)):
            start_time = tx_start_times.iloc[k]['Timestamp']
            end_time = tx_end_times.iloc[k]['Timestamp']

            # convert to datetime
            start_time_dt = pd.to_datetime(start_time)
            end_time_dt = pd.to_datetime(end_time)
            time_diff = end_time_dt - start_time_dt
            time_diff_seconds = time_diff.total_seconds()
            time_diffs_seconds.append(time_diff_seconds)

        validator_statistics[i] = time_diffs_seconds
    
    print(f"Validator Statistics for transaction verification with {constraint_count} constraints, time in seconds")
    print(f"Devnet TX gen Validator {tx_gen_validator}: {validator_statistics[tx_gen_validator]}")
    print(f"Special TX send Validator {send_validator}: {validator_statistics[send_validator]}")
    for k in normal_validators:
        print(f"Normal validator {k}: {validator_statistics[k]}")
    
    # compute the average time for normal validators
    normal_validator_times = []
    for k in normal_validators:
        normal_validator_times.extend(validator_statistics[k])
    normal_validator_average_time = sum(normal_validator_times) / len(normal_validator_times)
    print(f"Normal Validator Average Time: {normal_validator_average_time}")

    normal_validator_average_times.append(normal_validator_average_time)


# if multiple constraints, do a linear regression of normal_validator_average_times vs contraint_counts

if(len(contraint_counts) > 1):
    plt.plot(contraint_counts, normal_validator_average_times, marker='*', linestyle='-', color='b')  # Sternchen als Marker
    plt.xlabel("Number of Constraints")
    plt.ylabel("Average Time for program deployment verification\non normal validator nodes (s)")
    plt.title("Average Time vs Number of Constraints")
    plt.show()
