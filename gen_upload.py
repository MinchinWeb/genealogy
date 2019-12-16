#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Genealogy Uploader
v.4.0.4 - WM - December 15, 2019

This script serves to semi-automate the building and uploading of my
genealogy website. It is intended to be semi-interactive and run from the
command line.'''

# to call these tasks via `invoke`, use the `-c` parameter
# eg.
#       invoke -c gen_upload <task_name>

# TODO: make folders before trying to delete content from them.
# TODO: move Genealogy photos, etc to Z drive

import codecs
from datetime import date, datetime
import fileinput
from glob import iglob, glob
import multiprocessing as mp
import os
from pathlib import Path
import re
import sys
import textwrap
import uuid
import webbrowser
import zipfile

from bs4 import BeautifulSoup  # requires BeautifulSoup4 >= 4.5.0
import colorama
from colorama import Fore, Style
import invoke
from invoke import run, task  # requires invoke >= 0.13
from joblib import Parallel, delayed
import minchin.text
import requests
import winshell

try:
    import tbvaccine
except ImportError:
    pass
else:
    tbvaccine.add_hook(
        isolate=True,
    )


__version__ = '4.0.3'
colorama.init()

#######################
### Global Settings ###
#######################

COPYRIGHT_START_YEAR = 1987
ADAM_LINK = "http://gigatrees.com/"
ADAM_FOOTER = "<p><strong>Are we related?</strong> Are you a long lost cousin? Spotted an error here? This website remains a work-in-progress and I&nbsp;would love to hear from you. Drop me a line at minchinweb [at] gmail [dot] com.</p>"
INDENT = " "*4
GITHUB_FOLDER = Path("C:\\Users\\William\\Code\\genealogy-gh-pages")
PHOTO_FOLDER = Path("S:\Documents\Genealogy")
URL_ROOT = "http://genealogy.minchin.ca"
REPO_URL = "https://github.com/MinchinWeb/genealogy.git"
TODAY_STR = '' + str(date.today().year)[2:] + str.zfill(str(date.today().month), 2) + str.zfill(str(date.today().day), 2)
GEDCOM_EXPECTED = 'William ' + TODAY_STR + '.ged'
USER_FOLDER = Path(os.path.expanduser('~'))
MY_GEDCOM = USER_FOLDER / 'Desktop' / GEDCOM_EXPECTED
start_time = datetime.now()
step_no = 0  # step counter
# folder where the script is saved
HERE_FOLDER = Path(os.path.dirname(os.path.realpath(__file__)))
WORKING_FOLDER = HERE_FOLDER  # current working directory
CONTENT_FOLDER = HERE_FOLDER / 'content' / 'pages'
LOG_FOLDER = HERE_FOLDER / 'logs'
CONFIG_FOLDER = HERE_FOLDER / 'config'
MISSING_IMAGES_LOG = LOG_FOLDER / ('missing-images-' + TODAY_STR + '.txt')
tracking_filename = ''      # set later
ERROR_COLOUR = colorama.Fore.RED + colorama.Style.BRIGHT
WARNING_COLOUR = colorama.Fore.YELLOW + colorama.Style.BRIGHT
RESET_COLOUR = colorama.Fore.RESET + colorama.Style.RESET_ALL
ERROR_CODE = '[{}ERROR{}]'.format(ERROR_COLOUR, RESET_COLOUR)
WARNING_CODE = '[{}WARN{}]'.format(WARNING_COLOUR, RESET_COLOUR)
INVOKE_SHELL = 'C:\\Windows\\System32\\cmd.exe'
GIGATREES_EXE = Path('C:\\Users\\William\\bin\\gigatrees-pro\\cli\\gigatrees-pro.exe')
GIGATREES_ASSETS = GIGATREES_EXE.parent / 'assets'


# globals for Lenovo X201
#GITHUB_FOLDER = Path(r"C:\Users\User\Documents\GitHub\genealogy-gh-pages")
#PHOTO_FOLDER = Path(r"C:\Users\User\Documents\Genealogy")


#####################
### The Functions ###
#####################

def addimage(image):
    '''Take the file listed in image, finds in my genealogy photo directory, and
    adds it to the GitHub folder.'''
    # TODO: implement this!!
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
    with (CONTENT_FOLDER / 'names' / 'index.html').open(mode='r') as soup_file:
        soup = BeautifulSoup(soup_file, "lxml")
    return soup.find(id="gt-version").get_text().encode('utf-8').strip()  # 'Built by Adam 1.35.0.0' or the like


@task
def export_gedcom(ctx):
    '''Export from RootsMagic.'''
    # automate with pyautogui??
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
        start_time = datetime.fromtimestamp(os.stat(str(MY_GEDCOM)).st_ctime)
    except FileNotFoundError:
        print("{1} Your file doesn't seem to exist.\n{0}   Expecting {2}\n{0}   Exiting...".format(INDENT, ERROR_CODE, MY_GEDCOM))
        sys.exit(1)


@task
def clean_gedcom(ctx):
    '''Cleaning up GEDCOM.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Cleaning up GEDCOM.")

    subject = ''
    # TODO: convert to pathlib.Path.open() (here and elsewhere)
    with open(str(MY_GEDCOM), 'r', encoding='utf-8') as gedcom_file:
        subject = gedcom_file.read()

    # replace image paths
    pattern = re.compile(r'S:\\Documents\\Genealogy\\([0-9]+[\.[a-z]+]*\.? )*', re.IGNORECASE)  # path start
    result = pattern.sub('/images/', subject)
    pattern2 = re.compile(r'(images.*)\\')  # reverse slashes in rest of path
    result2 = pattern2.sub(r'\1/', result)
    result3 = pattern2.sub(r'\1/', result2)

    with open(str(MY_GEDCOM), 'w', encoding='utf-8') as gedcom_file:
        gedcom_file.write(result3)


