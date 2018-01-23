#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import os
import sys

import seafoam
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Adam configuration options
ADAM_PUBLISH = False
from config.adamconf import *
# ADAM = True  is used by the theme tempates to display 'Genealogy only' things

AUTHOR = 'D. Minchin & Wm. Minchin'
SITENAME = 'Minchin.ca'
SITEURL = ''
RELATIVE_URLS = True
# SITE_ROOT_URL = 'http://minchin.ca'
SITE_ROOT_URL = ''

TIMEZONE = 'America/Edmonton'

DEFAULT_LANG = 'en'


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# static paths will be copied under the same name
# these are relative to the base CONTENT folder
STATIC_PATHS = ['images',
                '../extras',
                'css',
                'design',
                'js',
                'pages/img',
                '../.gitattributes',
                '../.gitignore',
                '../README.txt',
                'assets',
                ]

# A list of files to copy from the source to the destination
EXTRA_PATH_METADATA = {
    '../.gitattributes':            {'path': '.gitattributes'},
    '../.gitignore':                {'path': '.gitignore'},
    '../README.txt':                {'path': 'README.txt'},
    '../extras/minchin.ico':        {'path': 'favicon.ico'},
    '../extras/.nojekyll':          {'path': '.nojekyll'},
    'js/tab-list-handler.js':       {'path': 'tab-list-handler.js'},
    'js/tooltip-handler.js':        {'path': 'tooltip-handler.js'},
    'js/graph-handler.js':          {'path': 'graph-handler.js'},
    'js/gigatrees-map-min.js':      {'path': 'gigatrees-map-min.js'},
    'pages/img/arrowd.png':         {'path': 'arrowd.png'},
    'pages/img/arrowl.png':         {'path': 'arrowl.png'},
    'pages/img/arrowr.png':         {'path': 'arrowr.png'},
    'pages/img/arrowu.png':         {'path': 'arrowu.png'},
    'pages/img/bg-black.png':       {'path': 'bg-black.png'},
    'pages/img/bg-pattern.png':     {'path': 'bg-pattern.png'},
    'pages/img/mapicon_f.png':      {'path': 'mapicon_f.png'},
    'pages/img/mapicon_m.png':      {'path': 'mapicon_m.png'},
    'pages/img/mapicon_u.png':      {'path': 'mapicon_u.png'},
    'pages/img/mapmarker1.png':     {'path': 'mapmarker1.png'},
    'pages/img/mapmarker2.png':     {'path': 'mapmarker2.png'},
    'pages/img/mapmarker3.png':     {'path': 'mapmarker3.png'},
    'pages/img/mapmarker4.png':     {'path': 'mapmarker4.png'},
    'pages/img/mapmarker5.png':     {'path': 'mapmarker5.png'},
    'pages/img/avatar.jpg':         {'path': 'avatar.jpg'},
    'pages/img/image.jpg':          {'path': 'image.jpg'},
    'pages/img/pdf.jpg':            {'path': 'pdf.jpg'},
    }


# Custom settings
#FILENAME_METADATA = ('(?P<date>\d{4}-\d{2}-\d{2}).*')  # default?
#FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'  # extract date and slug
# FILENAME_METADATA = '(?P<slug>[\w-]*)'      # so anything before the file extension becomes the slug
FILENAME_METADATA = '(?P<slug>[\w\-_\\\\/]+)'
## Please note that the metadata available inside your files takes precedence
#  over the metadata extracted from the filename.

MARKUP = (('rst',
           'md',
           'markdown',
           'mkd',
           'mdown',
           'html',
           'htm'))
PATH = 'content'
OUTPUT_PATH = '../genealogy-gh-pages/'

# Add Blog to sidebar
MENUITEMS = (('Blog',        'http://blog.minchin.ca/',      'fa fa-fw fa-pencil'),
             ('Genealogy',   SITEURL,                        'glyphicon glyphicon-tree-deciduous'),
             ('My Projects', 'http://minchin.ca/projects/',  'fa fa-fw fa-flask'),
             ('Search',      'http://minchin.ca/search/',    'fa fa-fw fa-search'),
             ('About',       'http://minchin.ca/about/',     'fa fa-fw fa-info-circle'),
             ('Contact Me',  'http://minchin.ca/contact/',   'fa fa-fw fa-envelope'),
             )

