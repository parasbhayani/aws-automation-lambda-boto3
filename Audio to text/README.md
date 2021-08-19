# Transcribing Audio

- Here we will be using two lambda func:
1. Transcribe
2. Parse

- First lambda function creates a Transcribe job to convert audio file into a JSON formatted output
- Second lambda function waits for Transcribe job to complete (async trigger) via Cloudwatch events, and triggers to extract audio speech to text file output

- `iam.json` will be used in both the lambda func folders to create the IAM role for them respectively

- You may use any sample input file with `en-US` in `.mp3` format for convert it to speech output for the same

- Intermediate output from first lambda func is as `asrOutput.json` file which will used as input by second lambda func