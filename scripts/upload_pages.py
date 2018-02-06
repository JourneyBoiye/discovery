#!/usr/bin/env python

#
# Upload *.json pages in the provided folder to discovery with the provided
# credentials.
#

import argparse
import json
import os

from watson_developer_cloud import DiscoveryV1

parser = argparse.ArgumentParser()
parser.add_argument('disc_config', help='The Discovery configuration file.')
parser.add_argument('coll_config',
                    help='Information about the collection and environment.')
parser.add_argument('pages_dir',
                    help='The directory where the wikivoyage pages are.')
args = parser.parse_args()

with open(args.disc_config, 'r') as f:
    discovery_config = json.load(f)

with open(args.coll_config, 'r') as f:
    collection_config = json.load(f)

discovery = DiscoveryV1(username=discovery_config['username'],
                        password=discovery_config['password'],
                        version='2017-11-07')

env_id = collection_config['environment_id']
coll_id = collection_config['collection_id']

for filename in os.listdir(args.pages_dir):
    full_path = os.path.join(args.pages_dir, filename)

    with open(full_path, 'r') as f:
        discovery.add_document(env_id, coll_id, file_info=f)
