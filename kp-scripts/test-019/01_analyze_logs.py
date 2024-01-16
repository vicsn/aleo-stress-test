# set the variables

import os
import pandas as pd
import matplotlib.pyplot as plt

val_id_sender = 1
val_id_receiver = 3

ip_sender = f"127.0.0.1:{5000+val_id_sender}"
ip_receiver = f"127.0.0.1:{5000+val_id_receiver}"

def load_validator_logs(id):
    log_file_name = f"validator-{id}.log"
    log_file_path = os.path.join(os.getcwd(), log_file_name)

    with open(log_file_path, 'r') as file:
        lines = file.readlines()

    # Assuming each line is a new entry and has a consistent format
    # We will split each line into a timestamp and a message
    data = [line.strip().split(' ', 1) for line in lines if line.strip()]

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['Timestamp', 'Message'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp'])

    return df

df_sender = load_validator_logs(val_id_sender)
df_reveicer = load_validator_logs(val_id_receiver)

def filter_requests(message, df):
    return df[df['Message'].str.contains(message)]

df_sender_filtered = filter_requests(f"Sending 'CertificateResponse' to '{ip_receiver}'", df_sender)
df_reveicer_filtered = filter_requests(f"Received 'CertificateResponse' from '{ip_sender}'", df_reveicer)

# iterate over sender filtered

time_diff_list = []

for index, row in df_sender_filtered.iterrows():
    sending_time = row['Timestamp']

    # find a row in receiver with the receiving time shortly after sending time
    df_receiver_filtered = df_reveicer_filtered[df_reveicer_filtered['Timestamp'] > sending_time]

    # get the first row
    row_receiver = df_receiver_filtered.iloc[0]

    receiving_time = row_receiver['Timestamp']

    # calculate the time difference
    time_diff = receiving_time - sending_time

    time_diff_seconds = time_diff.total_seconds()
    
    time_diff_list.append(time_diff_seconds)


print("Statistics:")
print(f"Number of requests: {len(time_diff_list)}")
print(f"Min: {min(time_diff_list)}")
print(f"Max: {max(time_diff_list)}")
print(f"Average: {sum(time_diff_list) / len(time_diff_list)}")

# std
import statistics
print(f"Standard deviation: {statistics.stdev(time_diff_list)}")

# plot
plt.hist(time_diff_list, bins=10)
plt.xlabel('Time difference in seconds')
plt.ylabel('Number of requests')
plt.title(f"Time difference between sending and receiving a certificate request")
plt.show()

a = 0