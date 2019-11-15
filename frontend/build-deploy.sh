#!/bin/bash

set -x

gcloud builds submit --tag gcr.io/$PROJECT_ID/messaging
gcloud beta run deploy messaging --image gcr.io/$PROJECT_ID/messaging \
    --platform managed --set-env-vars="TOKEN=$TOKEN" --max-instances 1
