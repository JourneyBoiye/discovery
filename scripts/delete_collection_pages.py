#!/usr/bin/env python

#
# Clear discovery of all WikiVoyage related info to reset and upload data again.
#

import argparse
import functools
import json
import multiprocessing

from watson_developer_cloud import DiscoveryV1

def delete_doc(discovery, env_id, coll_id, doc_id):
    print('Deleting {}'.format(doc_id))
    discovery.delete_document(env_id, coll_id, doc_id)

def delete_doc_wrapper(discovery, env_id, coll_id):
    return functools.partial(delete_doc, discovery, env_id, coll_id)

parser = argparse.ArgumentParser()
parser.add_argument('disc_config_file',
                    help='Discovery information such as username and password.')
parser.add_argument('wv_config_file', help='The WikiVoyage discovery config info.')
parser.add_argument('--threads', type=int, default=10,
                    help='The number of threads to use in deleting docs.')
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
wrapped = delete_doc_wrapper(discovery, env_id, coll_id)

qopts = {
    'query': '*.*',
    'count': 500
}

size = 1

while size > 0:
    resp = discovery.query(env_id, coll_id, qopts)
    ids = map(lambda r: r['id'], resp['results'])
    size = len(resp['results'])

    with multiprocessing.Pool(args.threads) as p:
        p.map(wrapped, ids)
