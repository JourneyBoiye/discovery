#!/usr/bin/env python

#
# Query a given collection for testing purposes.
#

import argparse
import json

from watson_developer_cloud import DiscoveryV1

parser = argparse.ArgumentParser()
parser.add_argument('disc_config', help='The Discovery configuration file.')
parser.add_argument('coll_config',
                    help='Collection and information configuration.')
parser.add_argument('query', help='The query for the collection')
args = parser.parse_args()

with open(args.disc_config, 'r') as f:
    discovery_config = json.load(f)

with open(args.coll_config, 'r') as f:
    collection_config = json.load(f)

with open(args.query, 'r') as f:
    query = json.load(f)

discovery = DiscoveryV1(username=discovery_config['username'],
                        password=discovery_config['password'],
                        version='2017-11-07')

env_id = collection_config['environment_id']
coll_id = collection_config['collection_id']

result = discovery.query(env_id, coll_id, query)

print(json.dumps(result, indent=2))
