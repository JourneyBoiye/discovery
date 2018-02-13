#!/usr/bin/env python

#
# Given a directory of WikiVoyage pages and other files decide which ones to
# select. Currently, this other file consists of a sorted list of cities by
# population. This will allow us to put in WikiVoyage articles that are of
# prominent places, approximately.
#

import argparse
import csv
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('wv_pages_dir',
                    help='The folder that contains WikiVoyage pages')
parser.add_argument('cities_by_pop',
                    help='A csv file of cities sorted by population')
parser.add_argument('output_dir', help='Where the selected pages are stored.')
parser.add_argument('num_cities', help='The number of cities to consider',
                    type=int)
args = parser.parse_args()

# This list will hold city names in order of population.
cities = []
with open(args.cities_by_pop, 'r') as f:
    cities_reader = csv.reader(f, delimiter=',')

    for i, row in enumerate(cities_reader):
        cities.append(row[1])

page_names = set()
# Go through all directories in the provided wikivoyage directory. All of these
# files should be pages with a .json suffix.
for filename in os.listdir(args.wv_pages_dir):
    # Remove the .json suffix to find out where this page is talking about.
    article_title = filename[:-5]
    page_names.add(article_title)


selected = 0
for city in cities:
    if city in page_names:
        selected += 1
        print(city)

        filename = city + '.json'
        source_article_path = os.path.join(args.wv_pages_dir, filename)
        dest_article_path = os.path.join(args.output_dir, filename)
        shutil.copyfile(source_article_path, dest_article_path)

    if selected >= args.num_cities:
        break
