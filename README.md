# multi-cloud-messaging


Create the service account

```
gcloud iam service-accounts create sns-to-pub-sub-lambda
gcloud iam service-accounts keys create gcp-key.json --iam-account sns-to-pub-sub-lambda@$PROJECT_ID.iam.gserviceaccou
nt.com
```
