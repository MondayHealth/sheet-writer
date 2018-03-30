#!/usr/bin/env bash

rm -rf ./package.zip
zip -9 -r package main.py s_private_key.json
pushd venv/lib/python3.6/site-packages/
zip -9 -ur \
    --exclude=*__pycache__* \
    --exclude=*setuptools* \
    --exclude=*pip* \
    --exclude=*easy-install* \
    ../../../../package *
popd

echo "Pushing lambda function"

aws lambda update-function-code \
    --function-name writeToSpreadSheet \
    --zip-file fileb://package.zip

echo "Done"
