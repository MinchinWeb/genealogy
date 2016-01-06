#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Genealogy Uploader
v.3.2.1 - WM - January 6, 2016

This script serves to semi-automate the building and uploading of my
genealogy website. It is intended to be semi-interactive and run from the
command line.'''


import codecs
from datetime import date, datetime
import fileinput
import multiprocessing
import os
from pathlib import Path
import re
import sys
import textwrap
import uuid
import webbrowser
import zipfile

from bs4 import BeautifulSoup
import colorama
from colorama import Fore, Style
from invoke import run, task
import requests
import winshell

import minchin.text

# import envoy
# from colorama import Back


__version__ = '3.2.1'
colorama.init()


COPYRIGHT_START_YEAR = 1987
ADAM_LINK = "http://gigatrees.com"
ADAM_FOOTER = "<p><strong>Are we related?</strong> Are you a long lost cousin? Spotted an error here? This website remains a work-in-progress and I would love to hear from you. Drop me a line at minchinweb [at] gmail [dot] com.</p>"
INDENT = " "*4
GITHUB_FOLDER = Path("S:\Documents\GitHub\genealogy-gh-pages")
PHOTO_FOLER = Path("S:\Documents\Genealogy")
DOWNLOAD_FOLDER = Path("S:\Downloads\Firefox")
URL_ROOT = "http://minchin.ca/genealogy"
REPO_URL = "https://github.com/MinchinWeb/genealogy.git"
ADAM_PREFIX = 'william-minchin-gigatree-offline-'
TODAY_STR = '' + str(date.today().year)[2:] + str.zfill(str(date.today().month), 2) + str.zfill(str(date.today().day), 2)
GEDCOM_EXPECTED = 'William ' + TODAY_STR + '.ged'
USER_FOLDER = Path(os.path.expanduser('~'))
MY_GEDCOM = USER_FOLDER / 'Desktop' / GEDCOM_EXPECTED
start_time = datetime.now()
step_no = 0  # step counter
start_time = datetime.now()
HERE_FOLDER = Path.cwd()
WORKING_FOLDER = HERE_FOLDER  # current working directory
CONTENT_FOLDER = HERE_FOLDER / 'content' / 'pages'
adam_zip = ''               # set later
tracking_filename = ''      # set later

# globals for Lenovo X201
#GITHUB_FOLDER = Path(r"C:\Users\User\Documents\GitHub\genealogy-gh-pages")
#PHOTO_FOLER = Path(r"C:\Users\User\Documents\Genealogy")
#DOWNLOAD_FOLDER = Path(r"C:\Users\User\Downloads")


def addimage(image):
    '''Take the file listed in image, finds in my genealogy photo directory, and
    adds it to the GitHub folder.'''
    '''TO-DO: implement this!!'''
    pass


# multiple replacement
# from  http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
#
# Usage:
# >>> replacements = (u"café", u"tea"), (u"tea", u"café"), (u"like", u"love")
# >>> print multiple_replace(u"Do you like café? No, I prefer tea.", *replacements)
# Do you love tea? No, I prefer café.
def multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M | re.I)
    return lambda string: pattern.sub(replacement_function, string)


def multiple_replace(string, *key_values):
    return multiple_replacer(*key_values)(string)


def get_adam_version():
    soup_file = open(str(CONTENT_FOLDER / 'names.html'), 'r')
    soup = BeautifulSoup(soup_file, "lxml")
    soup_file.close()
    return soup.find(True, "gt-version").get_text().encode('utf-8')  # 'Built by Adam 1.35.0.0' or the like


@task
def export_gedcom():
    '''Export from RootsMagic.'''
    global step_no
    global start_time
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Export from RootsMagic.")

    print("{}call the file {}{}{} and save it to the desktop".format(INDENT*2, Style.BRIGHT, GEDCOM_EXPECTED, Style.RESET_ALL))
    print("{}do not include LDS information".format(INDENT*2))
    print("{}no need to privatize individuals (at this step)".format(INDENT*2))
    if not minchin.text.query_yes_quit("{}Next?".format(INDENT), default="yes"):
        sys.exit()
    try:
        start_time = datetime.fromtimestamp(os.stat(MY_GEDCOM).st_ctime)
    except:
        print("{}Your file doesn't seem to exist. Exiting...".format(INDENT))


@task
def clean_gedcom():
    '''Cleaning up GEDCOM.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Cleaning up GEDCOM.")

    # replace image paths
    gedcom_file = open(str(MY_GEDCOM), 'r', encoding='utf-8')  # add failsafe is the fail doesn't exist yet or is still being written to
    subject = gedcom_file.read()
    gedcom_file.close()

    pattern = re.compile(r'S:\\Documents\\Genealogy\\([0-9]+[\.[a-z]+]*\.? )*', re.IGNORECASE)  # path start
    result = pattern.sub('images/', subject)
    pattern2 = re.compile(r'(images.*)\\')  # reverse slashes in rest of path
    result2 = pattern2.sub(r'\1/', result)
    result3 = pattern2.sub(r'\1/', result2)

    f_out = open(str(MY_GEDCOM), 'w', encoding='utf-8')
    f_out.write(result3)
    f_out.close()


