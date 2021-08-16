# Stopping EC2 Instances Nightly

## Lambda Function

- Be sure to set the Lambda function timeout high enough (i.e. 1 minute) so that it can iterate through every instance in every region.
- Function timeout can be set from Configuration option in the Mgmt console

## CloudWatch Event Rule

Cron expression: 
```
`30 12 ? * MON-FRI *`
```
- More about how to set the Cron-expression can be referred [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)

- 6:00pm IST (UTC-5) == 12:30pm (23:00) UTC

- Lambda execution role can be created from iam.json file