﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Genealogy Uploader
v.3.1.2 - WM - December 30, 2015

This script serves to semi-automate the building and uploading of my
genealogy website. It is intended to be semi-interactive and run from the
command line.'''


import codecs
import fileinput
import os
import re
import sys
import textwrap
import uuid
import webbrowser
import zipfile
from datetime import date, datetime
from pathlib import Path

import colorama
import minchin.text
import requests
from bs4 import BeautifulSoup
from colorama import Back, Fore, Style
from invoke import run, task
import winshell

# import envoy
# import winshell

__version__ = '3.1.2'
colorama.init()


COPYRIGHT_START_YEAR = 1987
ADAM_LINK = "http://gigatrees.com"
ADAM_FOOTER = "<p><strong>Are we related?</strong> Are you a long lost cousin? Spotted an error here? This website remains a work-in-progress and I would love to hear from you. Drop me a line at minchinweb [at] gmail [dot] com.</p>"
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
#start_time = datetime.now()
step_no = 0  # step counter
start_time = datetime.now()
HERE_FOLDER = Path.cwd()
WORKING_FOLDER = HERE_FOLDER  # current working directory
CONTENT_FOLDER = HERE_FOLDER / 'content' / 'pages'
adam_zip = ''               # set later
tracking_filename = ''      # set later


# globals for Lenovo X201
GITHUB_FOLDER = Path(r"C:\Users\User\Documents\GitHub\genealogy-gh-pages")
PHOTO_FOLER = Path(r"C:\Users\User\Documents\Genealogy")
DOWNLOAD_FOLDER = Path(r"C:\Users\User\Downloads")


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
    '''Export from RootsMagic'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Export from RootsMagic.")

    print("        call the file " + Style.BRIGHT + GEDCOM_EXPECTED + Style.RESET_ALL + " and save it to the desktop")
    print("        do not include LDS information")
    print("        no need to privatize individuals (at this step)")
    if not minchin.text.query_yes_quit("    Next?", default="yes"):
        sys.exit()
    try:
        start_time = datetime.fromtimestamp(os.stat(MY_GEDCOM).st_ctime)
    except:
        print("    Your file doesn't seem to exist. Exiting...")


@task
def clean_gedcom():
    '''Cleaning up GEDCOM'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Cleaning up GEDCOM...")

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
    '''Upload GEDCOM to Gigatree'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". The file is now ready to upload to Gigatrees.")

    webbrowser.open("http://gigatrees.com/toolbox/gigatree", new=2)
    print("        log-in (using Facebook)")
    print("        now click 'generate report'")
    # check to see if we're logged in
    # log in, if needed
    # discard old GEDCOM
    # upload new GEDCOM
    # run generator
    # download new output


@task
def check_images():
    '''Check which images have already been uploaded'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Checking images...")

    gedcom_file = open(str(MY_GEDCOM), 'r', encoding='utf-8')
    subject = gedcom_file.read()
    gedcom_file.close()

    missing_matches = []
    all_matches = []
    matches = 0
    wrapper = textwrap.TextWrapper(width=79, initial_indent=" "*6, subsequent_indent=" "*10)
    pattern_bad = re.compile("missing ")
    for match in re.findall(r'(images/.+\.(jpg|jpeg|png|gif|pdf))', subject, re.IGNORECASE):
        all_matches.append(match)

    all_matches = sorted(set(all_matches))  # remove duplicates and sort
    for match in all_matches:
        r = requests.head(env.url_root + "/" + str(match[0]), allow_redirects=True)
        if not r.status_code == requests.codes.ok:
            mytext = wrapper.fill("missing " + str(r.status_code) + " -> " + match[0])
            print(pattern_bad.sub(Fore.RED + Style.BRIGHT + "missing " + Style.RESET_ALL, mytext))
            missing_matches.append(match[0])
        else:
            matches += 1

    if len(missing_matches) == 0:
        print("        " + str(matches) + " images matching. No missing images.")
    else:
        print("        " + str(matches) + " images matching.")
        q_add_images = minchin.text.query_yes_no_all("        " + str(len(missing_matches)) + " missing images. Add them?", default="no")
        if q_add_images == 2:  # all
            for image in missing_matches:
                addimage(image)
        elif q_add_images == 1:  # yes
            for image in missing_matches:
                if minchin.text.querry_yes_no("        Add " + image + "?", default="yes"):
                    addimage(image)
                    # TO-DO: implement this!
                else:
                    pass
        else:  # no
            pass

        # write missing images to a file
        f = open('missing-images.txt', 'w', encoding='utf-8')
        f.write("Genealogy Uploader, v." + str(__version__) + '\n')
        f.write(MY_GEDCOM + '\n')
        f.write('\n')
        for missing in missing_matches:
            f.write(missing + '\n')
        f.close()


@task
def delete_old_output():
    '''Delete old Pelican output'''
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
    for myfile in to_delete:
        winshell.delete_file(myfile, no_confirm=True, allow_undo=False, silent=True)
        counter += 1
        bar.update(counter)
    print("\n      " + str(len(to_delete) + html_files) + " files deleted.")


@task
def delete_old_adam():
    '''Delete old Gigatrees output'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Deleting old Gigatree output.")

    os.chdir(str(CONTENT_FOLDER))
    run('del *.* /q')