@task
def check_images(ctx):
    '''Check which images have already been uploaded.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Checking images.")

    subject = ''
    with open(str(MY_GEDCOM), 'r', encoding='utf-8') as gedcom_file:
        subject = gedcom_file.read()

    missing_matches = []
    all_matches = []
    matches = 0
    wrapper = textwrap.TextWrapper(width=79, initial_indent=INDENT, subsequent_indent=INDENT*2)
    pattern_bad = re.compile("missing ")
    for match in re.findall(r'(images/.+\.(jpg|jpeg|png|gif|pdf))', subject, re.IGNORECASE):
        all_matches.append(match)

    all_matches = sorted(set(all_matches))  # remove duplicates and sort
    # TODO: move this to run in parallel
    for match in all_matches:
        r = requests.head(URL_ROOT + "/" + str(match[0]), allow_redirects=True)
        if not r.status_code == requests.codes.ok:
            mytext = wrapper.fill("missing {} -> {}".format(str(r.status_code), match[0]))
            print(pattern_bad.sub("{}missing{} ".format(WARNING_COLOUR, RESET_COLOUR), mytext))
            missing_matches.append(match[0])
        else:
            matches += 1

    if len(missing_matches) == 0:
        print("{}{} images matching. No missing images.".format(INDENT, str(matches)))
    else:
        print("{}{} images matching. {} missing images.".format(INDENT, str(matches), len(missing_matches)))
        # q_add_images = minchin.text.query_yes_no_all("{}Add missing images?".format(INDENT*2, default="no")
        # if q_add_images == 2:  # all
        #     for image in missing_matches:
        #         addimage(image)  # TO-DO: implement this!
        # elif q_add_images == 1:  # yes
        #     print()  # add blank line
        #     for image in missing_matches:
        #         if minchin.text.query_yes_no("{}Add {}?".format(INDENT, image), default="yes"):
        #             addimage(image)  # TO-DO: implement this!
        #         else:
        #             pass
        # else:  # no
        #     pass

        # write missing images to a file
        with open(str(MISSING_IMAGES_LOG), 'w', encoding='utf-8') as f:
            f.write("Genealogy Uploader, v.{}\n".format(str(__version__)))
            f.write('{}\n=== MISSING IMAGES ===\n\n'.format(MY_GEDCOM))
            for missing in missing_matches:
                f.write('{}\n'.format(missing))


@task
def delete_old_output(ctx):
    '''Delete old Pelican output.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Deleting old Pelican output.")

    to_delete = []
    html_files = 0
    try:
        os.chdir(str(GITHUB_FOLDER))
    except FileNotFoundError:
        print("    Directory does not (yet) exist. Skipping...")
        return

    all_files = os.listdir(str(GITHUB_FOLDER))

    for filename in all_files:
        if filename == ('.git'):
            pass  # don't drop the GIT repo
        elif filename == ('images'):
            pass  # don't drop the image folder
        elif filename.endswith('.html'):
            html_files += 1
        else:
            to_delete.append(filename)

    counter = 0

    # delete HTML files
    run('del /S /Q {}\*.html'.format(GITHUB_FOLDER), shell=INVOKE_SHELL, hide=True)
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
def delete_old_gigatrees(ctx):
    '''Delete old Gigatrees output.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Deleting old Gigatrees output.")

    run('del /S /Q {}\*.*'.format(CONTENT_FOLDER), shell=INVOKE_SHELL, hide=True)


@task
def call_gigatrees(ctx):
    '''Call Gigatrees executable.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Executing Gigatrees.")

    # log won't be created if log folder doesn't exist
    Path(LOG_FOLDER).mkdir(parents=True, exist_ok=True)

    my_cmd = (
        '"{0}" '
        # '-g '  # Gigatrees report
        #'-c "{1}\default.xml" '
        '-c "{1}\minchinca-4.4.1.xml" '  # XML configuration
        '-i "{2}" '
        '-o "{3}" '
        '-l "{4}\gigatrees-{5}.log"'
    ).format(
        GIGATREES_EXE,
        CONFIG_FOLDER,
        MY_GEDCOM,
        CONTENT_FOLDER,
        LOG_FOLDER,
        TODAY_STR
    )
    try:
        print("{}Log file is {}\gigatrees-{}.log".format(INDENT, LOG_FOLDER, TODAY_STR))
        run(my_cmd,
            shell=INVOKE_SHELL,
            #hide=True,
           )
    except invoke.exceptions.Failure:
        if not minchin.text.query_yes_quit("{}Gigatrees exited oddly. Continue anyways?".format(INDENT), default="yes"):
            sys.exit(1)


