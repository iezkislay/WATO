import pymysql
import boto3

# Database connection parameters
db_host = "ins-info.ch6tb7admtue.us-east-1.rds.amazonaws.com"
db_user = "kislay"
db_password = "Me_960866"
db_name = "ec2"

# Initialize a Boto3 EC2 client
ec2 = boto3.client('ec2', region_name='us-east-1')

# Retrieve information about the running EC2 instances
instance_info = []

# Fetch EC2 instances using filters to identify instances created by Terraform
response = ec2.describe_instances(
    Filters=[
        {"Name": "tag:CreatedWith", "Values": ["Terraform"]}
    ]
)

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instance_name = "Unnamed"
        instance_id = instance["InstanceId"]
        private_ip = instance.get("PrivateIpAddress", "N/A")
        public_ip = instance.get("PublicIpAddress", "N/A")

        # Find the "Name" tag for the instance
        for tag in instance.get("Tags", []):
            if tag["Key"] == "Name":
                instance_name = tag["Value"]
                break

        instance_info.append({
            "Name": instance_name,
            "Instance_ID": instance_id,
            "Private_IP": private_ip,
            "Public_IP": public_ip
        })

# Connect to the database
try:
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = connection.cursor()

    # Insert instance information into the table
    for info in instance_info:
        query = "INSERT INTO instance_info (Name, Instance_ID, Private_IP, Public_IP) VALUES (%s, %s, %s, %s)"
        values = (info["Name"], info["Instance_ID"], info["Private_IP"], info["Public_IP"])
        cursor.execute(query, values)

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

except Exception as e:
    print(f"Error: {e}")