MENUITEMS_2_AT = 'Genealogy'
MENUITEMS_2_AT_LINK = ''  # this is added to SITEURL

MENUITEMS_2 = (('Surnames',         SITEURL + '/names/index.html',          False),
               #('Updates',          SITEURL + '/updates.html',        False),
               ('Sources',          SITEURL + '/sources/index.html',        False),
               ('Distribution Map', SITEURL + '/map/index.html',            False),
               ('Timelines',        SITEURL + '/timelines/index.html',      False),
               #('Immigrants',       SITEURL + '/immigrants.html',     False),
               #('Nobility',         SITEURL + '/nobility.html',       False),
               #('Military',         SITEURL + '/soldiers.html',       False),
               ('Locations',        SITEURL + '/places/index.html',         False),
               #('Bonkers Report',   SITEURL + '/bonkers.html',        False),
               # doens't exist in current builds
               ('Photos',           SITEURL + '/photos/index.html',         False),
               # doens't exist in current builds
               #('External Links',   SITEURL + '/links.html',          False),
               # stats graphs aren't working right now; something with the JS link??
               ('Statistics',       SITEURL + '/stats/index.html',          False),
               )


DISPLAY_PAGES_ON_MENU = False

# disable Tags, etc
TAGS_SAVE_AS = ''
TAG_SAVE_AS = ''
CATEGORY_URL = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_URL = ''
CATEGORIES_SAVE_AS = ''
ARTICLE_URL = ''
ARTICLE_SAVE_AS = ''
AUTHORS_URL = ''
AUTHORS_SAVE_AS = ''
ARCHIVES_URL = ''
ARCHIVES_SAVE_AS = ''
PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

# Theme Related
THEME = seafoam.get_path()
BOOTSTRAP_THEME = 'seafoam'

SITELOGO = 'images/MinchindotCA-200.png'
SITELOGO_SIZE = '100%'
DISPLAY_BREADCRUMBS = True
FAVICON = 'favicon.ico'
USE_OPEN_GRAPH = True

TYPOGRIFY = False  # turn off for HIDDEN names...
# PYGMENTS_STYLE = 'friendly'
CUSTOM_CSS = 'css/minchin-ca.css'
DOCUTIL_CSS = False
CUSTOM_JS_LIST = ['js/jquery-ui.min.js',
                  'js/globalize.min.js',
                  'js/dx.chartjs.js',
                  ]

# Generate 404 error page
TEMPLATE_PAGES = {
    '404.html':     '404.html',
}

GOOGLE_ANALYTICS_UNIVERSAL = 'UA-384291-3'
GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = 'minchin.ca'

# Plugins
PLUGIN_PATHS = ('../pelican-plugins',)
# PLUGINS = ['assets', 'minify', 'sitemap', 'optimize_images']
PLUGINS = ['minchin.pelican.jinja_filters',
           'minchin.pelican.plugins.image_process',
           # others, as desired...
           ]

ASSET_CSS = False
ASSET_JS = False

SITEMAP = {
    "format": "xml",
}

IMAGE_PROCESS = {
  'article-feature': ["scale_in 848 848 True"],
  'index-feature': ["scale_in 263 263 True"],
}

# `assets` sounds good, but I can't figure out how to get it to work for my CSS
# `better_figures_and_images` didn't seem to do what I wanted (see Projects)
# `gallery` looks good, but don't have a use here yet
# `liquid_tags` & `pelican_comment_system` might be useful...
# `optimize_images` works, but I don't have many images yet
#       - requires `jpegtran.exe` <http://jpegclub.org/jpegtran/> and
#           `optinpng.exe` <http://sourceforge.net/projects/optipng/>
# look into 'neighbors' plugin for profiles


# # Make things disappear
DISPLAY_CATEGORIES_ON_MENU = False
HIDE_SITENAME = True
HIDE_SIDEBAR = True
FEED_ALL_ATOM = False
FEED_ALL_RSS = False
GITHUB_USER = False
ADDTHIS_PROFILE = False
DISQUS_SITENAME = False
PDF_PROCESSOR = False