@task
def copy_gigatree_assets(ctx):
    '''Copy Gigatree .js, .css, and images files.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Copy Gigatree asset files.")
    # files are copied from the base GIGATREES_ASSETS to the `content / js`
    # (where Pelican will find them)

    dest_folder = (CONTENT_FOLDER / '..').resolve() / 'assets'

    for my_file in GIGATREES_ASSETS.iterdir():
        dest_path = str(dest_folder / my_file.name)
        source_path = str(my_file)
        #print(dest_path)
        #print(source_path)
        #print(my_file, my_file)
        try:
            winshell.delete_file(dest_path, no_confirm=True, allow_undo=False, silent=True)
        except:
            pass
        winshell.copy_file(source_path, dest_path, no_confirm=True)


@task
def replace_index(ctx):
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

    for my_file in ("index.md",
                    # "404.md"
                   ):
        winshell.copy_file("../../_unchanging_pages/{}".format(my_file), my_file, no_confirm=True)


@task
def set_pelican_variables(ctx):
    '''Sets a couple of variables that Pelican uses while generating the site.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Setting up Pelican.")

    try:
        adam_version_text = get_adam_version()  # 'Built by Adam 1.35.0.0 ' or the like
    except AttributeError:
        print(ERROR_CODE, 'Unable to find Gigatrees version. Quitting...')
        sys.exit(1)

    adam_version_text = adam_version_text.decode('utf-8').strip()
    date_in_text = date.today().strftime("%B %d, %Y").replace(' 0', ' ')  # 'January 7, 2014' or the like
    year_range = "{}-{}".format(COPYRIGHT_START_YEAR, datetime.now().year)
    print('{}{} -- {}'.format(INDENT, adam_version_text, date_in_text))

    with (CONFIG_FOLDER / 'adamconf.py').open(mode='w') as f:
        f.write('# Genealogy Uploader, v.{}\n'.format(str(__version__)))
        f.write('# datafile : {}\n\n'.format(str(MY_GEDCOM)))
        f.write('### This file is automatically generated. Any changes may be overwritten. ###\n\n')
        f.write('ADAM = True\n')
        f.write('ADAM_VERSION = "{}"\n'.format(adam_version_text))
        f.write('ADAM_UPDATED = "{}"\n'.format(date_in_text))
        f.write('ADAM_COPY_DATE = "{}"\n'.format(year_range))
        f.write('ADAM_LINK = "{}"\n'.format(ADAM_LINK))
        f.write('ADAM_FOOTER = "{}"\n'.format(ADAM_FOOTER))
        f.write('ADAM_PUBLISH = True\n')


