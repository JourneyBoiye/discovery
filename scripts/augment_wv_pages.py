#!/usr/bin/env python

#
# TODO
#

import argparse
import json
import multiprocessing
import re
import os

import requests

import lib.places
import lib.normalize

def create_page_from_json_file(f):
    j = json.load(f)
    return create_page(j['title'], j['text'])

def create_page(title, text):
    # TODO: Rename to 'city'
    return {
        'title': title,
        'text': text
    }

def augment_page(pc, rc, page):
    mod_city = re.sub(r'\s*\(.+?\)\s*', '', page['title'])
    city = lib.normalize.city(mod_city)
    unnorm_country = pc.country(city)
    page['country'] = lib.normalize.country(unnorm_country)

    if page['country']:
        try:
            page['region'] = rc.region(page['country'])
        except requests.exceptions.HTTPError:
            page['region'] = ''
    else:
        page['region'] = ''

def augment_and_write_page(paths):
    in_path = paths[0]
    out_path = paths[1]
    print(in_path)

    with open(in_path, 'r') as f:
        page = create_page_from_json_file(f)
        augment_page(pc, rc, page)

    with open(out_path, 'w') as f:
        json.dump(page, f)


parser = argparse.ArgumentParser()
parser.add_argument('pages_dir', help='The location of pages to augment.')
parser.add_argument('output_dir', help='Where to output the augmented pages.')
parser.add_argument('places_config', help='Configuration for the places client.')
parser.add_argument('--threads', type=int, default=2,
                    help='Number of pool processes to run for this.')
args = parser.parse_args()

with open(args.places_config, 'r') as config:
    places_key = json.load(config)['key']

pc = lib.places.GooglePlacesClient(places_key)
rc = lib.places.RestCountriesClient()

filenames = []
for filename in os.listdir(args.pages_dir):
    in_path = os.path.join(args.pages_dir, filename)
    out_path = os.path.join(args.output_dir, filename)
    filenames.append((in_path, out_path))

with multiprocessing.Pool(args.threads) as p:
    p.map(augment_and_write_page, filenames)