@task
def upload_gedcom():
    '''Upload GEDCOM to Gigatree.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". The file is now ready to upload to Gigatrees.")

    webbrowser.open("http://gigatrees.com/toolbox/gigatree", new=2)
    print("{}log-in (using Facebook)".format(INDENT*2))
    print("{}now click 'generate report'".format(INDENT*2))
    # check to see if we're logged in
    # log in, if needed
    # discard old GEDCOM
    # upload new GEDCOM
    # run generator
    # download new output


@task
def check_images():
    '''Check which images have already been uploaded.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Checking images.")

    gedcom_file = open(str(MY_GEDCOM), 'r', encoding='utf-8')
    subject = gedcom_file.read()
    gedcom_file.close()

    missing_matches = []
    all_matches = []
    matches = 0
    wrapper = textwrap.TextWrapper(width=79, initial_indent=INDENT, subsequent_indent=INDENT*2)
    pattern_bad = re.compile("missing ")
    for match in re.findall(r'(images/.+\.(jpg|jpeg|png|gif|pdf))', subject, re.IGNORECASE):
        all_matches.append(match)

    all_matches = sorted(set(all_matches))  # remove duplicates and sort
    for match in all_matches:
        r = requests.head(URL_ROOT + "/" + str(match[0]), allow_redirects=True)
        if not r.status_code == requests.codes.ok:
            mytext = wrapper.fill("missing {} -> {}".format(str(r.status_code), match[0]))
            print(pattern_bad.sub(Fore.RED + Style.BRIGHT + "missing " + Style.RESET_ALL, mytext))
            missing_matches.append(match[0])
        else:
            matches += 1

    if len(missing_matches) == 0:
        print("{}{} images matching. No missing images.".format(INDENT, str(matches)))
    else:
        print("{}{} images matching.".format(INDENT, str(matches)))
        q_add_images = minchin.text.query_yes_no_all("{}{} missing images. Add them?".format(INDENT, str(len(missing_matches))), default="no")
        if q_add_images == 2:  # all
            for image in missing_matches:
                addimage(image)
        elif q_add_images == 1:  # yes
            for image in missing_matches:
                if minchin.text.querry_yes_no("{}Add {}?".format(INDENT*2, image), default="yes"):
                    addimage(image)
                    # TO-DO: implement this!
                else:
                    pass
        else:  # no
            pass

        # write missing images to a file
        f = open('missing-images.txt', 'w', encoding='utf-8')
        f.write("Genealogy Uploader, v.{}\n".format(str(__version__)))
        f.write('{}\n\n'.format(MY_GEDCOM))
        for missing in missing_matches:
            f.write('{}\n'.format(missing))
        f.close()


