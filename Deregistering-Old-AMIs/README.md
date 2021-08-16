# De-registering old AMIs

- This Lambda handler goes over the AMIs more than 10 days old, and de-registers them
- It can be run via a Cloudwatch event on schedule
- Only the AMIs owned by the account will be considered for de-registration