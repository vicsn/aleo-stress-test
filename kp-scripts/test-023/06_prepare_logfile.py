# set the variables

node_number = 1

# rest of the code

import os
import pandas as pd

log_file_name = f"val-{node_number}.log"
log_file_path = os.path.join(os.getcwd(), "aws-logs", log_file_name)

# open the file as one string
with open(log_file_path, 'r') as file:
    lines = file.read()

# replace "INFO \n\nAdvanced to block" with "INFO Advanced to block"
lines = lines.replace("INFO \n\nAdvanced to block", "INFO Advanced to block")

# replace "INFO \n\Committing a subdag" with "INFO Committing a subdag"
lines = lines.replace("INFO \n\nCommitting a subdag", "INFO Committing a subdag")

# store as a new log file
new_log_file_name = f"prepared_logs.log"
new_log_file_path = os.path.join(os.getcwd(), "aws-logs", new_log_file_name)

with open(new_log_file_path, 'w') as file:
    file.write(lines)