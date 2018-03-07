#!/usr/bin/env python
import boto3
import re
import sys
import fileinput
import os
import json
import urllib2

# IMPORTANT!
# Please not that for debugging / showcasing purposes, this utility prints a lot of debugging data,
# including the actual secrets that are extracted from parameter store. First remove the print
# statements before using this file in production!

regex = "\${ssm:([a-zA-Z0-9.\-_/]*)}";

# first find all files in which we want to replace ssm placeholders
if len(sys.argv) == 0:
    print "Please specify at least one file or directory in which to replace SSM placeholders"
    sys.exit(1)

globs = sys.argv[1:]

print "\nGLOBS:"
print globs

files = []
for glob in globs:
    if os.path.isfile(glob):
        files.append(glob)
    elif os.path.isdir(glob):
        for (root, _, filenames) in os.walk(glob):
            for filename in filenames:
                files.append(os.path.join(root, filename))
    else:
        print "ERROR: Parameter '{0}' is neither a file or a directory".format(glob)
        sys.exit(1)

print "\nFILES:"
print files

# find ssm placeholders in files
keys = []
for file in files:
    with open(file) as f:
        for line in f:
            match = re.search(regex, line)
            if match is not None:
                keys.append(match.group(1))

print "\nKEYS:"
print keys

if len(keys) == 0:
    print "No SSM placeholders were found"
    sys.exit()

# use the AWS SDK to fetch all values for the ssm keys
document = json.loads(urllib2.urlopen("http://169.254.169.254/latest/dynamic/instance-identity/document").read())
client = boto3.client('ssm', region_name=document['region'])

response = client.get_parameters(
  Names=keys,
  WithDecryption=True
)

if len(response['InvalidParameters']) > 0:
    print "Error: the following parameters were not found in parameter store:"
    print "\n".join(response['InvalidParameters'])
    sys.exit(1)

print "\nRESPONSE:"
print response

# create key => value array for easy replacement
replacements = {}
for parameter in response['Parameters']:
    replacements[parameter['Name']] = parameter['Value']

print "\nREPLACEMENTS:"
print replacements

# replace all ssm keys with the correct values
for file in files:
    for line in fileinput.input(file, inplace=1):
        match = re.search(regex, line)
        if match is not None:
            sys.stdout.write(line.replace(match.group(0), replacements[match.group(1)]))
        else:
            sys.stdout.write(line)
