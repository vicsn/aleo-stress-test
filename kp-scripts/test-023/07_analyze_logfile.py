# set the variables

import os
import pandas as pd
import matplotlib.pyplot as plt

limit_block_height = 361

node_numbers = list(range(50))

log_file_name = f"prepared_logs-0.log"
log_file_path = os.path.join(os.getcwd(), "aws-logs", log_file_name)

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

if(limit_block_height > -1):
    time_diff_list = time_diff_list[:limit_block_height]

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

# limit
if(limit_block_height > -1):
    cleaned_time_diff_seconds = cleaned_time_diff_seconds[:limit_block_height]

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
print("Number of block samples:", len(cleaned_time_diff_seconds))
print(f"Mean Time Difference: {mean_time_diff} seconds")
print(f"Standard Deviation of Time Differences: {std_time_diff} seconds")

import scipy.stats as stats

# Assuming 'cleaned_time_diff_seconds' is your data sample
n = len(cleaned_time_diff_seconds)  # sample size
mean_time_diff = sum(cleaned_time_diff_seconds) / n  # or use another method to calculate mean
std_time_diff = (sum([(x - mean_time_diff) ** 2 for x in cleaned_time_diff_seconds]) / (n-1)) ** 0.5  # sample standard deviation

# Standard error of the mean
sem = std_time_diff / n ** 0.5

# For a 95% confidence interval with large sample size, use z-score
# If the sample size is small, use t-score
if n > 30:
    z_score = stats.norm.ppf(0.975)  # for 95% confidence
else:
    z_score = stats.t.ppf(0.975, n-1)  # for 95% confidence, n-1 degrees of freedom

# Calculate the margin of error
margin_of_error = z_score * sem

# Calculate the confidence interval
confidence_interval = (mean_time_diff - margin_of_error, mean_time_diff + margin_of_error)

# Print the confidence interval
print(f"95% confidence interval of block times: {confidence_interval[0]} to {confidence_interval[1]} seconds")
