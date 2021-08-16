# Dependencies import
import boto3

# Lambda standard function entry point
def lambda_handler(object, context):

    # Get list of regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]
    
    # Iterate through the regions
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)
        print("Region:", region)

        # List only unattached volumes (i.e 'available' not 'in-use')
        volumes = ec2.volumes.filter(
            Filters=[{'Name': 'status', 'Values': ['available']}])

        for volume in volumes:
            v = ec2.Volume(volume.id)
            print("Deleting EBS volume: {}, Size: {} GiB".format(v.id, v.size))
            v.delete()
