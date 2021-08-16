# Dependencies import
from datetime import datetime
import boto3

# Lambda standard entry handler, the event / context are not used as this Lambda is invoked manually, or can be invoked on a schedule by Cloudwatch events
def lambda_handler(event, context):

    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    for region in regions:
        print('Instances in EC2 Region {0}:'.format(region))
        ec2 = boto3.resource('ec2', region_name=region)

        instances = ec2.instances.filter(
            Filters=[
                # Tag used here backup:true is very important as that is used to filters EC2 instances that require backup
                {'Name': 'tag:backup', 'Values': ['true']}
            ]
        )

        # ISO 8601 timestamp, i.e. 2019-01-31T14:01:58 for Cloudwatch logs
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat()

        for i in instances.all():
            for v in i.volumes.all():
                # Backup of Instance ID, volume xx, created at @timestamp
                desc = 'Backup of {0}, volume {1}, created {2}'.format(i.id, v.id, timestamp)
                print(desc)

                snapshot = v.create_snapshot(Description=desc)

                print("Created snapshot:", snapshot.id)
