#!/usr/bin/env python

#
# This script takes in UN data for all cities and performs a transformation on
# it. Note that each row is assumed to represent both sexes with no split. This
# transformation consists of a few steps. First, the result only contains the
# city population, the country name and the city name. The city population for
# each city is the maximum across all years seen.
#

import argparse
import collections
import csv
import sys

def subset_census_row(row_items):
    """
    Select a subset of the items in a row and return this subset as a list.
    Keep the same relative ordering in the subset. In this case, this function
    returns the country name, city name, and population in that order.

    Args:
    row_items: The items in the census row.

    Returns:
    A new row consisting of [country_name, city_name, population]
    """
    return (row_items[0], row_items[4], row_items[9])

parser = argparse.ArgumentParser()
parser.add_argument('un_data_fn', help='The raw UN census data filename.')
args = parser.parse_args()

max_populations = collections.defaultdict(int)

with open(args.un_data_fn, 'r') as un_data:
    un_data_reader = csv.reader(un_data, delimiter=',')
    transformed_writer = csv.writer(sys.stdout)

    # Discard the column headers.
    next(un_data_reader)

    for row in un_data_reader:
        transformed = subset_census_row(row)
        k = transformed[:2]
        # This removes the half people that exist in the world.
        pop = int(float(transformed[2]))

        if max_populations[k] < pop:
            max_populations[k] = pop

sorted_max_pop = sorted(max_populations.items(), key=lambda el: el[1],
                        reverse=True)
for k, pop in sorted_max_pop:
    transformed_writer.writerow((k[0], k[1], pop))