@task
def replace_emails(ctx):
    '''Hide emails in Sources.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Hiding Emails.")

    # replace and hide emails; but some of these are over lines breaks,
    #  so we'll have to search and replace through the output
    # We are actually only considering 'Sources', as that's where
    #  all the emails seem to be...
    #
    # Should I deal with vertical tabs here too?
    replacements =  ("w_minchin@hotmail.com",           '[email redacted]'), \
                    ("bmartin@nznet.gen.nz",            '[email redacted]'), \
                    ("Bruce.Sinnamon@unisys.com",       '[email redacted]'), \
                    ("bunburypr@ozemail.com.au",        '[email redacted]'), \
                    ("canrcr@gmail.com",                '[email redacted]'), \
                    ("cardena.depper@gmx.net",          '[email redacted]'), \
                    ("d3gl@shaw.ca",                    '[email redacted]'), \
                    ("david@westerhamworkshop.co.uk",   '[email redacted]'), \
                    ("djcmgf@optonline.net",            '[email redacted]'), \
                    ("djcmgf@optonline.net",            '[email redacted]'), \
                    ("donaldminchin@yahoo.com",         '[email redacted]'), \
                    ("ffirlotte@xplornet.com",          '[email redacted]'), \
                    ("G.Mitchell@gcu.ac.uk",            '[email redacted]'), \
                    ("gloog@eircom.net",                '[email redacted]'), \
                    ("howard.blaxland@gmail.com",       '[email redacted]'), \
                    ("jerry.doyle@sbcglobal.net",       '[email redacted]'), \
                    ("kathy.edwards@fredericton.ca",    '[email redacted]'), \
                    ("kenhazel@gmail.com",              '[email redacted]'), \
                    ("lbwong@charter.net",              '[email redacted]'), \
                    ("minchinweb@gmail.com",            '[email redacted]'), \
                    ("nysgys@shaw.ca",                  '[email redacted]'), \
                    ("redjoanne_58@hotmail.com",        '[email redacted]'), \
                    ("sonofcam@bigpond.com",            '[email redacted]'), \
                    ("stewdee@hotmail.com",             '[email redacted]'), \
                    ("turtle@turtlebunbury.com",        '[email redacted]'), \
                    ("turtlebunbury@gmail.com",         '[email redacted]'), \
                    ("w.minchin@gmail.com",             '[email redacted]'), \
                    ("webmaster@minchin.ca",            '[email redacted]'), \

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


def html_fixes(my_file):
    '''
    Applies the various updates and changes I want done to the raw Gigatrees
    HTML.

    Assumes 'my_file' is in the CONTENT_FOLDER.
    Assumes 'my_file' is a string.
    Assumes 'my_file' is the full path
    '''
    with codecs.open(str(my_file), 'r', 'utf-8') as html_doc:
        my_html = html_doc.read()


    # change page title
    try:
        soup = BeautifulSoup(my_html, "lxml")
        title_tag = soup.html.head.title
    except AttributeError:
        soup = BeautifulSoup(my_html, "html5lib")
        title_tag = soup.html.head.title
    for tag in soup(id="gt-page-title", limit=1):
        title_tag.string.replace_with(tag.string.strip())
        tag.decompose()

    # dump all the meta tags in the head section
    for tag in soup("meta"):
        tag.decompose()

    ## fix links that point to php pages
    #for tag in soup("a", href=True):
    #    tag['href'] = tag['href'].replace('.php', '.html')

    ## remove wrapper lists (ul/li) to tables
    #for tag in soup("ul"):
    #   tag2 = tag.findParent('ul')
    #       if tag2:
    #           tag2.replace_with(tag2.contents)
    #           # replace 'li' tags with 'p'
    #           for tag3 in tag2("li"):
    #              tag3.name = 'p'

    # Remove links to CDN stuff I serve locally
    js_served_locally = (
        'jquery.min.js',
        'jquery-ui.min.js',  # old, so not re-added
        'bootstrap.min.js',
        'globalize.min.js',  # old, so not re-added
        'dx.chartjs.js',  # old, so not re-added
        'gigatrees-charts.js',
        'c3.min.js',
        'd3.min.js',
        'bootstrap-tooltip-handler.js',
        'jquery.mousewheel.min.js',  # used by FancyBox
        'jquery.fancybox.pack.js',
        'jquery.fancybox-buttons.js',
        'jquery.fancybox-media.js',
        'jquery.fancybox-thumbs.js',
        'fancybox-handler.js',
        'html5shiv.min.js',
        'respond.min.js',
    )
    js_served_from_page = (
        "var myImage='../assets/mapicon_u.png';",
        '$(document).ready(function () {\ndocument.getElementById("gt-version")"',
    )
    for tag in soup.find_all("script"):
        try:
            link = tag["src"]
            if link.endswith(js_served_locally):
                tag.decompose()
        except:
            pass
        
        try:
            if str(tag.contents[0]).lstrip().startswith(js_served_from_page):
                tag.decompose()
        except IndexError:
            pass

    # fix pdf paths?

    # build-in narbar
    try:
        soup.html.body.nav.decompose()
    except AttributeError:
        # doesn't exist
        pass
    # style section for gt-about-modal
    try:
        soup.html.body.style.decompose()
    except AttributeError:
        # doesn't exist
        pass

    # other stuff
    for tag in soup(id="gt-version", limit=1):
        tag.decompose()
    for tag in soup(id="site-title"):
        tag.decompose()
    for tag in soup(id="gt-about-modal", limit=1):
        tag.decompose()
    for tag in soup(id="gt-qscore", limit=1):
        tag.decompose()

    # replace spaces in references to sources with non-breaking spaces
    for tag in soup.find_all(class_="gsref"):
        for my_contents in tag.contents:
            try:
                my_contents.replace("[ ", "[&nbsp;").replace("[\n", "[&nbsp;\n").replace(" ]", "&nbsp;]")
            except TypeError:
                pass

    # as of Gigatrees 4.4.0, the "age" column is always empty, so dump it
    #for tag in soup.find_all(class_="gage")

    # manually define the slug for the page (i.e. where the output file will be)
    my_slug = Path(my_file).relative_to(CONTENT_FOLDER)
    my_slug = str(my_slug)
    my_slug = my_slug[:-5] if my_slug.endswith('.html') else my_slug
    # swap direction of slashes
    my_slug = my_slug.replace('\\', '/')
    # drop initial 'I' from individuals and 'S' from sources
    ## Links thoughout the output are hardcoded. So we could replace these with "{filename}" links, but I don't feel like do that right now
    # my_slug = ('profiles\\' + my_slug[10:]) if my_slug.startswith('profiles\\I') else my_slug
    # my_slug = ('sources\\' + my_slug[9:]) if my_slug.startswith('sources\\S') else my_slug
    new_tag_3 = soup.new_tag("meta", content=my_slug)
    new_tag_3.attrs['name'] = 'slug'
    soup.html.head.append(new_tag_3)

    # Override page title
    if my_slug == "names/index":
        try:
            title_tag.string.replace_with("Surnames")
        except AttributeError:  # i.e. title_tag == None
            pass

    # Add meta tags, used for the breadcrumbs in the link.
    # These are used by the Pelican engine and template engine.
    # They need to be in the <head> section, in the form:
    #
    # <head>
    #    <!-- other stuff... -->
    #    <meta name="at" content="Locations" />
    #    <meta name="at_link" content="places.html" />  <!-- this is added to SITEURL -->
    # </head>
    new_tags = False
    if my_slug.startswith("names/") and my_slug != "names/index":
        new_tag_1 = soup.new_tag("meta", content="Surnames")
        new_tag_2 = soup.new_tag("meta", content="names/index.html")
        new_tags = True
    elif my_slug.startswith("places/") and my_slug != "places/index":
        new_tag_1 = soup.new_tag("meta", content="Locations")
        new_tag_2 = soup.new_tag("meta", content="places/index.html")
        new_tags = True
    elif my_slug.startswith("sources/") and my_slug != "sources/index":
        new_tag_1 = soup.new_tag("meta", content="Sources")
        new_tag_2 = soup.new_tag("meta", content="sources/index.html")
        new_tags = True
        # not working??
    elif my_slug.startswith("timelines/") and my_slug != "timelines/index":
        new_tag_1 = soup.new_tag("meta", content="Timelines")
        new_tag_2 = soup.new_tag("meta", content="timelines/index.html")
        new_tags = True

    if new_tags:
        new_tag_1.attrs['name'] = 'at'
        new_tag_2.attrs['name'] = 'at_link'
        soup.html.head.append(new_tag_1)
        soup.html.head.append(new_tag_2)

    # prep images for image_process pelican plugin
    for tag in soup.find_all("img", class_="gt-image-photo"):
        if not 'image-process-gt-photo' in tag.attrs["class"]:
            tag.attrs["class"].append("image-process-gt-photo")

    # style map button
    for tag in soup.find_all("a", class_="btn"):
        if not 'btn-info' in tag.attrs["class"]:
            tag.attrs["class"].append("btn-info")

    # unwrap "Last Modified" from being in a list to being a paragraph
    for tag in soup.find_all("li", id="gt-modified"):
        tag.name = 'p'
        tag.parent.unwrap()  # remove outer <ul>

    # remove extra line breaks in main flow of document
    for tag in soup.find_all("br"):
        if tag.parent == soup.html.body:
            tag.decompose()

    # write fixed version of file to disk
    with codecs.open(str(my_file), 'w', 'utf-8') as html_doc:
        html_doc.write(soup.prettify(formatter="html"))


def html_fixes_2(my_file, my_bar, my_counter):
    '''
    Applies the HTML changes and then updates the counter.

    Assumes 'my_bar' is of type minchin.text.progressbar
    Assumes 'my_counter' is of type multiprocessing.Value
    '''
    html_fixes(my_file)
    # get the lock so that different threads can't update it at the same time
    with my_counter.get_lock():
        my_counter.value += 1
        my_bar.update(my_counter.value)


'''
For 11,146 files (2 core, 4 thread machine, program run time):
    - no html cleaning (so just overhead):
        13:50 (partial delete, 7-Zip), 24:52, 21:56, 25:59 (Zipfile)
    - single thread: 18:49.190113
    - multi-threaded (n_jobs=9): 4:59.657586
