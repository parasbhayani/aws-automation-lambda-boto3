# Dependencies import
import os
import tempfile
import boto3

# Dependency library for Image manipulation to be uploaded as .zip
from PIL import Image

# Setting Destination bucket as env variable
DEST_BUCKET = os.environ['DEST_BUCKET']
SIZE = 128, 128

s3 = boto3.client('s3')

# Lambda standard entry point, event source s3 upload of input image
def lambda_handler(event, context):

    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        thumb = 'thumb-' + key

        with tempfile.TemporaryDirectory() as tmpdir:
            download_path = os.path.join(tmpdir, key)
            upload_path = os.path.join(tmpdir, thumb)
            s3.download_file(source_bucket, key, download_path)
            generate_thumbnail(download_path, upload_path)
            s3.upload_file(upload_path, DEST_BUCKET, thumb)

        # Message for Cloudwatch logs
        print('Thumbnail image saved at {}/{}'.format(DEST_BUCKET, thumb))

# Func to generate thumbnail by PIL lib, as per SIZE input
def generate_thumbnail(source_path, dest_path):
    print('Generating thumbnail from:', source_path)
    with Image.open(source_path) as image:
        image.thumbnail(SIZE)
        image.save(dest_path)
