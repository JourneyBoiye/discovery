#!/usr/bin/env sh

#
# Complete go through of the data pipeline from wikivoyage db dump to discovery
# articles. This requires the following command line args and is called as
# follows:
#   ./upload_wv_dump.sh disc_config.json coll_config.json wv_dump.xml un-pop.csv num-cities
#


mkdir __wvpages
echo Partition wikivoyage dump
scripts/./partition_wv_dump.py $3 __wvpages

echo Preprocess UN census data
scripts/./transform_un_census_data.py $4 > __pop.csv

mkdir __selected
echo Select pages from wikivoyage dump
scripts/.select_wv_pages.py __wvpages __pop.csv __selected $5

echo Uploading pages that were selected.
scripts/./upload_pages.py $1 $2 __selected

rm __pop.csv
rm -rf __wvpages
rm -rf __selected