'''


@task
def clean_adam_html_single_thread(ctx):
    '''Remove nasty and extra HTML.'''
    global step_no
    start_time_local = datetime.now()
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Remove nasty and extra HTML (single threaded).")

    # https://stackoverflow.com/a/40755802/4276230
    all_html_files = glob(str(CONTENT_FOLDER) + '/**/*.html', recursive=True)

    # this gives us a C-type integer, useful for accessing from multiple threads
    counter = mp.Value('i', 0)
    bar = minchin.text.progressbar(maximum=len(all_html_files))
    bar.update(counter.value)
    for my_file in all_html_files:
        html_fixes_2(my_file, bar, counter)
    print()  # clear progress bar
    print(INDENT, datetime.now() - start_time_local)


@task
def clean_adam_html_multithreaded(ctx, my_n_jobs=None):
    '''Remove nasty and extra HTML (multi-threaded).'''
    '''
    Benchmarks

    n_jobs      time
    9           6:20
    6           6:18  (machine has 6 cores)
    4           7:16
    '''
    global step_no
    #start_time_local = datetime.now()
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Remove nasty and extra HTML (multi-threaded).")

    # https://stackoverflow.com/a/40755802/4276230
    all_html_files = iglob(str(CONTENT_FOLDER) + '/**/*.html', recursive=True)

    if my_n_jobs is None:
        my_n_jobs = int(os.cpu_count())
    Parallel(n_jobs=my_n_jobs, verbose=5)(delayed(html_fixes)(my_file) for my_file in all_html_files)
    #print(INDENT, datetime.now() - start_time_local)


@task
def pelican(ctx):
    '''Run Pelican.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Run Pelican (site generator).")

    # TODO: run pelican directly
    #               drop command line args into sys.argv (with the first one
    #               being the script name, so 'pelican' (?)), and then call
    #               pelican.main()
    os.chdir(str(WORKING_FOLDER))
    run('pelican -s {}/publishconf.py'.format(HERE_FOLDER), shell=INVOKE_SHELL)