@task
def delete_old_output():
    '''Delete old Pelican output.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Deleting old Pelican output.")

    to_delete = []
    html_files = 0
    os.chdir(str(GITHUB_FOLDER))
    all_files = os.listdir(str(GITHUB_FOLDER))

    for filename in all_files:
        if filename == ('.git'):
            pass
        elif filename.endswith('.html'):
            html_files += 1
        else:
            to_delete.append(filename)

    counter = 0

    # delete HTML files
    run('del *.html -y')
    bar = minchin.text.progressbar(maximum=len(to_delete) + html_files)
    counter = html_files
    bar.update(counter)

    # delete everything else
    for my_file in to_delete:
        winshell.delete_file(my_file, no_confirm=True, allow_undo=False, silent=True)
        counter += 1
        bar.update(counter)
    print("\n{}{} files deleted.".format(INDENT*2, str(len(to_delete) + html_files)))


@task
def delete_old_adam():
    '''Delete old Gigatrees output.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Deleting old Gigatree output.")

    os.chdir(str(CONTENT_FOLDER))
    run('del *.* /q')


@task
def get_new_adam():
    '''Get new Gigatree output.'''
    # TO-DO: allow override of 'start time'
    global step_no
    global adam_zip
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Get new Gigatree output.")

    os.chdir(str(DOWNLOAD_FOLDER))
    gedcom_time = datetime.fromtimestamp(os.stat(str(MY_GEDCOM)).st_ctime)

    count_loops = 0
    while True:
        all_files = os.listdir(str(DOWNLOAD_FOLDER))
        for filename in all_files:
            if filename.startswith(ADAM_PREFIX) and filename.endswith(".zip"):
                if datetime.fromtimestamp(os.stat(filename).st_ctime) > gedcom_time:
                    adam_zip = filename
        if adam_zip != '' and os.stat(adam_zip).st_size > 1000:
            break
        count_loops += 1
        if count_loops > 60:
            if minchin.text.query_yes_quit("{}We've waited 30 minutes. Keep waiting?".format(INDENT), default="yes") is False:
                sys.exit()
            else:
                count_loops = 0
        else:
            minchin.text.wait(30)

    winshell.copy_file(adam_zip, str(CONTENT_FOLDER))


def step_unzip():
    # Test 1: 6:48.948 for 9,999 files
    # Test 2: 2:05.188204 for 11,1698 files
    global step_no
    start_time_local = datetime.now()
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Unzip new Gigatree output (Zipfile).")

    os.chdir(str(CONTENT_FOLDER))
    zf = zipfile.ZipFile(adam_zip)
    zf.extractall()
    zf.close()
    print(INDENT, datetime.now() - start_time_local)


def step_unzip_faster():
    # see http://dmarkey.com/wordpress/2011/10/15/python-zipfile-speedup-tips/
    # Test 1: 4:44.459 for 9,999 files
    # this doesn't appear to work on Python 3.5.1, says it's not a zip file
    global step_no
    start_time_local = datetime.now()
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Unzip new Gigatree output (Zipfile faster).")

    os.chdir(str(CONTENT_FOLDER))
    zf = zipfile.ZipFile(open(adam_zip, 'r'))
    zf.extractall()
    zf.close()
    print(INDENT, datetime.now() - start_time_local)


def step_unzip_czip():
    # Test 1: 4:46.109 for 9,999 files
    # Test 2: xx for 11,1698 files
    global step_no
    start_time_local = datetime.now()
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Unzip new Gigatree output (czip).")

    os.chdir(str(CONTENT_FOLDER))
    zf = czipfile.ZipFile(adam_zip)
    zf.extractall()
    zf.close()
    print(INDENT, datetime.now() - start_time_local)


@task
def step_unzip_7zip():
    # Test 1: 5:09.974 for 9,999 files
    # Test 2: 1:43.229726 for 11,1698 files
    global step_no
    start_time_local = datetime.now()
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Unzip new Gigatree output (7-zip).")

    os.chdir(str(CONTENT_FOLDER))
    run('"C:\\Program Files\\7-Zip\\7z.exe" e {} > nul'.format(adam_zip))
    print(INDENT, datetime.now() - start_time_local)


