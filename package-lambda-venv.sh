#!/bin/bash

set -xe

# make sure you have python 3.7 in your venv
rm lambda-venv.zip
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
python3 -m pip install google-cloud-pubsub
pushd .venv/lib/python3.7/site-packages
zip -r9 ${OLDPWD}lambda-venv.zip .
popd
zip -g lambda-venv.zip sns-to-pub-sub.py gcp-key.json
cp lambda-venv.zip /mnt/chromeos/MyFiles/Downloads/
#aws lambda update-function-code --function-name sns-to-pub-sub --zip-file fileb://lambda.zip
