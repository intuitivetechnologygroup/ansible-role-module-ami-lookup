#!/usr/bin/env python

import collections
from ansible import utils, errors
import json
import sys
from ansible.module_utils.basic import *

try:
  import boto3
except ImportError:
  raise errors.AnsibleError(
    "Can't LOOKUP(cloudformation): module boto3 is not installed")

def main():
    module = AnsibleModule(
        argument_spec = dict(
            region = dict(required=False, type='str', default='us-east-1'),
            ami_name = dict(required=True, type='str')
        )
    )

    ec2 =boto3.client('ec2', region_name=module.params.get('region'))
    resp = ec2.describe_images(
        Owners=["self"],
        Filters=[
            {"Name": "name", "Values": [ module.params.get('ami_name') ] },
            { "Name":"state","Values":["available"] }
        ]
    )
    images = {}
    for image in resp['Images']:
        images[image['CreationDate']]= image['ImageId']
    if len(images.keys()) == 0 :
        module.exit_json(
            Changed=False,
            Failed=True,
            Image=None,
            msg=(
                "Failed to find any images owned by 'self' in region '%s' under name '%s'" % (
                    module.params.get('ami_name'), module.params.get('region')
                )
            )
        )
    else:
        sorted_image_keys = sorted(images.keys() )
        most_recent_key = sorted_image_keys[-1]
        image = images[ most_recent_key ]
        module.exit_json(
            Changed=False,
            Failed=False,
            Image=image,
            AllImages=images,
            # SortedKeys =sorted_image_keys,
            msg="Most recent image was chosen from AllImages"
        )

main()
