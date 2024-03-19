#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import os
import sys

# import seafoam
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Adam configuration options
ADAM_PUBLISH = False
from config.adamconf import *
# ADAM = True  is used by the theme tempates to display 'Genealogy only' things

AUTHOR = 'D. Minchin & Wm. Minchin'
SITENAME = 'Minchin Genealogy'
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
STATIC_PATHS = [
    'images',
    '../extras',
    'css',
    'design',
    'js',
    'pages/assets',
    '../.gitattributes',
    '../.gitignore',
    '../README.txt',
]

# A list of files to copy from the source to the destination
EXTRA_PATH_METADATA = {
    '../.gitattributes':                            {'path': '.gitattributes'},
    '../.gitignore':                                {'path': '.gitignore'},
    '../README.txt':                                {'path': 'README.txt'},
    '../extras/minchin.ico':                        {'path': 'favicon.ico'},
    '../extras/netlify.toml':                       {'path': 'netlify.toml'},
    'pages/assets/bootstrap-tooltip-handler.js':    {'path': 'assets/bootstrap-tooltip-handler.js'},
    'pages/assets/fancybox-handler.js':             {'path': 'assets/fancybox-handler.js'},
    'pages/assets/gigatrees-charts.js':             {'path': 'assets/gigatrees-charts.js'},
    'pages/assets/gigatrees-heatmaps.min.js':       {'path': 'assets/gigatrees-heatmaps.min.js'},
    'pages/assets/gmaps-heatmap.min.js':            {'path': 'assets/gmaps-heatmap.min.js'},
    'pages/assets/heatmap.min.js':                  {'path': 'assets/heatmap.min.js'},
    'pages/assets/markerclusterer.min.js':          {'path': 'assets/markerclusterer.min.js'},
    'pages/assets/ac_arrow_down.png':               {'path': 'assets/ac_arrow_down.png'},
    'pages/assets/ac_arrow_up.png':                 {'path': 'assets/ac_arrow_up.png'},
    'pages/assets/avatar.png':                      {'path': 'assets/avatar.png'},
    'pages/assets/image.png':                       {'path': 'assets/image.png'},
    'pages/assets/link.png':                        {'path': 'assets/link.png'},
    'pages/assets/mapicon_f.png':                   {'path': 'assets/mapicon_f.png'},
    'pages/assets/mapicon_m.png':                   {'path': 'assets/mapicon_m.png'},
    'pages/assets/mapicon_u.png':                   {'path': 'assets/mapicon_u.png'},
    'pages/assets/mapmarker1.png':                  {'path': 'assets/mapmarker1.png'},
    'pages/assets/mapmarker2.png':                  {'path': 'assets/mapmarker2.png'},
    'pages/assets/mapmarker3.png':                  {'path': 'assets/mapmarker3.png'},
    'pages/assets/mapmarker4.png':                  {'path': 'assets/mapmarker4.png'},
    'pages/assets/mapmarker5.png':                  {'path': 'assets/mapmarker5.png'},
    'pages/assets/avatar.jpg':                      {'path': 'assets/avatar.jpg'},
    'pages/assets/pdf.png':                         {'path': 'assets/pdf.png'},
}


# Custom settings
#FILENAME_METADATA = ('(?P<date>\d{4}-\d{2}-\d{2}).*')  # default?
#FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'  # extract date and slug
# FILENAME_METADATA = '(?P<slug>[\w-]*)'      # so anything before the file extension becomes the slug
FILENAME_METADATA = r'(?P<slug>[\w\-_\\\\/]+)'
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
OUTPUT_PATH = '../genealogy-local/'

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

