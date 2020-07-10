#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Xiaoyong Guo'
SITENAME = u"Xiaoyong's Blog"
SITEURL = ''
THEME = 'themes/blueidea2'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'en'
#MD_EXTENSIONS
#MARKDOWN = ['fenced_code', 'codehilite(css_class=highlight, linenums=True)', 'extra']

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["render_math"]
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ("Leon's Blog", 'http://52.193.207.59/blog/'),)

# Social widget
SOCIAL = (('github', 'http://www.github.com/guoxiaoyong'),
          ('twitter', 'http://twitter.com'),)

DEFAULT_PAGINATION = False
LOAD_CONTENT_CACHE = False
DEFAULT_DATE = 'fs'
STATIC_PATHS = {'images', 'mp3'}
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

MENUITEMS = (
   ('Home', '/pages/welcome-to-xiaoyong-guos-homepage.html'),
   ('Blog', '/index.html'),
   ('Projects', '/pages/projects.html'),
   ('About', '/pages/about_xiaoyong_guo.html'),
)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
