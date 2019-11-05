# MultiCloud Msging w/ Functions: PubSub to/from SNS

This project demonstrates how to do some simple integrations between different
cloud providers using functions. Specifically, Google Cloud Pub/Sub and AWS
SNS are integrated using Google Cloud Functions and AWS Lambda. Whenever a
message gets published to SNS it will also be published to Pub/Sub and
vice versa as well.

The Pub/Sub function is triggered when a new message is published to Pub/Sub
and then publishes the message to SNS.
The Lambda function is triggered when a new message is published to SNS and
then publishes the exact same message to Pub/Sub.

For both functions, a custom attribute origin is added to prevent a
broadcast storm from happening where a message gets continiously sent
between the providers. The origin keeps track of where the message came from
so we can prevent a message with origin from SNS to not be sent back again
to SNS.

A topic called `multi-cloud-messaging` was created both in SNS and in Pub/Sub.
This guide only contains the steps needed to deploy the functions.

The code `sns-to-pub-sub.py` is run in AWS Lambda. The code in the `pub-sub-to-sns`
directory is run in Google Cloud Functions. In AWS Lambda, a service account
is used to authenticate with Pub/Sub. In Functions, an AWS account was created
that only has the `SNS:Publish` permission.

The estimated cost of this setup is free up to 1M requests per month. Please
do your own estimation to ensure you don't go over budget.

## GCP Setup
Create the service account and download the key
```
export PROJECT_ID=xxxxx
gcloud iam service-accounts create sns-to-pub-sub-lambda
gcloud iam service-accounts keys create gcp-key.json \
    --iam-account sns-to-pub-sub-lambda@$PROJECT_ID.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:sns-to-pub-sub-lambda@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/pubsub.publisher
# needed otherwise lambda throws permission denied
chmod 755 gcp-key.json
```

## Deploy to AWS Lambda
Lambda requires you to package your source and all dependencies as a ZIP file.
Also note that Python 3.7 is required. If you try to package the Google Cloud
libraries on a smaller Python version it will fail.

Create a lambda function named `sns-to-pub-sub`.

Run the script to package and deploy the lambda function with dependencies:
```
./package-lambda.sh
```

## Deploy to Google Cloud Functions
```
gcloud functions deploy pub-sub-to-sns --region us-east1 \
    --entry-point handler --runtime python37 --source pub-sub-to-sns \
    --env-vars-file aws-secrets.yaml --trigger-topic multi-cloud-messaging
```
