#!/usr/bin/env python

#
# This scripts is meant to transform raw data from the UN about RPI (Retail
# Price Index) into something that is workable within this app. There is a lot
# of data provided. This script will keep data about the average price of living
# excluding housing preferably and the country. The median of all data points
# will be kept. There is also some other data cleaning in here such as
# transforming NBSP to regular space.
#

import argparse
import re

import pandas

RPI_EXCL_HOUSING_CODE = 's203'

def extract_series_median_df(df, series_code):
    return df.loc[df['seriescode'] == series_code].groupby('country')['data'].median()

parser = argparse.ArgumentParser()
parser.add_argument('un_data', help='The location of the RPI data')
args = parser.parse_args()

df = pandas.read_csv(args.un_data)
median_df = extract_series_median_df(df, RPI_EXCL_HOUSING_CODE)

csv_text = median_df.to_csv(header=None).lower()
tmp = csv_text.replace('\xa0', ' ')
tmp = re.sub('[ \t]+', ' ', tmp)
print(tmp)