@task
def pelican_local(ctx):
    '''Run Pelican (in local, developmental mode).'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Run Pelican (site generator) in local mode.")

    os.chdir(str(WORKING_FOLDER))
    run('pelican -s {}/pelicanconf.py'.format(HERE_FOLDER), shell=INVOKE_SHELL)


@task
def create_tracking(ctx):
    '''Create deploy tracking file.'''
    global step_no
    global tracking_filename
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Create deploy tracking file.")

    # make sure the destination directory exists
    GITHUB_FOLDER.mkdir(parents=True, exist_ok=True)

    # create a 'random' number using UUID
    # note that the last set of digits will correspond to the workstation
    myUUID = str(uuid.uuid1())
    tracking_filename = myUUID + ".txt"
    with (GITHUB_FOLDER / tracking_filename).open(mode='w') as target:
        target.write(myUUID + "\n")
        target.write("Adam upload by Python script.\n")
        target.write(GEDCOM_EXPECTED + "\n")
    print('{}Tracking: {}'.format(INDENT, myUUID))


@task
def git(ctx):
    '''Git commit and push.'''
    global step_no
    step_no += 1
    minchin.text.clock_on_right(str(step_no).rjust(2) + ". Git -> commit and push.")

    commit_msg = "Gigatrees generated upload from {}".format(GEDCOM_EXPECTED)
    os.chdir(str(GITHUB_FOLDER))
    minchin.text.clock_on_right('{}{}> git add -A{}'.format(INDENT, Fore.YELLOW, Style.RESET_ALL))
    r1 = run('git add -A', hide=True, shell=INVOKE_SHELL)
    #print(r1.stdout)
    print(r1.stderr)
    minchin.text.clock_on_right('{}{}> git commit -m "{}"{}'.format(INDENT, Fore.YELLOW, commit_msg, Style.RESET_ALL))
    r2 = run('git commit -m "Gigatrees upload {}"'.format(TODAY_STR), hide=True, shell=INVOKE_SHELL)
    #print(r2.stdout)
    print(r2.stderr)
    minchin.text.clock_on_right('{}{}> git push origin{}'.format(INDENT, Fore.YELLOW, Style.RESET_ALL))
    r3 = run('git push origin', hide=True, shell=INVOKE_SHELL)
    print(r3.stdout)
    print(r3.stderr)


@task
def live(ctx):
    '''Tell us when we're live.'''
    # TODO: find tracking file based on creation/modified date
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
def all_steps(ctx):
    '''Everything!'''
    minchin.text.title("Genealogy Uploader, v.{}".format(str(__version__)))
    print()

    export_gedcom(ctx)             # works 160717
    clean_gedcom(ctx)              # works 160717
    delete_old_gigatrees(ctx)      # works 160717  ~2 min
    call_gigatrees(ctx)            # works 160718
    check_images(ctx)              # works 160717
    delete_old_output(ctx)         # works 160718
    # copy_gigatree_assets(ctx)      # works 160718
    replace_index(ctx)             # works 160721
    set_pelican_variables(ctx)     # works 160721
    # clean_adam_html_single_thread(ctx)  # doesn't crash
    clean_adam_html_multithreaded(ctx)  # runs 20160721
    # replace_emails(ctx)            # runs 20160721  # now configured with Gigatrees
    create_tracking(ctx)           # works 20160721
    pelican(ctx)                   # works (assuming Pelican works)
    # pelican_local(ctx)
    git(ctx)                       #
    live(ctx)                      #

    minchin.text.clock_on_right(Fore.GREEN + Style.BRIGHT + "Update is Live!")
    print(Style.RESET_ALL)

    print(INDENT, datetime.now() - start_time)


@task(default=True)
def does_nothing(ctx):
    print('this does nothing')


if __name__ == "__main__":
    all_steps(invoke.context.Context())
