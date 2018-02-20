#!/usr/bin/env python

#
# Deletes all collections off of an environment and discovery node that is
# provided in a configuration file.
#

import argparse
import json

from watson_developer_cloud import DiscoveryV1

parser = argparse.ArgumentParser()
parser.add_argument('disc_config', help='Discovery configuration information.')
parser.add_argument('env_config', help='Environment configuration information.')
args = parser.parse_args()

# TODO: Move into method.
# TODO: Move configuration into class.
with open(args.disc_config, 'r') as f:
    discovery_config = json.load(f)

discovery = DiscoveryV1(username=discovery_config['username'],
                        password=discovery_config['password'],
                        version='2017-11-07')

with open(args.env_config, 'r') as f:
    env_config = json.load(f)

env_id = env_config['environment_id']
collections_resp = discovery.list_collections(env_id)
coll_ids = [col['collection_id'] for col in collections_resp['collections']]

for coll_id in coll_ids:
    discovery.delete_collection(env_id, coll_id)
