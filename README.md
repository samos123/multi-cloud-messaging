# Multi Cloud Messaging with Functions: PubSub to/from SNS

This project demonstrates how to do some simple integrations between different
cloud providers using functions. Specifically, Google Cloud Pub/Sub and AWS
SNS are integrated using Google Cloud Functions and AWS Lambda.

The Pub/Sub function is triggered when a new message is published to Pub/Sub
and publishes the message to SNS.
The Lambda function is triggered when a new message is published to SNS and
publishes the exact same message to Pub/Sub.

For both functions, the custom attribute origin is added to prevent a
broadcast storm from happening where a message gets continiously sent
between the providers. The origin keeps track of where the message came from
so we can prevent a message with origin from SNS to not be sent back again
to SNS.


## Raw notes
Create the service account
```
export PROJECT_ID=xxxxx
gcloud iam service-accounts create sns-to-pub-sub-lambda
gcloud iam service-accounts keys create gcp-key.json --iam-account sns-to-pub-sub-lambda@$PROJECT_ID.iam.gserviceaccou
nt.com
chmod 755 gcp-key.json # needed otherwise lambda throws permission denied
# add pub/sub publisher to service account
```
