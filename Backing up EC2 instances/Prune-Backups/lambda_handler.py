# Dependencies import
import boto3

# Lambda standard entry handler, the event / context are not used as this Lambda is invoked manually, or can be invoked on a schedule by Cloudwatch events
def lambda_handler(event, context):

    account_id = boto3.client('sts').get_caller_identity().get('Account')
    ec2 = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2.describe_regions()['Regions']]

    for region in regions:
        print("Region:", region)
        ec2 = boto3.client('ec2', region_name=region)
        # Only the EC2 snapshots being owned by the account owner will be worked with
        response = ec2.describe_snapshots(OwnerIds=[account_id])
        snapshots = response["Snapshots"]

        # Sort snapshots by date ascending
        snapshots.sort(key=lambda x: x["StartTime"])

        # Remove snapshots other than we want to keep (i.e. 5 most recent snapshots will remain)
        snapshots = snapshots[:-5]

        for snapshot in snapshots:
            id = snapshot['SnapshotId']
            # Only consider unattached snapshots will be shown as status available, skip the snapshots which are shown as in-use
            try:
                print("Deleting snapshot:", id)
                ec2.delete_snapshot(SnapshotId=id)
            except Exception as e:
                print("Snapshot {} in use, skipping.".format(id))
                continue
