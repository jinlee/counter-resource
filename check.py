#!/usr/local/bin/python

import sys
import json
import boto3

config = json.loads(sys.stdin.read())
source = config.get('source', {})

session = boto3.session.Session(
    aws_access_key_id       = source.get('aws_access_key_id'),
    aws_secret_access_key   = source.get('aws_secret_access_key'),
    region_name             = source.get('region')
)

obj = session.resource('s3').Object(source['bucket'], source['key'])

try:
    count = int(obj.get()['Body'].read())
except Exception:
    count = 0

res = []
for i in range(0, count + 1):
    res.append({'count': str(i)})

print json.dumps(res)