def step_unzip_infozip():
    # Test 2: 1:51.550671 for 11,1698 files
    global step_no
    start_time_local = datetime.now()
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Unzip new Gigatree output (unzip.exe).")

    os.chdir(str(CONTENT_FOLDER))
    run('C:\\bin\\unzip.exe {} > nul'.format(adam_zip))
    print(INDENT, datetime.now() - start_time_local)


@task
def unzip_adam():
    '''Unzip new Adam output.'''
    try:
        step_unzip_7zip()
    except:
        step_unzip()


@task
def php_to_html():
    '''Change any .php files to .html.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Rename all .php files.")
    os.chdir(str(CONTENT_FOLDER))
    run('rename *.php *.html')


@task
def copy_js():
    '''Copy Gigatree .js files.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Copy Gigatree .js files.")
    # files are copied from the base CONTENT_FOLDER (where they are put by unzipping
    # the adam.zip) to the CONTENT_FOLDER / js (where Pelican will find them)

    js_files = ('tab-list-handler.js',
                'tooltip-handler.js',
                'graph-handler.js',
                'gigatrees-map-min.js', )

    for my_file in js_files:
        try:
            winshell.delete_file(str(CONTENT_FOLDER / 'js' / my_file), no_confirm=True, allow_undo=False, silent=True)
        except:
            pass
        winshell.copy_file(str(CONTENT_FOLDER / my_file), str(CONTENT_FOLDER / 'js' / my_file), no_confirm=True)


# not needed; the elements of the 'gigatrees.css' needed have been folded
# directly into the theme LESS files
@task
def copy_css():
    '''Copy Gigatree .css files.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Copy Gigatree .css files.")
    os.chdir(str(CONTENT_FOLDER))

    css_files = ('gigatrees.css', )

    for my_file in css_files:
        try:
            winshell.delete_file("../css/" + my_file, no_confirm=True, allow_undo=False, silent=True)
        except:
            pass
        winshell.copy_file(my_file, "../css/" + my_file, no_confirm=True)


@task
def copy_img():
    '''Copy Gigatree image files.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Copy Gigatree image files.")
    # files are copied from the base CONTENT_FOLDER (where they are put by unzipping
    # the adam.zip) to the CONTENT_FOLDER / img (where Pelican will find them)

    img_files = ('arrowd.png',
                 'arrowl.png',
                 'arrowr.png',
                 'arrowu.png',
                 'bg-black.png',
                 'bg-pattern.png',
                 'mapicon_f.png',
                 'mapicon_m.png',
                 'mapicon_u.png',
                 'mapmarker1.png',
                 'mapmarker2.png',
                 'mapmarker3.png',
                 'mapmarker4.png',
                 'mapmarker5.png',
                 'avatar.jpg',
                 'image.jpg',
                 'pdf.jpg', )

    for my_file in img_files:
        try:
            winshell.delete_file(str(CONTENT_FOLDER / 'img' / my_file), no_confirm=True, allow_undo=False, silent=True)
        except:
            pass
        winshell.copy_file(str(CONTENT_FOLDER / my_file), str(CONTENT_FOLDER / 'img' / my_file), no_confirm=True)



