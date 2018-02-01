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

parser = argparse.ArgumentParser()
parser.add_argument('wv_pages_dir',
                    help='The folder that contains WikiVoyage pages')
parser.add_argument('cities_by_pop',
                    help='A csv file of cities sorted by population')
args = parser.parse_args()

# This list will hold city, country name pairs in order of population.
cities_by_pop = []
with open(args.cities_by_pop, 'r') as f:
    cities_reader = csv.reader(f, delimiter=',')

# Go through all directories in the provided wikivoyage directory. All of these
# files should be pages with a .json suffix.
for filename in os.listdir(args.wv_pages_dir):
    # Remove the .json suffix to find out where this page is talking about.
    article_title = filename[:-5]
