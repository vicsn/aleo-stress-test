import os

deployment_dir = os.path.join(os.path.getcwd(), "deployment")

# Create the deployment directory if it doesn't exist
if not os.path.exists(deployment_dir):
    os.makedirs(deployment_dir)

# ... todo continue