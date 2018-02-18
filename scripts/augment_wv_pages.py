#!/usr/bin/env python

#
# TODO
#

import argparse
import json
import os

import lib.places

def create_page(title, text):
    return {
        'title': title,
        'text': text
    }

def augment_page(pc, page):
    mod_title = re.sub(r'\s*\(.+?\)\s*', '', page['title'])
    page['country'] = pc.country(page['title'])

parser = argparse.ArgumentParser()
parser.add_argument('pages_dir', help='The location of pages to augment.')
parser.add_argument('places_config', help='Configuration for the places client.')
args = parser.parse_args()

with open(args.places_config, 'r') as config:
    places_key = json.load(config)['key']
pc = lib.places.GooglePlacesClient(places_key)

for filename in os.lisdir(args.pages_dir):
    with open(filename, 'r') as f:
        # TODO: util?
        # Remove the .json suffix to find out where this page is talking about.
        title = filename[:-5]
        content = f.read()

        page = create_page(title, content)
        augment_page(pc, page)

    with open(filename, 'w') as f:
        json.dump(page, f)
