#!/usr/bin/env python

#
# Clear discovery of all WikiVoyage related info to reset and upload data again.
#

import argparse
import json

from watson_developer_cloud import DiscoveryV1

parser = argparse.ArgumentParser()
parser.add_argument('disc_config_file',
                    help='Discovery information such as username and password.')
parser.add_argument('wv_config_file', help='The WikiVoyage discovery config info.')
args = parser.parse_args()

with open(args.disc_config_file, 'r') as f:
    discovery_config = json.load(f)

with open(args.wv_config_file, 'r') as f:
    wv_config = json.load(f)

discovery = DiscoveryV1(username=discovery_config['username'],
                        password=discovery_config['password'],
                        version='2017-11-07')

env_id = wv_config['environment_id']
coll_id = wv_config['collection_id']

discovery.delete_collection(env_id, coll_id)
discovery.delete_environment(env_id)
