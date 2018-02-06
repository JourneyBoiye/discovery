#!/usr/bin/env python

import argparse
import json

from watson_developer_cloud import DiscoveryV1

parser = argparse.ArgumentParser()
parser.add_argument('config', help='The Discovery configuration file.')
args = parser.parse_args()

with open(args.config, 'r') as f:
    discovery_config = json.load(f)

discovery = DiscoveryV1(username=discovery_config['username'],
                        password=discovery_config['password'],
                        version='2017-11-07')

env_resp = discovery.create_environment(
    name='pages',
    description='The environment that houses wikivoyage pages.',
    size=1
)
env_id = env_resp['environment_id']

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
