#!/usr/bin/env python

#
# Upload *.json pages in the provided folder to discovery with the provided
# credentials.
#

import argparse
import functools
import json
import multiprocessing
import os

from watson_developer_cloud import DiscoveryV1, WatsonException
from retry import retry

import logging

def upload_article(discovery, env_id, coll_id, f):
    discovery.add_document(env_id, coll_id, file_info=f)

@retry(exceptions=WatsonException, delay=1, backoff=1.2, max_delay=10)
def upload_filename(discovery, env_id, coll_id, fn):
    print(fn)
    with open(fn) as f:
        upload_article(discovery, env_id, coll_id, f)

def upload_filename_configured(discovery, env_id, coll_id):
    return functools.partial(upload_filename, discovery, env_id, coll_id)

parser = argparse.ArgumentParser()
parser.add_argument('disc_config', help='The Discovery configuration file.')
parser.add_argument('coll_config',
                    help='Information about the collection and environment.')
parser.add_argument('pages_dir',
                    help='The directory where the wikivoyage pages are.')
parser.add_argument('--threads', type=int, default=1,
                    help='The number of threads to use in deleting docs.')
args = parser.parse_args()

logging.basicConfig()

with open(args.disc_config, 'r') as f:
    discovery_config = json.load(f)

with open(args.coll_config, 'r') as f:
    collection_config = json.load(f)

discovery = DiscoveryV1(username=discovery_config['username'],
                        password=discovery_config['password'],
                        version='2017-11-07')

env_id = collection_config['environment_id']
coll_id = collection_config['collection_id']
configured = upload_filename_configured(discovery, env_id, coll_id)

filenames = []
for filename in os.listdir(args.pages_dir):
    full_path = os.path.join(args.pages_dir, filename)
    filenames.append(full_path)

with multiprocessing.Pool(args.threads) as p:
    p.map(configured, filenames)
