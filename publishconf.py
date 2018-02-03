#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from pelicanconf import *

SITEURL = 'http://genealogy.minchin.ca'
RELATIVE_URLS = False
SITE_ROOT_URL = 'http://minchin.ca'

#FEED_ALL_ATOM = 'feeds/all.atom.xml'
#CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

# DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""

# PLUGINS = ['assets', 'minify', 'sitemap', 'optimize_images']

PLUGINS = PLUGINS + [
    'minchin.pelican.plugins.cname',
    'minchin.pelican.plugins.nojekyll',
]
