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

import lib.geo.country
import lib.geo.region


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


def augment_page(rc, cities_to_country, country_to_iata, page):
    country = cities_to_country[page.title]

    try:
        code = country_to_iata[country]
        page.set_extra('iata', code)
    except KeyError:
        page.set_extra('iata', '')

    page.set_extra('country', country.value.title())

    try:
        r = rpi_by_country[country]
        page.set_extra('rpi', r)
    except KeyError:
        page.set_extra('rpi', -1)

    try:
        region = rc.region(country)
        page.set_extra('region', region.name.title())
    except requests.exceptions.HTTPError:
        page.set_extra('region', '')


def augment_and_write(rc, cities_to_country, country_to_iata, output_dir, page):
    page.remove_wikicode()
    augment_page(rc, cities_to_country, country_to_iata, page)

    out_fn = os.path.join(output_dir, page.title + '.json')
    with open(out_fn, 'w') as f:
        json.dump(page.json(), f)

    print(page.title)


parser = argparse.ArgumentParser()
parser.add_argument('dump', help='The file name of the WikiVoyage dump.')
parser.add_argument('output_dir', help='The output directory of the pages')
parser.add_argument('cities_by_pop',
                    help='A csv file of cities sorted by population')
parser.add_argument('rpi_by_country', help='A csv of countries and their rpi')
parser.add_argument('iata_country_codes', help='A csv of IATA countries codes')
parser.add_argument('num_cities', help='The number of cities to consider',
                    type=int)
parser.add_argument('--threads', type=int, default=5,
                    help='The number of threads to use.')
args = parser.parse_args()


# Go through the list of cities in order of population and create a list.
cities = []
cities_to_country = {}
with open(args.cities_by_pop, 'r') as f:
    cities_reader = csv.reader(f, delimiter=',')

    for i, row in enumerate(cities_reader):
        country = row[0]
        city = row[1]
        cities.append(city)
        if city not in cities_to_country:
            cities_to_country[city] = lib.geo.country.create(country.lower())

rpi_by_country = {}
with open(args.rpi_by_country, 'r') as f:
    rpi_reader = csv.reader(f, delimiter=',')

    for row in rpi_reader:
        if row:
            raw_country = row[0]
            c = lib.geo.country.create(raw_country)
            rpi_by_country[c] = float(row[1])

country_to_iata = {}
with open(args.iata_country_codes, 'r') as f:
    iata_reader = csv.reader(f, delimiter=',')

    for row in iata_reader:
        if row:
            raw_country = row[0].lower()

            try:
                c = lib.geo.country.create(raw_country)
                code = row[1]

                country_to_iata[c] = code
            except ValueError:
                pass


factory = lib.page.WVPageXMLFactory(NAMESPACE)
dump = ElementTree.parse(args.dump)
root = dump.getroot()

aggs = collections.defaultdict(list)
for page_node in root.iterfind(NAMESPACE + 'page'):
    page = factory.create(page_node)

    if save_page(page):
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
rc = lib.places.RestCountriesClient()

with multiprocessing.Pool(args.threads) as p:
    wrapped = functools.partial(augment_and_write, rc, cities_to_country,
        country_to_iata, args.output_dir)
    p.map(wrapped, pages_to_augment)
