#!/usr/bin/env python

#
# This script takes in an XML db dump from WikiVoyage and breaks up each article
# into a separate file with the name of the article. This article will be a json
# file with the fields title and text. This also selects only real articles, as
# in no disambiguation pages, or mediawiki pages, or meta pages.
#

import argparse
import collections
import json
import os
import re

import xml.etree.cElementTree as ElementTree

NAMESPACE = '{http://www.mediawiki.org/xml/export-0.10/}'
def namespaced_tag(tag):
    return NAMESPACE + tag

def save_page(page):
    text = page['text'].lower()
    title = page['title'].lower()

    return '#redirect' not in text and \
           'mediawiki:' not in title and \
           'wikivoyage:' not in title and \
           'file:' not in title and \
           'template:' not in title and \
           'disambiguation' not in title and \
           'module:' not in title and \
           'category:' not in title and \
           'disambiguation banner' not in text[:200]

def transformed_page_text(text):
    tmp1 = re.sub(r'\{\{(pagebanner|departures)|(.+?)\}\}', '', text)
    tmp2 = re.sub(r'\[\[(File|Image)(.+?)\]\]', '', tmp1)
    tmp3 = re.sub(r'\[\[(.*?)\|?([^\[\]]+)\]\]', '\\2', tmp2)
    tmp4 = re.sub(r'={2,}(.+?)={2,}', '\\1', tmp3)
    tmp5 = re.sub(r'\'{2,}', '', tmp4)
    tmp6 = re.sub(r'\[\S+ (\S+)\]', '\\1', tmp5)

    return tmp6

def create_page_from_page_node(node):
    page = {}
    page['title'] = page_node.find(namespaced_tag('title')).text
    raw_text = page_node.find(namespaced_tag('revision')).find(namespaced_tag('text')).text
    if raw_text is None:
        raw_text = ''
    page['text'] = raw_text

    return page


parser = argparse.ArgumentParser()
parser.add_argument('dump', help='The file name of the WikiVoyage dump.')
parser.add_argument('output_dir', help='The output directory of the pages')
args = parser.parse_args()

dump = ElementTree.parse(args.dump)
root = dump.getroot()

aggs = collections.defaultdict(list)
for page_node in root.iterfind(namespaced_tag('page')):
    page = create_page_from_page_node(page_node)

    if save_page(page):
        splice = page['title'].find('/')
        if splice < 0:
            title = page['title']
        else:
            title = page['title'][:splice]

        aggs[title].append(transformed_page_text(page['text']))

for title, articles in aggs.items():
    page = {
        'title': title,
        'text': '\n'.join(articles)
    }

    print(title)

    fn = title + '.json'
    full_path = os.path.join(args.output_dir, fn)
    with open(full_path, 'w') as f:
        json.dump(page, f)
