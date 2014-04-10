#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Genealogy Uploader
v.3.0 - WM - April 9, 2014

This script serves to semi-automate the building and uploading of my
genealogy website. It is intended to be semi-interactive and run from the
command line.'''

__version__ = 3.0
github_folder = "S:\\Documents\\GitHub\\genealogy-gh-pages"
photo_folder = "S:\\Documents\\genealogy"
download_folder = "S:\\Downloads\\Firefox"
url_root = "http://minchin.ca/genealogy"
repo_url = "https://github.com/MinchinWeb/genealogy.git"
adam_prefix = 'adam-1246-'

from datetime import datetime
from datetime import date
import colorama
from colorama import Fore, Back, Style
colorama.init()
import re
import fileinput
import textwrap
import webbrowser
import os
import zipfile
import uuid
import sys
import winshell
import requests
from bs4 import BeautifulSoup
import envoy
import wmtext

today = '' + str(date.today().year)[2:] + str.zfill(str(date.today().month), 2) + str.zfill(str(date.today().day), 2)
gedcom_expected = 'William ' + today + '.ged'
my_gedcom = winshell.desktop() + "\\" + gedcom_expected
#start_time = datetime.now()
step_no = 0 # step counter
start_time = datetime.now()

def addimage(image):
	'''Take the file listed in image, finds in my genealogy photo directory, and
	adds it to the GitHub folder.'''
	'''TO-DO: implement this!!'''
	pass

# multiple replacement
# from 	http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
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




def step_export():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Export from RootsMagic.")

	print("        call the file " + Style.BRIGHT + gedcom_expected + Style.RESET_ALL + " and save it to the desktop")
	print("        do not include LDS information")
	print("        no need to privatize individuals (at this step)")
	if not wmtext.query_yes_quit("    Next?", default="yes"):
		sys.exit()
	global start_time
	start_time = datetime.fromtimestamp(os.stat(my_gedcom).st_ctime)


def step_clean_gedcom():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Cleaning up GEDCOM...")

	# replace image paths
	gedcom_file = file(my_gedcom, 'r') # add failsafe is the fail doesn't exist yet or is still being written to
	subject = gedcom_file.read()
	gedcom_file.close()

	pattern = re.compile(r'S:\\Documents\\Genealogy\\([0-9]+[\.[a-z]+]*\.? )*', re.IGNORECASE) # path start
	result = pattern.sub('images/', subject)
	pattern2 = re.compile(r'(images.*)\\') # reverse slashes in rest of path
	result2 = pattern2.sub(r'\1/', result)
	result3 = pattern2.sub(r'\1/', result2)

	f_out = file(my_gedcom, 'w')
	f_out.write(result3)
	f_out.close()


def step_upload_gedcom():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". The file is now ready to upload to Adam.")

	webbrowser.open("http://timforsythe.com/tools/adam", new=2)
	print("        log-in (using Facebook)")
	print("        now click 'generate report'")
	# check to see if we're logged in
	# log in, if needed
	# discard old GEDCOM
	# upload new GEDCOM
	# run generator
	# download new output


def step_check_images():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Checking images...")

	gedcom_file = open(my_gedcom, 'r')
	subject = gedcom_file.read()
	gedcom_file.close()

	missing_matches = []
	all_matches = []
	matches = 0
	wrapper = textwrap.TextWrapper(width=79, initial_indent=" "*6, subsequent_indent=" "*10)
	pattern_bad = re.compile("missing ")
	for match in re.findall(r'(images/.+\.(jpg|jpeg|png|gif|pdf))', subject, re.IGNORECASE):
		all_matches.append(match)
	
	all_matches = set(all_matches) # remove duplicates
	for match in all_matches:
		r = requests.head(url_root + "/" + str(match[0]), allow_redirects=True)
		if not r.status_code == requests.codes.ok:
			mytext = wrapper.fill("missing " + str(r.status_code) + " -> " + match[0])
			print pattern_bad.sub(Fore.RED + Style.BRIGHT + "missing " + Style.RESET_ALL, mytext)
			missing_matches.append(match[0])
		else:
			matches += 1

	if len(missing_matches) == 0:
		print("        " + str(matches) + " images matching. No missing images.")
	else:
		print("        " + str(matches) + " images matching.")
		q_add_images = wmtext.query_yes_no_all("        " + str(len(missing_matches)) + " missing images. Add them?", default="no")
		if q_add_images == 2: #all
			for image in missing_matches:
				addimage(image)
		elif q_add_images == 1: #yes
			for image in missing_matches:
				if wmtext.querry_yes_no("        Add " + image + "?", default="yes"):
					addimage(image)
					# TO-DO: implement this!
				else:
					pass
		else: #no
			pass
			
		# write missing images to a file
		f = open('missing-images.txt', 'w')
		f.write("Genealogy Uploader, v." + str(__version__) + '\n')
		f.write(my_gedcom + '\n')
		f.write('\n')
		for missing in missing_matches:
			f.write(missing + '\n')
		f.close()
		

def step_clean_old_output():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Deleting old Adam output.")

	to_delete = []
	os.chdir(github_folder)
	all_files = os.listdir(github_folder)

	for filename in all_files:
		if filename == ('.git'):
			pass
		else:
			to_delete.append(filename)

	counter = 0
	bar = wmtext.progressbar(maximum = len(to_delete))
	for myfile in to_delete:
		winshell.delete_file(myfile, no_confirm = True, allow_undo = False, silent = True)
		counter += 1
		bar.update(counter)
	print("\n        " + str(len(to_delete)) + " files deleted.")

	
def step_get_new_output():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Get new Adam output.")

	global adam_zip
	adam_zip = ''
	os.chdir(download_folder)

	count_loops = 0
	while True:
		all_files = os.listdir(download_folder)
		for filename in all_files:
			if filename.startswith(adam_prefix) and filename.endswith(".zip"):
				if datetime.fromtimestamp(os.stat(filename).st_ctime) > start_time:
					adam_zip = filename
		if adam_zip != '' and os.stat(adam_zip).st_size > 1000:
			break
		count_loops +=1
		if count_loops > 60:
			if wmtext.query_yes_quit("    We've waited 30 minutes. Keep waiting?", default="yes") == False:
				sys.exit()
			else:
				count_loops = 0
		else:
			wmtext.wait(30)
		
	winshell.copy_file(adam_zip, github_folder)


def step_unzip():
	# 6:48.948 for 9,999 files
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Unzip new Adam output.")

	os.chdir(github_folder)
	zf = zipfile.ZipFile(adam_zip)
	zf.extractall()
	zf.close()


def step_unzip_faster():
	# see http://dmarkey.com/wordpress/2011/10/15/python-zipfile-speedup-tips/
	# 4:44.459 for 9,999 files
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Unzip new Adam output.")

	os.chdir(github_folder)
	zf = zipfile.ZipFile(open(adam_zip, 'r'))
	zf.extractall()
	zf.close()


def step_unzip_czip():
	# 4:46.109 for 9,999 files
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Unzip new Adam output.")

	os.chdir(github_folder)
	zf = czipfile.ZipFile(adam_zip)
	zf.extractall()
	zf.close()


def step_unzip_7zip():
	#  5:39.121 for 9,999 files
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Unzip new Adam output.")

	os.chdir(github_folder)
	my_cmd = r'"C:\Program Files\7-Zip\7z.exe" e ' + adam_zip + ' > nul'
	#print my_cmd
	r4 = os.system(my_cmd)


def step_replace_index():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Copy over index.html")

	os.chdir(github_folder)
	winshell.delete_file("index.html", no_confirm = True, allow_undo = False, silent = True)
	winshell.copy_file("_adam/index.html", "index.html", no_confirm = True)

	
def step_replace_text():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Replacing Adam version number.")

	print("    Updated dates")
	print("    Hiding emails")
	soup_file = open('names.html', 'r')
	soup = BeautifulSoup(soup_file)
	soup_file.close()
	adam_version_text = soup.find(True, "adam-version").get_text().encode('utf-8') # 'Built by Adam 1.35.0.0 ' or the like
	date_in_text = date.today().strftime("%B %d, %Y").replace(' 0', ' ') # 'January 7, 2014' or the like
	# replace and hide emails; but some of these are over lines breaks,
	#  so we'll have to search and replace through the output
	replacements =	("$adam-version$",					 adam_version_text), \
					("$tree-updated$",					 date_in_text),      \
					("w_minchin@hotmail.com",			'[email redacted]'), \
					("w.minchin@gmail.com",				'[email redacted]'), \
					("webmaster@minchin.ca",			'[email redacted]'), \
					("minchinweb@gmail.com",			'[email redacted]'), \
					("nysgys@shaw.ca",					'[email redacted]'), \
					("bunburypr@ozemail.com.au",		'[email redacted]'), \
					("turtle@turtlebunbury.com",		'[email redacted]'), \
					("howard.blaxland@gmail.com",		'[email redacted]'), \
					("kenhazel@gmail.com",				'[email redacted]'), \
					("canrcr@gmail.com",				'[email redacted]'), \
					("david@westerhamworkshop.co.uk",	'[email redacted]'), \
					("d3gl@shaw.ca",					'[email redacted]'), \
					("cardena.depper@gmx.net",			'[email redacted]'), \
					("redjoanne_58@hotmail.com",		'[email redacted]'), \
					("lbwong@charter.net",				'[email redacted]'), \
					("djcmgf@optonline.net",			'[email redacted]'), \
					("jerry.doyle@sbcglobal.net",		'[email redacted]'), \
					("sonofcam@bigpond.com",			'[email redacted]'), \
					("stewdee@hotmail.com",				'[email redacted]'), \
					("nysgys@shaw.ca",					'[email redacted]'), \
					("gloog@eircom.net",				'[email redacted]')

	all_files = os.listdir(github_folder)
	all_html_files = []
	for my_file in all_files:
		if my_file.endswith(".html"):
			all_html_files.append(my_file)
	counter = 0
	bar = wmtext.progressbar(maximum = len(all_html_files))
	# inline search and replace
	for file in all_html_files:
		for line in fileinput.input(file, inplace=1):
			print multiple_replace(line, *replacements)
		counter += 1
		bar.update(counter)
	print # clear progress bar


def step_clean_html():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Remove nasty HTML")

	counter = 0
	bar = wmtext.progressbar(maximum = len(all_html_files))
	for file in all_html_files:
		soup = BeautifulSoup(file)
		for tag in soup(property="og:title", limit=1):
			tag.decompose()
		for tag in soup(charset=True, limit=1):
			tag.decompose()
		counter += 1
		bar.update(counter)
	print # clear progress bar


def step_tracking():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Create deploy tracking file")

	# create a 'random' number using UUID
	# note that the last set of digits will correspond to the workstation
	myUUID = str(uuid.uuid1())
	tracking_filename = myUUID + ".txt"
	target = open(tracking_filename, 'w')
	target.write(myUUID + "\n")
	target.write("Adam upload by Python script.\n")
	target.write(gedcom_expected + "\n")
	target.close()


def step_git():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Git -> commit and push")

	#commit_msg = "Adam generated upload from " + gedcom_expected
	os.chdir(github_folder)
	wmtext.clock_on_right(Fore.YELLOW + ' > git add -A' + Style.RESET_ALL)
	r1 = envoy.run('git add -A')
	print r1.std_err,
	wmtext.clock_on_right(Fore.YELLOW + '> git commit -m Adam_upload' + Style.RESET_ALL)
	r2 = envoy.run('git commit -m Adam_upload')
	print r2.std_out, r2.std_err,
	wmtext.clock_on_right(Fore.YELLOW + '> git push origin' + Style.RESET_ALL)
	r3 = envoy.run('git push origin')
	print r3.std_out, r3.std_err


def step_live():
	global step_no
	step_no += 1
	wmtext.clock_on_right(str(step_no).rjust(2) + ". Wait to go live")
	while True:
		r = requests.head(url_root + "/" + tracking_filename, allow_redirects=rue)
		if r.status_code == requests.codes.ok:
			break
		else:
			wmtext.wait(180)


if __name__ == "__main__":
	wmtext.title("Genealogy Uploader, v." + str(__version__))
	print
	
	#step_export()
	step_clean_gedcom()
	#step_upload_gedcom()
	step_check_images()
	#step_clean_old_output()
	#step_get_new_output()
	#step_unzip_faster()
	#step_replace_index()
	#step_replace_text()
	#step_clean_html()
	#step_tracking()
	#step_git()
	#step_live()
	
	wmtext.clock_on_right(Fore.GREEN + Style.BRIGHT + "Update is Live")
	print Style.RESET_ALL
	
	print datetime.now() - start_time
