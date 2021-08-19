# Dependencies import
import json
import os
import urllib.request
import boto3

# Mention output bucket name as env variable to store output text file
BUCKET_NAME = os.environ["BUCKET_NAME"]
s3 = boto3.resource('s3')
transcribe = boto3.client('transcribe')

# Lambda standard entry with event context of Transcribe job completion from Cloudwatch event
def lambda_handler(event, context):
    job_name = event['detail']['TranscriptionJobName']
    job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print(uri)

    # Using json lib to load contents of the output
    content = urllib.request.urlopen(uri).read().decode('UTF-8')
    print(json.dumps(content))
    data = json.loads(content)
    text = data['results']['transcripts'][0]['transcript']
    object = s3.Object(BUCKET_NAME, job_name + '-asrOutput.txt')
    object.put(Body=text)