MENUITEMS_2 = (('Surnames',         SITEURL + '/names/',          'fa fa-fw fa-user-circle'),
               #('Updates',          SITEURL + '/updates.html',        False),
               ('Sources',          SITEURL + '/sources/',        'fa fa-fw fa-book'),
               ('Distribution Map', SITEURL + '/map/',            'fa fa-fw fa-globe'),
               ('Timelines',        SITEURL + '/timelines/',      'fa fa-fw fa-clock-o'),  # consider hourglass (FA5)
               # doesn't exist in current builds
               #('Immigrants',       SITEURL + '/immigrants.html',     False),
               #('Nobility',         SITEURL + '/nobility.html',       False),
               #('Military',         SITEURL + '/soldiers.html',       False),
               ('Locations',        SITEURL + '/places/',         'fa fa-fw fa-map-marker'),
               ('Photos',           SITEURL + '/photos/',         'fa fa-fw fa-picture-o'),
               # doesn't exist in current builds
               #('External Links',   SITEURL + '/links.html',          False),
               ('Statistics',       SITEURL + '/stats/',          'fa fa-fw fa-bar-chart'),
               ('Data Issues',      SITEURL + '/alerts/',        'fa fa-fw fa-exclamation-triangle'),
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
# THEME = seafoam.get_path()
BOOTSTRAP_THEME = 'seafoam'

SITELOGO = 'images/MinchindotCA-200.png'
SITELOGO_SIZE = '100%'
DISPLAY_BREADCRUMBS = True
FAVICON = 'favicon.ico'
USE_OPEN_GRAPH = True

TYPOGRIFY = False  # turn off for HIDDEN names...
# PYGMENTS_STYLE = 'friendly'
DOCUTIL_CSS = False
JQUERY_JS_IN_HEAD = True
CUSTOM_JS_LIST_HEAD = [
    """<script type="text/javascript">
            var myImage='{0}/assets/mapicon_u.png';
            var myImageW='{0}/assets/mapicon_f.png';
            var myImageM='{0}/assets/mapicon_m.png';
            var mcOptions={{styles:[
                {{ height:35,width:35,url:"{0}/assets/mapmarker1.png"}},
                {{ height:35,width:35,url:"{0}/assets/mapmarker2.png"}},
                {{ height:35,width:35,url:"{0}/assets/mapmarker3.png"}},
                {{ height:35,width:35,url:"{0}/assets/mapmarker4.png"}},
                {{ height:35,width:35,url:"{0}/assets/mapmarker5.png"}}
            ]}};
            function dynamicallyLoadScript(url) {{
                var script = document.createElement('script');
                script.src = url;
                document.head.appendChild(script);
            }}
            if ('file:' == document.location.protocol) {{
                dynamicallyLoadScript('https://maps.googleapis.com/maps/api/js');
            }} else {{
                dynamicallyLoadScript('https://maps.googleapis.com/maps/api/js?key=AIzaSyBtE7dlokTduwUIfWaYdWCdXP_ve2hPKtQ');
            }}
            var loadMap = function(callback) {{
                var interval = setInterval(function() {{
                    if (typeof google !== 'undefined') {{
                        clearInterval(interval);
                        callback();
                    }}
                }}, 1);
            }};
            loadMap(function() {{
                dynamicallyLoadScript('{0}/assets/heatmap.min.js');
                dynamicallyLoadScript('{0}/assets/gmaps-heatmap.min.js');
                dynamicallyLoadScript('{0}/assets/markerclusterer.min.js');
                dynamicallyLoadScript('{0}/assets/gigatrees-heatmaps.min.js');
            }});
        </script>
        """.format(SITEURL),  # use double brackets {{ }} to escape them, to let us use string formatting    
]
CUSTOM_JS_LIST = [           
    'assets/bootstrap-tooltip-handler.js',

    'js/d3.min.js?v=3.5.17',
    'js/c3.min.js?v=0.4.18',
    'js/gigatrees-charts.wm.js',

    'assets/fancybox-handler.js',
    'js/jquery.mousewheel.min.js?v=3.1.13',  # used with FancyBox
    'js/jquery.fancybox.pack.js?v=2.1.7',
    'js/jquery.fancybox-buttons.js?v=1.0.5',
    'js/jquery.fancybox-media.js?v=1.0.6',
    'js/jquery.fancybox-thumbs.js?v=1.0.7',
]
CUSTOM_CSS_LIST = [
    'css/minchin-ca.css',
    'css/jquery.fancybox.min.css?v=2.1.7',
    # '//cdnjs.cloudflare.com/ajax/libs/fancybox/2.1.5/helpers/jquery.fancybox-buttons.css',  # included in Seafoam CSS
    # '//cdnjs.cloudflare.com/ajax/libs/fancybox/2.1.5/helpers/jquery.fancybox-thumbs.css',  # unused??
]

# Generate 404 error page
TEMPLATE_PAGES = {
    '404.html':     '404.html',
}

GOOGLE_ANALYTICS_UNIVERSAL = 'UA-384291-3'
GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = 'minchin.ca'

# Plugins
# PLUGIN_PATHS = ('../pelican-plugins',)
# PLUGINS = ['assets', 'minify', 'sitemap', 'optimize_images']
# PLUGINS = [
#     'minchin.pelican.jinja_filters',
#     # 'minchin.pelican.plugins.image_process',  # breaks
#     # others, as desired...
#     'minchin.pelican.plugins.autoloader',
# ]

ASSET_CSS = False
ASSET_JS = False

SITEMAP = {
    "format": "xml",
}

IMAGE_PROCESS = {
  'article-feature': ["scale_in 848 848 True"],
  'index-feature': ["scale_in 263 263 True"],
  'gt-photo': ["scale_in 100 100 False"],
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
