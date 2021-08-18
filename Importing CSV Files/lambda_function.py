# Dependencies import
import csv
import os
import tempfile
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Movies')
s3 = boto3.client('s3')

# Lambda standard entry point, event context passed by the upload of csv file from S3 bucket
def lambda_handler(event, context):

    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        # temp dir as space for work
        with tempfile.TemporaryDirectory() as tmpdir:
            download_path = os.path.join(tmpdir, key)
            s3.download_file(source_bucket, key, download_path)
            # main func call
            items = read_csv(download_path)
	    
	    # batch_writer() provides ability to retry failed items and write items faster
            with table.batch_writer() as batch:
                for item in items:
                    batch.put_item(Item=item)

# Main func entry point
def read_csv(file):
    items = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {}
            data['Meta'] = {}
            data['Year'] = int(row['Year'])
            data['Title'] = row['Title'] or None
            data['Meta']['Length'] = int(row['Length'] or 0)
            data['Meta']['Subject'] = row['Subject'] or None
            data['Meta']['Actor'] = row['Actor'] or None
            data['Meta']['Actress'] = row['Actress'] or None
            data['Meta']['Director'] = row['Director'] or None
            data['Meta']['Popularity'] = row['Popularity'] or None
            data['Meta']['Awards'] = row['Awards'] == 'Yes'
            data['Meta']['Image'] = row['Image'] or None
            data['Meta'] = {k: v for k, v in data['Meta'].items() if v is not None}
            items.append(data)
    return items
