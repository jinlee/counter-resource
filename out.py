#!/usr/local/bin/python

import sys
import json
import boto3

config = json.loads(sys.stdin.read())
source = config.get('source', {})
params = config.get('params', {})

session = boto3.session.Session(
    aws_access_key_id       = source.get('aws_access_key_id'),
    aws_secret_access_key   = source.get('aws_secret_access_key'),
    region_name             = source.get('region')
)

path = "%s/%s" % (sys.argv[1], params['file'])

obj = session.resource('s3').Object(source['bucket'], source['key'])
obj.upload_file(path)

with open(path, 'r') as f:
    res = {'version': {'count': f.read() } }
    print json.dumps(res)

