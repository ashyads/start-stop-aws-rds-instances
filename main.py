import sys
import boto3

# AWS credentials
AWS_SERVER_PUBLIC_KEY = ""  # Replace with your AWS access key
AWS_SERVER_SECRET_KEY = ""  # Replace with your AWS secret access key
AWS_REGION = ""  # Replace with your desired AWS region

# Create a session using the AWS credentials
session = boto3.Session(
    aws_access_key_id=AWS_SERVER_PUBLIC_KEY,
    aws_secret_access_key=AWS_SERVER_SECRET_KEY,
)

region = AWS_REGION

# Create an RDS client using the session and region
client = session.client('rds', region_name=region)

# List of RDS instance names that you want to start or stop
ON_OFF_DB_INSTANCES = ['test-db']

# Get the action from the command line arguments (first argument)
action = sys.argv[1]

# Function to start an RDS instance
def start_rds_instance(db_instance_name):
    client.start_db_instance(DBInstanceIdentifier=db_instance_name)
    print("Started RDS instance:", db_instance_name)

# Function to stop an RDS instance
def stop_rds_instance(db_instance_name):
    client.stop_db_instance(DBInstanceIdentifier=db_instance_name)
    print("Stopped RDS instance:", db_instance_name)

# Loop through each RDS instance and perform the specified action
for instance in ON_OFF_DB_INSTANCES:
    try:
        if action == "START":
            # Check if the instance is not already running
            response = client.describe_db_instances(DBInstanceIdentifier=instance)
            if response['DBInstances'][0]['DBInstanceStatus'] != 'available':
                # Start the instance if it's not running
                start_rds_instance(instance)
            else:
                print(f"RDS instance {instance} is already running.")
        elif action == "STOP":
            # Check if the instance is not already stopped
            response = client.describe_db_instances(DBInstanceIdentifier=instance)
            if response['DBInstances'][0]['DBInstanceStatus'] != 'stopped':
                # Stop the instance if it's not stopped
                stop_rds_instance(instance)
            else:
                print(f"RDS instance {instance} is already stopped.")
        else:
            print("Invalid action. Please specify either 'START' or 'STOP' in the command line.")
    except Exception as e:
        print(str(e))
