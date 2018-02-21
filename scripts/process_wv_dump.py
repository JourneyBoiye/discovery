#!/usr/bin/env python

#
# The processing pipeline for a WikiVoyage db dump. This takes in the db dump as
# an xml file, then processes all docs, selects the top n based on population
# and adds more info to each doc such as country and region. Pages that are
# disambiguation, mediawiki, or meta pages are excluded.
#

import argparse
import collections
import csv
import functools
import json
import multiprocessing
import os
import re
import xml.etree.cElementTree as ElementTree

import requests

import lib.normalize
import lib.page
import lib.places

NAMESPACE = '{http://www.mediawiki.org/xml/export-0.10/}'


def save_page(page):
    """
    Determine whether or not to save the given page. Do not save the page if it
    is a disambiguation page, a redirect page, a mediawiki page, a meta page,
    etc.

    Args
    page: The page to check whether or not we should save.

    Returns
    True if the page should be saved, and false otherwise.
    """
    text = page.text.lower()
    title = page.title.lower()

    return '#redirect' not in text and \
           'mediawiki:' not in title and \
           'wikivoyage:' not in title and \
           'file:' not in title and \
           'template:' not in title and \
           'disambiguation' not in title and \
           'module:' not in title and \
           'category:' not in title and \
           'disambiguation banner' not in text[:200]


def augment_page(pc, rc, page):
    mod_city = re.sub(r'\s*\(.+?\)\s*', '', page.title)
    city = lib.normalize.city(mod_city)
    unnorm_country = pc.country(city)

    country = lib.normalize.country(unnorm_country)
    page.set_extra('country', country)

    if country:
        try:
            # TODO: How to handle this elegantly.
            if country == 'South Korea':
                country = 'Korea (Republic of)'

            region = rc.region(country)
            page.set_extra('region', region)
        except requests.exceptions.HTTPError:
            page.set_extra('region', '')
    else:
        page.set_extra('region', '')


def augment_and_write(pc, rc, output_dir, page):
    augment_page(pc, rc, page)

    out_fn = os.path.join(output_dir, page.title + '.json')
    with open(out_fn, 'w') as f:
        json.dump(page.json(), f)

    print(page.title)


parser = argparse.ArgumentParser()
parser.add_argument('dump', help='The file name of the WikiVoyage dump.')
parser.add_argument('output_dir', help='The output directory of the pages')
parser.add_argument('cities_by_pop',
                    help='A csv file of cities sorted by population')
parser.add_argument('num_cities', help='The number of cities to consider',
                    type=int)
parser.add_argument('places_config', help='Configuration for the places client.')
parser.add_argument('--threads', type=int, default=5,
                    help='The number of threads to use.')
args = parser.parse_args()

with open(args.places_config, 'r') as config:
    places_key = json.load(config)['key']

# Go through the list of cities in order of population and create a list.
cities = []
with open(args.cities_by_pop, 'r') as f:
    cities_reader = csv.reader(f, delimiter=',')

    for i, row in enumerate(cities_reader):
        cities.append(row[1])

factory = lib.page.WVPageXMLFactory(NAMESPACE)
dump = ElementTree.parse(args.dump)
root = dump.getroot()

aggs = collections.defaultdict(list)
for page_node in root.iterfind(NAMESPACE + 'page'):
    page = factory.create(page_node)

    if save_page(page):
        page.remove_wikicode()

        splice = page.title.find('/')
        if splice < 0:
            title = page.title
        else:
            title = page.title[:splice]

        aggs[title].append(page.text)

selected = 0
selected_aggs = {}
for city in cities:
    if city in aggs:
        selected += 1
        selected_aggs[city] = '\n'.join(aggs[city])

        if selected >= args.num_cities:
            break

pages_to_augment = [lib.page.WVPage(k, v) for k, v in selected_aggs.items()]
pc = lib.places.GooglePlacesClient(places_key)
rc = lib.places.RestCountriesClient()

with multiprocessing.Pool(args.threads) as p:
    wrapped = functools.partial(augment_and_write, pc, rc, args.output_dir)
    p.map(wrapped, pages_to_augment)
