# Dependencies import
import boto3

# Standard lambda function entry, event / context will not be used in this case, just trigger will be received from scheduled Cloudwatch event
def lambda_handler(event, context):

    # Get list of all regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    # Iterate over each region
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)

        print("Region:", region)

        # Get only running instances in the region
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name',
                      'Values': ['running']}])

        # Stop the running instances
        for instance in instances:
            instance.stop()
            print('Stopped instance: ', instance.id)
