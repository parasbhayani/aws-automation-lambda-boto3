# Dependencies import
import os
import boto3

# Environment variables, get the AMI of the desired instance by launch screen on AWS Mgmt console, Key-pair should be created before 
AMI = os.environ['AMI']
INSTANCE_TYPE = os.environ['INSTANCE_TYPE']
KEY_NAME = os.environ['KEY_NAME']
SUBNET_ID = os.environ['SUBNET_ID']

# Declare the boto3 resource for EC2
ec2 = boto3.resource('ec2')

# Lambda entry handler definition
def lambda_handler(event, context):

    instance = ec2.create_instances(
        ImageId=AMI,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        SubnetId=SUBNET_ID,
        MaxCount=1,
        MinCount=1
    )
    # Print statements can be read on the Cloudwatch console
    print("New instance created:", instance[0].id)
