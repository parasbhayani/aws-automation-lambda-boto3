# Dependencies import
import datetime
from dateutil.parser import parse
import boto3

# Func for getting time difference in days
def days_old(date):
    parsed = parse(date).replace(tzinfo=None)
    diff = datetime.datetime.now() - parsed
    return diff.days

# Lambda standard entry point, can be run via schedule in the Cloudwatch events
def lambda_handler(event, context):

    # Get list of regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    # Iterate through the regions
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        print("Region:", region)
        
        amis = ec2.describe_images(Owners=['self'])['Images']

        for ami in amis:
            creation_date = ami['CreationDate']
            age_days = days_old(creation_date)
            image_id = ami['ImageId']
            print('ImageId: {}, CreationDate: {} ({} days old)'.format(
                image_id, creation_date, age_days))

            # If AMI is more than 10 days old the image will be de-registered 
            if age_days > 10:
                print('Deleting ImageId:', image_id)

                # Deregister the AMI
                ec2.deregister_image(ImageId=image_id)
