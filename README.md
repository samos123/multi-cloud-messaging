# MultiCloud Msging w/ Functions: PubSub to/from SNS

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

Create a lambda function named `sns-to-pub-sub`

Run the script to package the lambda function and dependencies:
```
./package-lambda.sh
```