@task
def replace_index():
    '''Copy over index.md, 404.md.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Copy over index.md, 404.md.")

    os.chdir(str(CONTENT_FOLDER))
    for my_file in ("index.md", "index.html", "404.md"):
        try:
            winshell.delete_file(my_file, no_confirm=True, allow_undo=False, silent=True)
        except:
            pass

    for my_file in ("index.md", "404.md"):
        winshell.copy_file("../../_unchanging_pages/{}".format(my_file), my_file, no_confirm=True)


@task
def set_pelican_variables():
    '''Sets a couple of variables that Pelican uses while generating the site.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Setting up Pelican.")

    adam_version_text = get_adam_version()  # 'Built by Adam 1.35.0.0 ' or the like
    adam_version_text = adam_version_text.decode('utf-8').strip()
    date_in_text = date.today().strftime("%B %d, %Y").replace(' 0', ' ')  # 'January 7, 2014' or the like
    year_range = "{}-{}".format(COPYRIGHT_START_YEAR, datetime.now().year)
    print('{}{} - {}'.format(INDENT, adam_version_text, date_in_text))

    f = open(str(WORKING_FOLDER / 'adamconf.py'), 'w')
    f.write('# Genealogy Uploader, v.{}\n'.format(str(__version__)))
    f.write('# {}\n\n'.format(str(MY_GEDCOM)))
    f.write('ADAM = True\n')
    f.write('ADAM_VERSION = "{}"\n'.format(adam_version_text))
    f.write('ADAM_UPDATED = "{}"\n'.format(date_in_text))
    f.write('ADAM_COPY_DATE = "{}"\n'.format(year_range))
    f.write('ADAM_LINK = "{}"\n'.format(ADAM_LINK))
    f.write('ADAM_FOOTER = "{}"\n'.format(ADAM_FOOTER))
    f.write('ADAM_PUBLISH = True\n')
    f.close()


@task
def replace_emails():
    '''Hide emails in Sources.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Hiding Emails.")

    # replace and hide emails; but some of these are over lines breaks,
    #  so we'll have to search and replace through the output
    # We are actually only considering 'Sources', as that's where
    #  all the emails seem to be...
    replacements =  ("w_minchin@hotmail.com",           '[email redacted]'), \
                    ("w.minchin@gmail.com",             '[email redacted]'), \
                    ("webmaster@minchin.ca",            '[email redacted]'), \
                    ("minchinweb@gmail.com",            '[email redacted]'), \
                    ("nysgys@shaw.ca",                  '[email redacted]'), \
                    ("bunburypr@ozemail.com.au",        '[email redacted]'), \
                    ("turtle@turtlebunbury.com",        '[email redacted]'), \
                    ("howard.blaxland@gmail.com",       '[email redacted]'), \
                    ("kenhazel@gmail.com",              '[email redacted]'), \
                    ("canrcr@gmail.com",                '[email redacted]'), \
                    ("david@westerhamworkshop.co.uk",   '[email redacted]'), \
                    ("d3gl@shaw.ca",                    '[email redacted]'), \
                    ("cardena.depper@gmx.net",          '[email redacted]'), \
                    ("redjoanne_58@hotmail.com",        '[email redacted]'), \
                    ("lbwong@charter.net",              '[email redacted]'), \
                    ("djcmgf@optonline.net",            '[email redacted]'), \
                    ("jerry.doyle@sbcglobal.net",       '[email redacted]'), \
                    ("sonofcam@bigpond.com",            '[email redacted]'), \
                    ("stewdee@hotmail.com",             '[email redacted]'), \
                    ("nysgys@shaw.ca",                  '[email redacted]'), \
                    ("gloog@eircom.net",                '[email redacted]'), \
                    ("donaldminchin@yahoo.com",         '[email redacted]'),

    os.chdir(str(CONTENT_FOLDER))
    all_files = os.listdir(str(CONTENT_FOLDER))
    all_html_files = []
    for my_file in all_files:
        #if my_file.endswith(".html"):
        if my_file.startswith('sources-'):
            all_html_files.append(my_file)
    counter = 0
    bar = minchin.text.progressbar(maximum=len(all_html_files))
    # inline search and replace
    for my_file in all_html_files:
        for line in fileinput.input(my_file, inplace=1):
            print(multiple_replace(line, *replacements))
        counter += 1
        bar.update(counter)
    print()  # clear progress bar


def html_fixes(my_file, my_bar, my_counter):
    '''
    Applies the various updates and changes I want done to the raw Gigatrees
    HTML.

    Assumes 'my_file' is in the CONTENT_FOLDER.
    Assumes 'my_file' is a string.
    Assumes 'my_bar' is of type minchin.text.progressbar
    Assumes 'my_counter' is of type multiprocessing.Value
    '''

    with codecs.open(str(CONTENT_FOLDER / my_file), 'r', 'utf-8') as html_doc:
        my_html = html_doc.read()

    soup = BeautifulSoup(my_html, "lxml")

    # change page title
    title_tag = soup.html.head.title
    for tag in soup(id="gt-page-title", limit=1):
        title_tag.string.replace_with(tag.string.strip())
        tag.decompose()

    # dump all the meta tags in the head section
    for tag in soup("meta"):
        tag.decompose()

    '''
    # fix links that point to php pages
    for tag in soup("a", href=True):
        tag['href'] = tag['href'].replace('.php', '.html')
    '''
    '''
    # remove wrapper lists (ul/li) to tables
    for tag in soup("ul"):
       tag2 = tag.findParent('ul')
           if tag2:
               tag2.replace_with(tag2.contents)
               # replace 'li' tags with 'p'
               for tag3 in tag2("li"):
                  tag3.name = 'p'
    '''

    # Remove links to CDN stuff I serve locally
    js_served_locally = ('jquery.min.js',
                         'jquery-ui.min.js',
                         'bootstrap.min.js',
                         'globalize.min.js',
                         'dx.chartjs.js')
    for tag in soup("script"):
        try:
            link = tag["src"]
            if link.endswith(js_served_locally):
                tag.decompose()
        except:
            pass

    # fix pdf paths?

    # other stuff
    for tag in soup(id="gt-page-title"):
        tag.decompose()
    for tag in soup(class_="gt-version", limit=1):
        tag.decompose()

    # write fixed version of file to disk
    with codecs.open(str(CONTENT_FOLDER / my_file), 'w', 'utf-8') as html_doc:
        #html_doc.write(str(soup))
        #html_doc.write(unicode(soup))
        html_doc.write(soup.prettify())

    # get the lock so that different threads can't update it at the same time
    with my_counter.get_lock():
        my_counter.value += 1
        my_bar.update(my_counter.value)


'''
For 14 html files (2 core, 4 thread machine, program run time):
    - single threaded:
        34.4s, 44.8s, 34.2s, 33.9s, 26.7s
    - multi-treaded:
        28.7s, 30.6s, 27.7s, 28.2s

