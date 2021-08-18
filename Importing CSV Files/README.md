# Transforming CSV to JSON for DynamoDB

- Create the `DynamoDB` table using the aws cli command below,

- Table details,<br>
    Table name: `Movies`<br>
    Partition key: `Year`<br>
    Sort key: `Title`<br>
    (Please visit the .csv file sample data for more reference)

```
aws dynamodb create-table \
    --table-name Music \
    --attribute-definitions \
        AttributeName=Year,AttributeType=S \
        AttributeName=Title,AttributeType=S \
    --key-schema \
        AttributeName=Year,KeyType=HASH \
        AttributeName=Title,KeyType=RANGE \
--provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5
```

- The table would be created asynchronously, wait for it to be created

- We will use the `csv library` to read the contents of the input csv file and converting it to the dict format for Python which can be pushed to Movies DynamoDB table

- `batch_writer()` provides the capability to write failed items back and uploading items faster in DynamoDB

- `iam.json` will be used to create the IAM role for the lambda func

- S3 upload of csv file act as a trigger for the Lambda function


