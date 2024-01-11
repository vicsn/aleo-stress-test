# set the variables

import os
import pandas as pd
import matplotlib.pyplot as plt


log_file_name = f"prepared_logs.log"
log_file_path = os.path.join(os.getcwd(), log_file_name)

with open(log_file_path, 'r') as file:
    lines = file.readlines()

# Assuming each line is a new entry and has a consistent format
# We will split each line into a timestamp and a message
data = [line.strip().split('  INFO ', 1) for line in lines if line.strip()]

# Convert to DataFrame
df = pd.DataFrame(data, columns=['Timestamp', 'Message'])

# Filter rows that contain 'Advanced to block'
block_df = df[df['Message'].str.contains('Advanced to block', na=False)]

# Now, block_df contains only the rows with block time information
# Let's extract and print the timestamps
block_times = block_df['Timestamp']

block_times_dt = pd.to_datetime(block_times)

time_differences = block_times_dt.diff()

time_differences_seconds = time_differences.dt.total_seconds()

time_diff_list = time_differences_seconds.tolist()

# Create a line plot
plt.figure(figsize=(12, 7))  # Set figure size
plt.plot(time_diff_list, marker='o')  # 'o' creates dots at each data point
plt.title('Time Differences Between Consecutive Blocks')
plt.xlabel('Block Index (of block where we are coming from)')
plt.ylabel('Time Difference (seconds)')
plt.grid(True)
plt.savefig("line_plot.png")  # Save the plot as a PNG file
plt.show()



# Remove NaN values from time differences
cleaned_time_diff_seconds = time_differences_seconds.dropna()

# Plotting the distribution of time differences
plt.figure(figsize=(12, 7))  # Set figure size
plt.hist(cleaned_time_diff_seconds, bins=20, alpha=0.7, color='blue')
plt.title('Distribution of Time Differences Between Consecutive Blocks')
plt.xlabel('Time Difference (seconds)')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig("histogram_plot.png")  # Save the plot as a PNG file
plt.show()

# Calculate mean and standard deviation
mean_time_diff = cleaned_time_diff_seconds.mean()
std_time_diff = cleaned_time_diff_seconds.std()

# Print the mean and standard deviation
print(f"Mean Time Difference: {mean_time_diff} seconds")
print(f"Standard Deviation of Time Differences: {std_time_diff} seconds")