For 11,168 files (2 core, 4 thread machine, program run time):
    - no html cleaning (so just overhead):
        13:50 (partial delete, 7-Zip), 24:52, 21:56, 25:59 (Zipfile)
'''

@task
def clean_adam_html_single_thread():
    '''Remove nasty and extra HTML.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Remove nasty and extra HTML (single threaded).")

    #os.chdir(str(CONTENT_FOLDER))
    all_files = os.listdir(str(CONTENT_FOLDER))
    all_html_files = []
    for my_file in all_files:
        if my_file.endswith(".html"):
            all_html_files.append(my_file)

    # this gives us a C-type integer, useful for accessing from multiple threads
    counter = multiprocessing.Value('i', 0)
    bar = minchin.text.progressbar(maximum=len(all_html_files))
    bar.update(counter.value)
    for my_file in all_html_files:
        html_fixes(my_file, bar, counter)
    print()  # clear progress bar


@task
def clean_adam_html_multithreaded():
    '''Remove nasty and extra HTML (multi-threaded).'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Remove nasty and extra HTML (multi-threaded).")

    #os.chdir(str(CONTENT_FOLDER))
    all_files = os.listdir(str(CONTENT_FOLDER))
    all_html_files = []
    for my_file in all_files:
        if my_file.endswith(".html"):
            all_html_files.append(my_file)

    # this gives us a C-type integer, useful for accessing from multiple threads
    counter = multiprocessing.Value('i', 0)
    bar = minchin.text.progressbar(maximum=len(all_html_files))
    bar.update(counter.value)

    jobs = []
    for my_file in all_html_files:
        p = multiprocessing.Process(target=html_fixes, args=(my_file, bar, counter))
        jobs.append(p)
        p.start()
    for job in jobs:
        job.join()

    print()  # clear progress bar


@task
def pelican():
    '''Run Pelican.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Run Pelican (site generator).")

    os.chdir(str(WORKING_FOLDER))
    run('pelican -s publishconf.py')