@task
def get_new_adam():
    '''Get new Gigatree output'''
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
            if minchin.text.query_yes_quit("    We've waited 30 minutes. Keep waiting?", default="yes") is False:
                sys.exit()
            else:
                count_loops = 0
        else:
            minchin.text.wait(30)

    winshell.copy_file(adam_zip, str(CONTENT_FOLDER))


def step_unzip():
    # 6:48.948 for 9,999 files
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Unzip new Gigatree output (Zipfile).")

    os.chdir(str(CONTENT_FOLDER))
    zf = zipfile.ZipFile(adam_zip)
    zf.extractall()
    zf.close()


def step_unzip_faster():
    # see http://dmarkey.com/wordpress/2011/10/15/python-zipfile-speedup-tips/
    # 4:44.459 for 9,999 files
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Unzip new Gigatree output (Zipfile faster).")

    os.chdir(str(CONTENT_FOLDER))
    zf = zipfile.ZipFile(open(adam_zip, 'r'))
    zf.extractall()
    zf.close()


def step_unzip_czip():
    # 4:46.109 for 9,999 files
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Unzip new Gigatree output (czip).")

    os.chdir(str(CONTENT_FOLDER))
    zf = czipfile.ZipFile(adam_zip)
    zf.extractall()
    zf.close()


@task
def step_unzip_7zip():
    #  5:09.974 for 9,999 files
    global step_no
    start_time_local = datetime.now()
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Unzip new Gigatree output (7-zip).")

    os.chdir(str(CONTENT_FOLDER))
    run('"C:\\Program Files\\7-Zip\\7z.exe" e {} > nul'.format(adam_zip))
    print(" "*7, datetime.now() - start_time_local)


@task
def unzip_adam():
    '''Unzip new Adam output'''
    try:
        step_unzip_faster()
    except:
        step_unzip_7zip()


@task
def php_to_html():
    '''Change any .php files to .html'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Rename all .php files")
    os.chdir(str(CONTENT_FOLDER))
    run('rename *.php *.html')


@task
def copy_js():
    '''Copy Gigatree .js files'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Copy Gigatree .js files")
    os.chdir(str(CONTENT_FOLDER))

    js_files = ('tab-list-handler.js',
                'tooltip-handler.js',
                'graph-handler.js',
                'gigatrees-map-min.js', )

    for my_file in js_files:
        try:
            winshell.delete_file("../js/" + my_file, no_confirm=True, allow_undo=False, silent=True)
        except:
            pass
        winshell.copy_file(my_file, "../js/" + my_file, no_confirm=True)


@task
def copy_css():
    '''Copy Gigatree .css files'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Copy Gigatree .css files")
    os.chdir(str(CONTENT_FOLDER))

    js_files = ('gigatrees.css', )

    for my_file in js_files:
        try:
            winshell.delete_file("../css/" + my_file, no_confirm=True, allow_undo=False, silent=True)
        except:
            pass
        winshell.copy_file(my_file, "../css/" + my_file, no_confirm=True)


@task
def replace_index():
    '''Copy over index.md, 404.md'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Copy over index.md, 404.md")

    os.chdir(str(CONTENT_FOLDER))
    try:
        winshell.delete_file("index.md", no_confirm=True, allow_undo=False, silent=True)
    except:
        pass
    try:
        winshell.delete_file("index.html", no_confirm=True, allow_undo=False, silent=True)
    except:
        pass
    try:
        winshell.delete_file("404.md", no_confirm=True, allow_undo=False, silent=True)
    except:
        pass

    winshell.copy_file("../../_unchanging_pages/index.md", "index.md", no_confirm=True)
    winshell.copy_file("../../_unchanging_pages/404.md", "404.md", no_confirm=True)


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
    print('        {} - {}'.format(adam_version_text, date_in_text))

    f = open(str(WORKING_FOLDER / 'adamconf.py'), 'w')
    f.write('# Genealogy Uploader, v.{}\n'.format(str(__version__)))
    f.write('# {}\n\n'.format(str(MY_GEDCOM)))
    f.write('ADAM = True\n')
    f.write('ADAM_VERSION = "{}"\n'.format(adam_version_text))
    f.write('ADAM_UPDATED = "{}"\n'.format(date_in_text))
    f.write('ADAM_COPY_DATE = "{}"'.format(year_range))
    f.write('ADAM_LINK = "{}"'.format(ADAM_LINK))
    f.write('ADAM_FOOTER = "{}"'.format(ADAM_FOOTER))
    f.close()


