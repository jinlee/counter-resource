#!/usr/local/bin/python

import json
import sys

config = json.loads(sys.stdin.read())
version = config.get('version', {})
params = config.get('params', {})

count = int(version['count'])
if params.get('inc', False):
    count = count + 1
count = str(count)

path = "%s/count" % sys.argv[1]
with open(path, 'w') as f:
    f.write(count)

res = {'version': {'count': count } }
print json.dumps(res)