@task
def pelican_local():
    '''Run Pelican (in local, developmental mode).'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Run Pelican (site generator) in local mode.")

    os.chdir(str(WORKING_FOLDER))
    run('pelican -s pelicanconf.py')


@task
def create_tracking():
    '''Create deploy tracking file.'''
    global step_no
    global tracking_filename
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Create deploy tracking file.")

    # create a 'random' number using UUID
    # note that the last set of digits will correspond to the workstation
    myUUID = str(uuid.uuid1())
    tracking_filename = myUUID + ".txt"
    target = open(str(GITHUB_FOLDER / tracking_filename), 'w')
    target.write(myUUID + "\n")
    target.write("Adam upload by Python script.\n")
    target.write(GEDCOM_EXPECTED + "\n")
    target.close()


@task
def git():
    '''Git commit and push.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Git -> commit and push.")

    commit_msg = "Gigatrees generated upload from {}".format(GEDCOM_EXPECTED)
    os.chdir(str(GITHUB_FOLDER))
    minchin.text.clock_on_right('{}{}> git add -A{}'.format(INDENT, Fore.YELLOW, Style.RESET_ALL))
    r1 = run('git add -A')
    #print(r1.stdout)
    print(r1.stderr)
    minchin.text.clock_on_right('{}{}> git commit -m "{}"{}'.format(INDENT, Fore.YELLOW, commit_msg, Style.RESET_ALL))
    r2 = run('git commit -m Gigatrees_upload')
    #print(r2.stdout)
    print(r2.stderr)
    minchin.text.clock_on_right('{}{}> git push origin{}'.format(INDENT, Fore.YELLOW, Style.RESET_ALL))
    r3 = run('git push origin')
    print(r3.stdout)
    print(r3.stderr)


@task
def live():
    '''Tell us when we're live.'''
    # TO-DO: find tracking file based on creation/modified date
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Wait to go live.")

    if tracking_filename is None:
        print('{}No tracking file set.'.format(INDENT))
    else:
        while True:
            r = requests.head(URL_ROOT + "/" + tracking_filename, allow_redirects=True)
            if r.status_code == requests.codes.ok:
                break
            else:
                minchin.text.wait(180)


@task
def all_steps():
    '''Everything!'''
    minchin.text.title("Genealogy Uploader, v.{}".format(str(__version__)))
    print()

    '''
    export_gedcom()             # works 151230
    clean_gedcom()              # works
    upload_gedcom()             # works
    #check_images()              # works
    delete_old_output()         # works
    '''
    delete_old_adam()           # works ~2 min
    get_new_adam()              #
    unzip_adam()                # pretty sure works ~5 min
    '''
    #php_to_html()              # works, brakes if there are no PHP files
    copy_js()                   # works
    #copy_css()
    copy_img()
    replace_index()             # works
    set_pelican_variables()     # works
    clean_adam_html_single_thread()  # doesn't crash
    '''
    '''
    clean_adam_html_multithreaded()
    '''
    '''
    replace_emails()            # doesn't crash
    create_tracking()           # works ~10 sec
    pelican()                   # works (assuming Pelican works)
    #pelican_local()
    git()                      #
    live()                     #
    '''

    minchin.text.clock_on_right(Fore.GREEN + Style.BRIGHT + "Update is Live!")
    print(Style.RESET_ALL)

    print(INDENT, datetime.now() - start_time)


@task(default=True)
def does_nothing():
    print('this does nothing')


if __name__ == "__main__":
    all_steps()
