#!/bin/bash

rm lambda.zip
rm -rf package
mkdir package
python3 -m pip install --target ./package google-cloud-pubsub
pushd package
zip -r9 ${OLDPWD}/lambda.zip .
popd
zip -g lambda.zip sns-to-pub-sub.py gcp-key.json
cp lambda.zip /mnt/chromeos/MyFiles/Downloads/
#aws lambda update-function-code --function-name sns-to-pub-sub --zip-file fileb://lambda.zip