@task
def replace_emails():
    '''Hide emails in Sources'''
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
    for file in all_html_files:
        for line in fileinput.input(file, inplace=1):
            print(multiple_replace(line, *replacements))
        counter += 1
        bar.update(counter)
    print()  # clear progress bar


@task
def clean_adam_html():
    '''Remove nasty and extra HTML.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Remove nasty and extra HTML.")

    os.chdir(str(CONTENT_FOLDER))
    all_files = os.listdir(str(CONTENT_FOLDER))
    all_html_files = []
    for my_file in all_files:
        if my_file.endswith(".html"):
            all_html_files.append(my_file)

    counter = 0
    bar = minchin.text.progressbar(maximum=len(all_html_files))
    for file in all_html_files:
        with codecs.open(str(CONTENT_FOLDER / file), 'r', 'utf-8') as html_doc:
            my_html = html_doc.read()

        soup = BeautifulSoup(my_html, "lxml")
        # change page title
        title_tag = soup.html.head.title
        for tag in soup(id="gt-page-title", limit=1):
            title_tag.string.replace_with(tag.string)
            tag.decompose()
        # dump all the meta tags in the head section
        for tag in soup("meta"):
            tag.decompose()
        # fix links that point to php pages
        for tag in soup("a", href=True):
            tag['href'] = tag['href'].replace('.php', '.html')
        # remove wrapper lists (ul/li) to tables
        #for tag in soup("ul"):
        #   tag2 = tag.findParent('ul')
        #       if tag2:
        #           tag2.replace_with(tag2.contents)
        #           # replace 'li' tags with 'p'
        #           #for tag3 in tag2("li"):
        #           #   tag3.name = 'p'

        # other stuff
        for tag in soup(id="gt-page-title"):
            tag.decompose()
        for tag in soup(class_="gt-version", limit=1):
            tag.decompose()

        with codecs.open(str(CONTENT_FOLDER / file), 'w', 'utf-8') as html_doc:
            #html_doc.write(str(soup))
            #html_doc.write(unicode(soup))
            html_doc.write(soup.prettify())

        counter += 1
        bar.update(counter)
    print()  # clear progress bar


@task
def pelican():
    '''Run Pelican'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Run Pelican (site generator)")

    os.chdir(str(WORKING_FOLDER))
    run('pelican -s publishconf.py')


@task
def pelican_local():
    '''Run Pelican (in local, developmental mode)'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Run Pelican (site generator)")

    os.chdir(str(WORKING_FOLDER))
    run('pelican -s pelicanconf.py')


@task
def create_tracking():
    '''Create deploy tracking file'''
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
    '''Git commit and push'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Git -> commit and push")

    commit_msg = "Adam generated upload from " + GEDCOM_EXPECTED.name
    os.chdir(str(GITHUB_FOLDER))
    minchin.text.clock_on_right('{}> git add -A{}'.format(Fore.YELLOW, Style.RESET_ALL))
    r1 = run('git add -A')
    print(r1.std_err,)
    minchin.text.clock_on_right('{}> git commit -m "{}"{}'.format(Fore.YELLOW, commit_msg, Style.RESET_ALL))
    r2 = run('git commit -m Gigatrees_upload')
    print(r2.std_out, r2.std_err,)
    minchin.text.clock_on_right('{}> git push origin{}'.format(Fore.YELLOW, Style.RESET_ALL))
    r3 = run('git push origin')
    print(r3.std_out, r3.std_err)


@task
def live():
    '''Tell us when we're live'''
    # TO-DO: find tracking file based on creation/modified date
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Wait to go live")

    if tracking_filename is None:
        print('No tracking file set.')
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
    minchin.text.title("Genealogy Uploader, v." + str(__version__))
    print

    export_gedcom()             # works 151230
    clean_gedcom()              # works
    #upload_gedcom()            # works
    #check_images()             # works
    delete_old_output()         # works
    delete_old_adam()           # works ~2 min
    get_new_adam()              #
    unzip_adam()                # pretty sure works ~5 min
    #php_to_html()              # works, brakes if there are no PHP files
    copy_js()                   # works
    #copy_css()
    replace_index()             # works
    set_pelican_variables()     # works
    clean_adam_html()           # doesn't crash
    replace_emails()            # doesn't crash
    create_tracking()           # works ~10 sec
    #pelican()                  # works (assuming Pelican works)
    pelican_local()
    #git()                      #
    #live()                     #

    minchin.text.clock_on_right(Fore.GREEN + Style.BRIGHT + "Update is Live")
    print(Style.RESET_ALL)

    print(" "*7, datetime.now() - start_time)


@task(default=True)
def does_nothing():
    print('this does nothing')


if __name__ == "__main__":
    all_steps()
