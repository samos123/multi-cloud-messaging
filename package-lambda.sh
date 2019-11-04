#!/bin/bash


mkdir target
pip install --target ./package google-cloud-pubsub
zip -r lambda.zip sns-to-pub-sub.py gcp-key.json package
#aws lambda update-function-code --function-name sns-to-pub-sub --zip-file fileb://lambda.zip
