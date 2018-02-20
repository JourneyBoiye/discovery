#!/usr/bin/env python

#
# Adds the wikivoyage page collection to the given discovery instance and
# environment.
#

import argparse
import json

from watson_developer_cloud import DiscoveryV1

parser = argparse.ArgumentParser()
parser.add_argument('disc_config', help='Discovery configuration information.')
parser.add_argument('env_config', help='Environment configuration information.')
args = parser.parse_args()

with open(args.disc_config, 'r') as f:
    discovery_config = json.load(f)

discovery = DiscoveryV1(username=discovery_config['username'],
                        password=discovery_config['password'],
                        version='2017-11-07')

with open(args.env_config, 'r') as f:
    env_config = json.load(f)
env_id = env_config['environment_id']

col_resp = discovery.create_collection(
    env_id,
    'wikivoyage',
    description='The wvpages on this instance.'
)
col_id = col_resp['collection_id']

ids = {
    'environment_id': env_id,
    'collection_id': col_id
}

print(json.dumps(ids))
