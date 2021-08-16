# Backing up EC2 instance volumes

## Lambda Functions

- Be sure to set the Lambda functions timeout high enough (i.e. 1.5 minute) so that it can iterate through every instance in every region.
- Function timeout can be set from Configuration option in the Mgmt console
- Use iam.json for creating IAM role for both the lambda functions 

## Create Backup

- The function can be invoked at frequency per day or other as per requirement
- Tag should be created with **backup:true** for the lambda to only work on required instances
- Logic picks up all the volumes for backing up

## Prune (delete) Backup snapshots

- Only the snapshots owned by the account owner will be selected
- 5 most recent snapshots will remain, all other snapshots which are in available state (ones attached and with status ***in-use*** will be skipped)


